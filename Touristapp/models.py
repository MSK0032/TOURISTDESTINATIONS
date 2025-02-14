from django.db import models

class TouristDestination(models.Model):
    place_name = models.CharField(max_length=255)
    tourist_img = models.ImageField(upload_to='places/', blank=True, null=True)
    weather = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_district = models.CharField(max_length=100)
    google_map_link = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.place_name

class TouristImage(models.Model):
    destination = models.ForeignKey(TouristDestination, related_name='images', on_delete=models.CASCADE)
    place_name = models.CharField(max_length=255)
    Tourist_img = models.ImageField(upload_to='more_images/')
