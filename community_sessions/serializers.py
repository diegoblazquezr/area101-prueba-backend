from rest_framework import serializers
from .models import Session, Reservation

class ReservationSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['created_at', 'session']


class SessionSerializer(serializers.ModelSerializer):
    available_slots = serializers.IntegerField(read_only=True)

    # Incluyo reservas actuales en el detalle
    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = '__all__'