from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.expressions import Window
from django.db.models.functions import Lag
from django.db.models import Q, F, Case, When, FloatField

from ..models import TankVolume, TankSales


def get_sales_data_for_day(model, day):
    query_set = model.objects.filter(created_at_date=day).all()
    if query_set.count() == 0:
        return None
    date_first = query_set.order_by("created_at").first().created_at
    last_from_prev_day = model.objects.filter(created_at__lt=date_first).order_by("created_at").last()
    if last_from_prev_day:
        query_set |= model.objects.filter(pk=last_from_prev_day.pk)
    return query_set

def calculate_sales(query_set):
    query_set = (
        query_set
        .annotate(
            sales = F("volume") - Window(
                expression=Lag('volume'), 
                order_by=F('created_at').asc(),
                )
        )
        .annotate(
            sales = Case(When(Q(sales__lt=0) | Q(sales__isnull=True), then=0), default=F("sales"), output_field=FloatField())
        )
        .all()
        .values_list("sales", flat=True)
    )
    total_sales, sales_count = 0, 0
    for sales_for_the_day in query_set:
        total_sales += sales_for_the_day
        sales_count += 1 if sales_for_the_day != 0 else 0
    return total_sales, sales_count

@receiver([post_save, post_delete], sender=TankVolume, dispatch_uid="update_sales_after_save")
def update_sales_after_save_create(sender, instance, **kwargs):
    query_set = get_sales_data_for_day(model=sender, day=instance.created_at_date)
    if not query_set:
        try:
            tank_sales_del = TankSales.objects.get(sales_date=instance.created_at_date)
            tank_sales_del.delete()
        except TankSales.DoesNotExist:
            pass
        return
    total_sales, sales_count = calculate_sales(query_set)
    day_sales, _ = TankSales.objects.update_or_create(
        sales_date=instance.created_at_date, 
        tank=instance.tank,
        defaults={
            "sales": total_sales, 
            "sales_count": sales_count,
        }
    )
    day_sales.save()
    