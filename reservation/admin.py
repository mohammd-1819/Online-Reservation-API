from django.contrib import admin
from .models import reservation


@admin.register(reservation.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality')


@admin.register(reservation.AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'time')


@admin.register(reservation.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'slot')