from django.urls import path
from .views import *

urlpatterns = [
    path('create_destinations/', TouristDestinationListCreateView.as_view(), name='destination_create'),
    path('detail_destinations/<int:pk>/', TouristDestinationDetailView.as_view(), name='destination_detail'),
    path('update_destinations/<int:pk>/', TouristDestinationUpdateView.as_view(), name='destination_update'),
    path('delete_destinations/<int:pk>/', TouristDestinationDeleteView.as_view(), name='destination_delete'),
    path('create_TouristDestination/', create_TouristDestination, name='create_destination'),
    path('TouristDestination_fetch/<int:id>/', TouristDestination_fetch, name='fetch_destination'),

    path('TouristDestination_update/<int:id>/', update_TouristDestination, name='update_destination'),
    path('TouristDestination_delete/<int:id>/', TouristDestination_delete, name='destination_delete'),
    path('', index, name='index'),
    path('update_detail_TouristDestination/<int:id>/', update_TouristDestination, name='update_detail_destination'),

]
