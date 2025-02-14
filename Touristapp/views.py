from rest_framework import generics
from .models import TouristDestination, TouristImage
from .serializers import TouristDestinationSerializer
from rest_framework.permissions import AllowAny
import requests
from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage

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

def create_TouristDestination(request):
    if request.method == 'POST':
        form = TouristDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save()  # Save the destination first
            # Handle multiple images
            tourist_images = request.FILES.getlist('tourist_img')
            for img in tourist_images:
                TouristImage.objects.create(destination=destination, Tourist_img=img)
            messages.success(request, 'Destination and images added successfully')
            return redirect('index')  # Redirect to the index or another page
        else:
            messages.error(request, 'Form is invalid')
    else:
        form = TouristDestinationForm()
    return render(request, 'create_TouristDestination.html', {'form': form})

def update_TouristDestination(request, id):
    destination = TouristDestination.objects.get(id=id)
    if request.method == 'POST':
        form = TouristDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()  # Save the destination first
            # Handle multiple images
            tourist_images = request.FILES.getlist('tourist_img')
            for img in tourist_images:
                TouristImage.objects.create(destination=destination, Tourist_img=img)
            messages.success(request, 'Destination updated successfully with images')
            return redirect('fetch_destination', id=id)
        else:
            messages.error(request, 'Form is invalid')
    else:
        form = TouristDestinationForm(instance=destination)
    return render(request, 'update_TouristDestination.html', {'form': form, 'tourist_destination': destination})

def TouristDestination_delete(request, id):
    try:
        destination = TouristDestination.objects.get(id=id)
        destination.delete()
        messages.success(request, 'Destination deleted successfully')
    except TouristDestination.DoesNotExist:
        messages.error(request, 'Destination not found')
    return redirect('index')

def TouristDestination_fetch(request, id):
    destination = TouristDestination.objects.get(id=id)
    images = TouristImage.objects.filter(destination=destination)
    return render(request, 'detail_TouristDestination.html', {'TouristDestination': destination, 'images': images})

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
