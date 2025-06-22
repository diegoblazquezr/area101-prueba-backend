from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, F
from .models import Session, Reservation
from .serializers import SessionSerializer, ReservationSerializer
from django.core.cache import cache

class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Session.objects.all().annotate(res_count=Count('reservations'))
    # Con prefetch_related evito una consulta por sesión cuando hago session.reservations.all() (o .count()).
    # queryset = Session.objects.all() \
	# 	.annotate(res_count=Count('reservations')) \
	# 	.prefetch_related('reservations')
    
    serializer_class = SessionSerializer

    # def get_queryset(self):
    #     return self.queryset.filter(res_count__lt=F('capacity'))
    # def get_queryset(self):
    #     return Session.objects.annotate(
    #         res_count=Count('reservations')
    #     ).prefetch_related('reservations').filter(
    #         res_count__lt=F('capacity')
    #     )
    def get_queryset(self):
        qs = Session.objects.annotate(
            res_count=Count('reservations')
        ).prefetch_related('reservations')

        if self.action == 'list':
            # Solo filtra si veo el listado
            qs = qs.filter(res_count__lt=F('capacity'))

        return qs
    
    def retrieve(self, request, *args, **kwargs):
        session_id = kwargs['pk']
        cache_key = f"session_{session_id}_data"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # Si no hay en caché, seguimos como siempre y luego lo guardamos
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=10)  # puedes ajustar el timeout
        return response

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        session = self.get_object()
        if session.available_slots <= 0:
            return Response({'detail': 'No hay plazas disponibles'}, status=400)
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            # Limpio el caché justo antes de guardar reserva
            cache.delete(f"available_slots_session_{session.id}")
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
            # No me hace falta select_related ahí, pero si tuviera muchas reservas en una lista, sería útil hacer:
            # Reservation.objects.select_related('session')
            reservation.delete()
            # Limpio el caché justo antes de eliminar reserva
            cache.delete(f"available_slots_session_{session.id}")
            return Response({'detail': 'Reserva cancelada'}, status=200)
        except Reservation.DoesNotExist:
            return Response({'detail': 'No se encontró una reserva para ese email'}, status=404)