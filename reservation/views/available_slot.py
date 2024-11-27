from datetime import datetime

from reservation.models.reservation import AvailableSlot
from reservation.serializers import AvailableSlotSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from reservation.utility.pagination import StandardResultSetPagination
from reservation.utility.permissions import IsReadOnlyUser


class AvailableSlotListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        slots = AvailableSlot.objects.all()
        result = self.paginate_queryset(slots, request)
        serializer = AvailableSlotSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class DoctorAvailableSlotView(APIView):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request, name):
        slots = AvailableSlot.objects.filter(doctor__name=name, is_booked=False).select_related('doctor')
        serializer = AvailableSlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateSlotView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        serializer = AvailableSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        slot = get_object_or_404(AvailableSlot, id=pk)
        slot.delete()
        return Response({'message': 'slot deleted'})


class RemoveExpiredSlotView(APIView):
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get(self, request):
        slots = AvailableSlot.objects.all()
        current_date = datetime.now().date()
        for slot in slots:
            if slot.date < current_date:
                slot.delete()
        return Response({"message": 'expired slots deleted'})
