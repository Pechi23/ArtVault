from django.urls import path
from .views import (GalleryListView, GalleryDetailView, 
                    GalleryCommentView, GalleryLikeView,
                    GalleryEditView, GalleryImageView,
                    GalleryDeleteView, GalleryImageDeleteView)

app_name = 'gallery'

urlpatterns = [
    path('', GalleryListView.as_view(), name='index'),
    path('gallery/create', GalleryListView.as_view(), name='create'),
    path('gallery/<slug:slug>', GalleryDetailView.as_view(), name='detail'),
    path('gallery/<slug:slug>/edit', GalleryEditView.as_view(), name='edit'),
    path('gallery/<slug:slug>/add-image', GalleryImageView.as_view(), name='add_image'),
    path('gallery/<slug:slug>/delete-image/<int:pk>', GalleryImageDeleteView.as_view(), name='delete_image'),
    path('gallery/<slug:slug>/delete', GalleryDeleteView.as_view(), name='delete'),
    path('gallery/<slug:slug>/like', GalleryLikeView.as_view(), name='like'),
    path('gallery/<slug:slug>/comment', GalleryCommentView.as_view(), name='comment'),
]