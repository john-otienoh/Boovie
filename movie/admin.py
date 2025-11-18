from django.contrib import admin
from .models import Movie, Genre

# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name',]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "release_date", "duration", "language", "age_rating"]
    list_filter = ["status", "language", "age_rating", "genre"]
    search_fields = ["title", "language", "description"]
    ordering = ["-created_at"]

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Movie Details", {
            "fields": ("title", "slug", "description", "genre", "poster_image")
        }),
        ("Metadata", {
            "fields": ("duration", "release_date", "language", "age_rating", "status")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    show_facets = admin.ShowFacets.ALWAYS
