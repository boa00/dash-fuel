from django.db import models
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist


class TankQuerySet(models.QuerySet):
    def search(self, query):
        if query:
            lookups = Q(name__icontains=query)
            return self.filter(lookups)
        return self


class TankManager(models.Manager):
    def get_queryset(self):
        return TankQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)


class Tank(models.Model):
    name = models.CharField(max_length=120)

    objects = TankManager()


class TankVolumeQuerySet(models.QuerySet):

    def sort(self, order, col):
        order = "desc" if not order else order
        try:
            col = TankVolume._meta.get_field(col)
        except FieldDoesNotExist:
            col = "created_at"
        order_by = col if order == "asc" else "-" + col
        return self.order_by(order_by)

    def filter_by_tank(self, tank_id):
        if tank_id:
            return self.filter(tank__id=tank_id)
        return self


class TankVolumeManager(models.Manager):
    def get_queryset(self):
        return TankVolumeQuerySet(self.model, using=self._db)

    def sort(self, order, col):
        return self.get_queryset().sort(order=order, col=col)

    def filter_by_tank(self, tank_id):
        return self.get_queryset().filter_by_tank(tank_id=tank_id)


class TankVolume(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, null=False)
    volume = models.FloatField()
    created_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at_date = models.DateField(db_index=True, auto_now=True)

    objects = TankVolumeManager()


class TankSalesQuerySet(models.QuerySet):

    def filter_by_tank(self, tank_id):
        if tank_id:
            return self.filter(tank__id=tank_id)
        return self


class TankSalesManager(models.Manager):
    def get_queryset(self):
        return TankSalesQuerySet(self.model, using=self._db)

    def filter_by_tank(self, tank_id):
        return self.get_queryset().filter_by_tank(tank_id=tank_id)

class TankSales(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, null=False)
    sales_date = models.DateField(db_index=True)
    sales = models.FloatField()
    sales_count = models.IntegerField()

    objects = TankSalesManager()


class AverageTankSalesQuerySet(models.QuerySet):
    def filter_by_tank(self, tank_id):
        if tank_id:
            return self.filter(tank__id=tank_id)
        return self


class AverageTankSalesManager(models.Manager):
    def get_queryset(self):
        return AverageTankSalesQuerySet(self.model, using=self._db)

    def filter_by_tank(self, tank_id):
        return self.get_queryset().filter_by_tank(tank_id=tank_id)

class AverageTankSales(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, null=False)
    sales_date = models.DateField(db_index=True)
    five_week_avg_sales = models.FloatField()

    objects = AverageTankSalesManager()
