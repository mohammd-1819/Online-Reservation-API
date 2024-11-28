import django_filters
from reservation.models.reservation import Doctor


class DoctorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Doctor
        fields = ['name']
