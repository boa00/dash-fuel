from datetime import timedelta

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from ..models import TankSales, AverageTankSales


def update_avg_sales_at_date(current_date, sender, tank):
    dates_to_update = [current_date - timedelta(days=i) for i in range(0, 29, 7)]
    query_set = sender.objects.filter(sales_date__in=dates_to_update).all()
    if query_set.count() < 5:
        try:
            avg_sales_to_delete = AverageTankSales.objects.get(sales_date=current_date)
            avg_sales_to_delete.delete()
        except AverageTankSales.DoesNotExist:
            pass
        return
    five_week_avg_sales = (
        query_set.aggregate(Sum('sales'))['sales__sum']  / 
        query_set.aggregate(Sum('sales_count'))['sales_count__sum']
    )
    avg_sales, _ = AverageTankSales.objects.update_or_create(
        sales_date=current_date, 
        tank=tank,
        defaults={
            "five_week_avg_sales": five_week_avg_sales,
        }
    )
    avg_sales.save()

@receiver([post_save, post_delete], sender=TankSales)
def update_average_sales_after_save_create(sender, instance, **kwarg):
    dates_to_check = [instance.sales_date + timedelta(days=i) for i in range(0, 29, 7)]
    for current_date in dates_to_check:
        update_avg_sales_at_date(current_date=current_date, sender=sender, tank=instance.tank)
