from reservation.models.reservation import Appointment
from django.shortcuts import get_object_or_404
from reservation.serializers import AppointmentSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from reservation.utility.pagination import StandardResultSetPagination
from reservation.utility.permissions import IsReadOnlyUser, IsDoctor, IsPatient


class UserAppointmentListView(APIView, StandardResultSetPagination):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        appointments = Appointment.objects.filter(patient=request.user).select_related('doctor', 'slot')
        result = self.paginate_queryset(appointments, request)
        serializer = AppointmentSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class AppointmentDetailView(APIView):
    permission_classes = (IsAuthenticated, IsReadOnlyUser)

    def get(self, request, patient_username):
        appointment = Appointment.objects.get(patient__username=patient_username)
        serializer = AppointmentSerializer(instance=appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelAppointmentView(APIView):
    permission_classes = (IsPatient,)

    def get(self, request, patient_username):
        appointment = get_object_or_404(Appointment, patient__username=patient_username)
        slot = appointment.slot
        slot.is_booked = False
        slot.save()
        appointment.delete()
        return Response({'message': 'Appointment canceled successfully'})
