from django.urls import path
from .views import GalleryListView, GalleryDetailView

urlpatterns = [
    path('', GalleryListView.as_view(), name='index'),
    path('gallery/<slug:slug>', GalleryDetailView.as_view(), name='gallery'),
]