from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from .serializers import (
    TankSerializer, 
    TankVolumeSerializer, 
    TankSalesSerializer,
    AverageTankSalesSerializer,
)
from .models import (
    Tank, 
    TankVolume, 
    TankSales, 
    AverageTankSales,
)

class TankListCreateView(ListCreateAPIView):
    serializer_class = TankSerializer
    queryset = Tank.objects.all()

    def get_queryset(self):
        queryset = (
            Tank
            .objects
            .search(query=self.request.query_params.get('query', None))
        )
        return queryset


class TankRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TankSerializer
    queryset = Tank.objects.all()


class TankVolumeListCreateView(ListCreateAPIView):
    serializer_class = TankVolumeSerializer
    queryset = TankVolume.objects.all()

    def get_queryset(self):
        queryset = (
            TankVolume
            .objects
            .filter_by_tank(tank_id=self.request.query_params.get('tank_id', None))
            .sort(
                order=self.request.query_params.get('order_by', None),
                col=self.request.query_params.get('sort_by', None),
            )
        )
        return queryset


class TankVolumeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TankVolumeSerializer
    queryset = TankVolume.objects.all()

    def get_queryset(self):
        queryset = (
            TankVolume
            .objects
            .filter_by_tank(tank_id=self.request.query_params.get('tank_id', None))
            .sort(
                order=self.request.query_params.get('order_by', None),
                col=self.request.query_params.get('sort_by', None),
            )
        )
        return queryset


class TankSalesListView(ListAPIView):
    serializer_class = TankSalesSerializer
    queryset = TankSales.objects.all()

    def get_queryset(self):
        queryset = (
            TankSales
            .objects
            .filter_by_tank(tank_id=self.request.query_params.get('tank_id', None))
        )
        return queryset

class TankSalesRetrieveView(RetrieveAPIView):
    serializer_class = TankSalesSerializer
    queryset = TankSales.objects.all()

    def get_queryset(self):
        queryset = (
            TankSales
            .objects
            .filter_by_tank(tank_id=self.request.query_params.get('tank_id', None))
        )
        return queryset

class AverageTankSalesListView(ListAPIView):
    serializer_class = AverageTankSalesSerializer
    queryset = AverageTankSales.objects.all()

    def get_queryset(self):
        queryset = (
            AverageTankSales
            .objects
            .filter_by_tank(tank_id=self.request.query_params.get('tank_id', None))
        )
        return queryset

class AverageTankSalesRetrieveView(RetrieveAPIView):
    serializer_class = AverageTankSalesSerializer
    queryset = AverageTankSales.objects.all()

    def get_queryset(self):
        queryset = (
            AverageTankSales
            .objects
            .filter_by_tank(tank_id=self.request.query_params.get('tank_id', None))
        )
        return queryset
