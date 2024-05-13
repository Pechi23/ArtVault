from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Gallery

class GalleryListView(ListView):
    model = Gallery
    template_name = 'galleries.html'
    context_object_name = 'galleries'
    paginate_by = 10

    def get_queryset(self):
        return Gallery.objects.all().order_by('-created_at')


class GalleryDetailView(LoginRequiredMixin ,DetailView):
    model = Gallery
    template_name = 'gallery.html'
    context_object_name = 'gallery'
    
    def get_object(self, slug):
        return Gallery.objects.get(slug=slug)
    
    def get(self, request, slug=None):
        self.object = self.get_object(slug)
        if self.request.user != self.object.user:
            self.object.views += 1
            self.object.save()
        context = self.get_context_data(object=self.object, slug=slug)
        
        return render(request, self.template_name, context=context)