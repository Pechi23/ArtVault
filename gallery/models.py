from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gallery(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover = models.ImageField(upload_to='static/images/')
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = self.title.lower().replace(' ', '-')
        super(Gallery, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Image(TimeStamp):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, 
                                related_name='images',
                                null=True, blank=True)
    image = models.ImageField(upload_to='static/images/')

    def __str__(self):
        return str(self.image)

class Comment(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        return self.comment
    

class Like(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user.username} likes {self.gallery.title}'
    
    
class Follow(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.user.username} follows {self.followed.username}'
    