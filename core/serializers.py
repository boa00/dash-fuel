from rest_framework import serializers

from .models import (
    Tank, 
    TankVolume, 
    TankSales,
    AverageTankSales,
)

class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = "__all__"

class TankVolumeSerializer(serializers.ModelSerializer):
    tank = serializers.CharField(source='tank.name')

    class Meta:
        model = TankVolume
        fields = "__all__"
        read_only_fields = ['tank']

    def create(self, validated_data):
        tank_name = validated_data.pop('tank')["name"]
        try:
            tank = Tank.objects.get(name=tank_name)
            validated_data["tank"] = tank
            tank_volume_instance = TankVolume.objects.create(volume=validated_data["volume"], tank=tank)
            return tank_volume_instance
        except Tank.DoesNotExist:
            raise serializers.ValidationError("No tank with such name present")

class TankSalesSerializer(serializers.ModelSerializer):
    tank = serializers.CharField(source='tank.name')

    class Meta:
        model = TankSales
        fields = "__all__"

class AverageTankSalesSerializer(serializers.ModelSerializer):
    tank = serializers.CharField(source='tank.name')
    
    class Meta:
        model = AverageTankSales
        fields = "__all__"
        