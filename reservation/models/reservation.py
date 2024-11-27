from django.db import models

from account.models import User


class Doctor(models.Model):
    name = models.CharField(max_length=60)
    speciality = models.CharField(max_length=80)
    info = models.CharField(max_length=130)
    work_time = models.DateTimeField()

    def __str__(self):
        return f'Dr.{self.name}'


class AvailableSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='available_slot')
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'slot for Dr.{self.doctor.name}'


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment')
    slot = models.OneToOneField(AvailableSlot, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'appointment for {self.patient.username} with {self.doctor.name}'
