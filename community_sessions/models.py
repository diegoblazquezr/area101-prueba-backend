from django.db import models
from django.core.cache import cache

class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    @property
    def available_slots(self):
        cache_key = f"available_slots_session_{self.id}"
        slots = cache.get(cache_key)

        if slots is None:
            slots = self.capacity - self.reservations.count()
            # Guardo en caché durante 20 segundos y evito hacer una query extra cada vez que quiero hacer count()
            cache.set(cache_key, slots, timeout=20)

        return slots
        # return self.capacity - self.reservations.count()

class Reservation(models.Model):
    session = models.ForeignKey(Session, related_name='reservations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'email')  # Para que no se dupliquen reservas

    def __str__(self):
        return f'{self.name} - {self.session.title}'
