from urllib import response
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from .models import *
from .serializers import TouristDestinationSerializer, UserSerializer
from rest_framework.permissions import AllowAny
import requests
from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth import login, logout, authenticate
from contextvars import Token
from tokenize import Token
from multiprocessing.managers import Token
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render # Import your user model

class TouristDestinationListCreateView(generics.ListCreateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializer
    permission_classes = [AllowAny]

class TouristDestinationDetailView(generics.RetrieveAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializer
    permission_classes = [AllowAny]

class TouristDestinationUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializer
    permission_classes = [AllowAny]

class TouristDestinationDeleteView(generics.DestroyAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializer
    permission_classes = [AllowAny]

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RegisterUserView(APIView):
    @method_decorator(csrf_exempt)  # Disable CSRF for this view
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_admin = request.data.get('is_admin', False)

        if not username or not email or not password:
            return requests.Response({'error': 'All fields are required'}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return requests.Response({'error': 'Username already exists'}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return requests.Response({'error': 'Email already exists'}, status=400)

        user = CustomUser(username=username, email=email, is_admin=is_admin)
        user.set_password(password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        return requests.Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=201)
 

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return requests.Response({'token': token.key, 'user': UserSerializer(user).data})
        return requests.Response({'error': 'Invalid credentials'}, status=400)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.auth.delete()
        return requests.Response({'message': 'Logged out successfully'})
    
@login_required
def create_TouristDestination(request):
    if request.method == 'POST':
        form = TouristDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save()  # Save the destination first
            # Handle multiple images
            tourist_images = request.FILES.getlist('tourist_img')
            for img in tourist_images:
                TouristImage.objects.create(destination=destination, image=img)

            messages.success(request, 'Destination and images added successfully')
            return redirect('index')  # Redirect to the index or another page
        else:
            messages.error(request, 'Form is invalid')
    else:
        form = TouristDestinationForm()
    return render(request, 'create_TouristDestination.html', {'form': form})

@login_required
def update_TouristDestination(request, id):
    destination = TouristDestination.objects.get(id=id)
    if request.method == 'POST':
        form = TouristDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()  # Save the destination first
            # Handle multiple images
            tourist_images = request.FILES.getlist('Tourist_img')
            for img in tourist_images:  
                TouristImage.objects.create(destination=destination, Tourist_img=img)
            messages.success(request, 'Destination updated successfully with images')
            return redirect('fetch_destination', id=id)
        else:
            messages.error(request, 'Form is invalid')
    else:
        form = TouristDestinationForm(instance=destination)
    return render(request, 'update_TouristDestination.html', {'form': form, 'tourist_destination': destination})


@login_required
def TouristDestination_delete(request, id):
    try:
        destination = TouristDestination.objects.get(id=id)
        destination.delete()
        messages.success(request, 'Destination deleted successfully')
    except TouristDestination.DoesNotExist:
        messages.error(request, 'Destination not found')
    return redirect('index')

@login_required
def TouristDestination_fetch(request, id):
    destination = TouristDestination.objects.get(id=id)
    images = TouristImage.objects.filter(destination=destination)
    return render(request, 'detail_TouristDestination.html', {'TouristDestination': destination, 'images': images})

@login_required
def index(request):
    if request.method == 'POST':
        search = request.POST['search']
        api_url = f'http://127.0.0.1:8000/search/{search}'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
            else:
                data = None
        except requests.RequestException as e:
            data = None
        return render(request, 'index.html', {'data': data})
    
    api_url = 'http://127.0.0.1:8000/create_destinations/'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            Original_data = data
            paginator = Paginator(Original_data, 2)
            page = int(request.GET.get('page', 0))

            try:
                TouristDestination = paginator.page(page)
            except EmptyPage:
                TouristDestination = paginator.page(paginator.num_pages)

            context = {
                'Original_data': Original_data,
                'TouristDestination': TouristDestination,
            }
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html', {'error_messages': f'Error: {response.status_code}'})
    except requests.RequestException as e:
        messages.error(request, f'ERROR during API request: {str(e)}')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def is_admin(user):
    return user.is_authenticated and user.is_admin  # Ensure user is an admin

@login_required
@user_passes_test(is_admin)
def destinations_table(request):
    """Display all destinations in a table format"""
    destinations = TouristDestination.objects.all()
   
    return render(request, 'destinations_table.html', {'destinations': destinations})

@login_required
@user_passes_test(is_admin)
def users_table(request):
    """Display all users in a table format"""
    users = CustomUser.objects.all()
    return render(request, 'users_table.html', {'users': users})

@login_required
def profile(request):
    """Render the user profile page"""
    user = request.user
    return render(request, 'profile.html', {'user': user})



@login_required
@user_passes_test(is_admin)

def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_destinations = TouristDestination.objects.count()  # Replace with actual destination count from your model
    pending_requests = Request.objects.count()  # Replace with actual pending requests count

    context = {
        'total_users': total_users,
        'total_destinations': total_destinations,
        'pending_requests': pending_requests,
    }
    return render(request, 'admin_dashboard.html', context)
