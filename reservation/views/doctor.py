from reservation.models.reservation import Doctor
from reservation.serializers import DoctorSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from reservation.utility.pagination import StandardResultSetPagination
from reservation.utility.permissions import IsReadOnlyUser


class DoctorListView(APIView, StandardResultSetPagination):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request):
        doctors = Doctor.objects.all()

        # filter
        name = request.query_params.get('name')
        if name:
            doctors = doctors.filter(name__icontains=name)

        result = self.paginate_queryset(doctors, request)
        serializer = DoctorSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class DoctorDetailView(APIView):
    permission_classes = (IsReadOnlyUser,)

    def get(self, request, name):
        doctor = get_object_or_404(Doctor, name=name)
        serializer = DoctorSerializer(instance=doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddDoctorView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def update(self, request, name):
        doctor = get_object_or_404(Doctor, name=name)
        serializer = DoctorSerializer(instance=doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        doctor = get_object_or_404(Doctor, name=name)
        doctor.delete()
        return Response({'message': 'doctor deleted'})
