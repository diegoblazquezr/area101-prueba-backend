from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, F
from .models import Session, Reservation
from .serializers import SessionSerializer, ReservationSerializer

class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.all().annotate(res_count=Count('reservations'))
    serializer_class = SessionSerializer

    def get_queryset(self):
        return self.queryset.filter(res_count__lt=F('capacity'))

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        session = self.get_object()
        if session.available_slots <= 0:
            return Response({'detail': 'No hay plazas disponibles'}, status=400)
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email requerido'}, status=400)

        session = self.get_object()
        try:
            reservation = Reservation.objects.get(session=session, email=email)
            reservation.delete()
            return Response({'detail': 'Reserva cancelada'}, status=200)
        except Reservation.DoesNotExist:
            return Response({'detail': 'No se encontró una reserva para ese email'}, status=404)