from django.db import models

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
        return self.capacity - self.reservations.count()

class Reservation(models.Model):
    session = models.ForeignKey(Session, related_name='reservations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'email')  # Para que no se dupliquen reservas

    def __str__(self):
        return f'{self.name} - {self.session.title}'
