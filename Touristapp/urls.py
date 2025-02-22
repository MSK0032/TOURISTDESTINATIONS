from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('api/register/', RegisterUserView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('create_destinations/', TouristDestinationListCreateView.as_view(), name='destination_create'),
    path('detail_destinations/<int:pk>/', TouristDestinationDetailView.as_view(), name='destination_detail'),
    path('update_destinations/<int:pk>/', TouristDestinationUpdateView.as_view(), name='destination_update'),
    path('delete_destinations/<int:pk>/', TouristDestinationDeleteView.as_view(), name='destination_delete'),
    path('create_TouristDestination/', create_TouristDestination, name='create_destination'),
    path('TouristDestination_fetch/<int:id>/', TouristDestination_fetch, name='fetch_destination'),
    path('TouristDestination_update/<int:id>/', update_TouristDestination, name='update_destination'),
    path('TouristDestination_delete/<int:id>/', TouristDestination_delete, name='destination_delete'),
    path('index/', index, name='index'),

    path('profile/', profile, name='profile'),
   

    path('destinations_table/', destinations_table, name='destinations_table'),
    path('users_table/', users_table, name='users_table'),


]
