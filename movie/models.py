from django.db import models
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    STATUS_CHOICES = [
        ('now_showing', 'Now Showing'),
        ('coming_soon', 'Coming Soon'),
        ('archived', 'Archived'),
    ]

    AGE_RATINGS = [
        ('G', 'General'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'PG-13'),
        ('R', 'Restricted'),
        ('18+', 'Adults Only'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    age_rating = models.CharField(max_length=10, choices=AGE_RATINGS, default='PG')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='coming_soon')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
