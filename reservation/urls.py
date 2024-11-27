from django.urls import path
from reservation.views import appointment, available_slot, doctor

app_name = 'reservation'

urlpatterns = [
    path('doctor/list', doctor.DoctorListView.as_view(), name='doctor-list'),
    path('doctor/detail/<str:name>', doctor.DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor/add', doctor.AddDoctorView.as_view(), name='doctor-add'),
    path('doctor/<str:name>', doctor.DoctorView.as_view(), name='doctor'),
    path('doctor/slot/<str:name>', available_slot.DoctorAvailableSlotView.as_view(), name='doctor-slot'),

    path('slot/list', available_slot.AvailableSlotListView.as_view(), name='slot-list'),
    path('slot/create', available_slot.CreateSlotView.as_view(), name='slot-create'),
    path('slot/delete/<int:pk>', available_slot.SlotDeleteView.as_view(), name='slot-delete'),
    path('slot/expired/delete', available_slot.RemoveExpiredSlotView.as_view(), name='slot-expired-delete'),

    path('appointment/user/list', appointment.UserAppointmentListView.as_view(), name='user-appointment-list'),
    path('appointment/detail/<str:patient_username>', appointment.AppointmentDetailView.as_view(),
         name='appointment-detail'),
    path('appointment/create', appointment.AppointmentCreateView.as_view(), name='appointment-create'),

]
