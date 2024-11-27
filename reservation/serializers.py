from rest_framework import serializers
from .models.reservation import Doctor, AvailableSlot, Appointment
from account.models import User


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ('id',)


class AvailableSlotSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = AvailableSlot
        exclude = ('id',)


class SlotSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        exclude = ('id', 'doctor')


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    doctor = DoctorSerializer()
    slot = SlotSummarySerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        slot = data['slot']
        if slot.is_booked:
            raise serializers.ValidationError("This slot is already booked.")
        return data

    def create(self, validated_data):
        slot = validated_data['slot']
        slot.is_booked = True
        slot.save()
        return super().create(validated_data)
