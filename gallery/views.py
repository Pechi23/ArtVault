from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Gallery, Image, Comment, Like, Follow
from .forms import GalleryForm # type: ignore
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse

class GalleryListView(ListView):
    model = Gallery
    template_name = 'galleries.html'
    context_object_name = 'galleries'
    paginate_by = 10

    def get_queryset(self):
        return Gallery.objects.all().order_by('-created_at')
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('auth_signin')
        gallery = Gallery.objects.create(user=request.user, title=request.POST.get('title'), description=request.POST.get('description'), cover=request.FILES.get('cover'))
        return redirect('gallery:detail', slug=gallery.slug)


class GalleryDetailView(LoginRequiredMixin ,DetailView):
    model = Gallery
    template_name = 'gallery.html'
    context_object_name = 'gallery'
    
    def get_object(self, slug):
        return get_object_or_404(Gallery, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['likes'] = self.object.likes.all()
        context['images'] = self.object.images.all()
        context['is_liked'] = self.object.likes.filter(user=self.request.user).exists()
        return context
    
    def get(self, request, slug=None):
        if slug is None:
            return redirect('gallery:index')
        self.object = self.get_object(slug)
        if self.request.user != self.object.user:
            self.object.views += 1
            self.object.save()
        context = self.get_context_data(object=self.object, slug=slug)
        
        return render(request, self.template_name, context=context)
    
    def post(self, request, slug=None):
        self.object = self.get_object(slug)
        if request.POST.get('like'):
            self.object.likes.create(user=request.user)
        elif request.POST.get('comment'):
            self.object.comments.create(user=request.user, comment=request.POST.get('comment'))
        context = self.get_context_data(object=self.object, slug=slug)
        
        return render(request, self.template_name, context=context)
    
class GalleryEditView(LoginRequiredMixin, FormView):
    model = Gallery
    template_name = 'edit.html'
    form_class = GalleryForm
    
    def get(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        context = {
            'gallery': gallery,
            'form': self.form_class(instance=gallery)
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        form = self.form_class(request.POST, request.FILES, instance=gallery)
        
        if form.is_valid():
            gallery.save()
            return redirect('gallery:detail', slug=gallery.slug)
        
        context = {
            'gallery': gallery,
            'form': self.form_class(instance=gallery)
        }
        return render(request, self.template_name, context=context)
    
class GalleryImageDeleteView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'delete-image.html'
    
    def get(self, request, slug=None, pk=None):
        if request.user != Gallery.objects.get(slug=slug).user:
            return HttpResponseForbidden("You are not allowed to delete this image.")
        
        gallery = Gallery.objects.get(slug=slug)
        image = gallery.images.get(pk=pk)
        context = {
            'gallery': gallery,
            'image': image
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, slug=None, pk=None):
        gallery = Gallery.objects.get(slug=slug)
        image = gallery.images.get(pk=pk)
        image.delete()
        return redirect('gallery:detail', slug=slug)
    
class GalleryImageView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'partials/add-image.html'
    
    def post(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        gallery.save()
        image = gallery.images.create(image=request.FILES.get('image'))
        return render(request, self.template_name, context={'image': image})
        
    
class GalleryDeleteView(LoginRequiredMixin, DetailView):
    model = Gallery
    template_name = 'delete.html'
    
    def get(self, request, slug=None):
        if request.user != Gallery.objects.get(slug=slug).user:
            return HttpResponseForbidden("You are not allowed to delete this gallery.")
        
        gallery = Gallery.objects.get(slug=slug)
        context = {
            'gallery': gallery
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        gallery.delete()
        return redirect('gallery:index')
    
class GalleryCommentView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'partials/comment.html'
    
    def post(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        comment = gallery.comments.create(user=request.user, comment=request.POST.get('comment'))
        return render(request, self.template_name, context={'comment': comment})
    
    def delete(self, request, slug=None, pk=None):
        gallery = Gallery.objects.get(slug=slug)
        comment = gallery.comments.get(pk=pk)
        comment.delete()
        return HttpResponse('Comment deleted.')
    
class GalleryLikeView(LoginRequiredMixin, DetailView):
    model = Like
    template_name = 'partials/like.html'
    
    def post(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        gallery.likes.create(user=request.user)
        context = {
            'gallery': gallery,
            'message': 'liked'
        }
            
        return render(request, self.template_name, context=context)
    
    def delete(self, request, slug=None):
        gallery = Gallery.objects.get(slug=slug)
        gallery.likes.filter(user=request.user).delete()
        context = {
            'gallery': gallery,
            'message': 'unliked'
        }
        return render(request, self.template_name, context=context)