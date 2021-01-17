from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField

# profile model
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='profiles/default.jpg', upload_to='profiles')

  def __str__(self):
    return self.user.username
  
  def save(self, *args, **kwargs):
    super().save()

    img = Image.open(self.image.path)
    
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.image.path)

# notes
class Note(models.Model):
  STATUS_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
  )
  title = models.CharField(max_length=120)
  body = RichTextUploadingField()
  attatchment = models.FileField(upload_to='attatchment/', blank=True, null=True)
  date_posted = models.DateTimeField(auto_now_add=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='private')
  tags = TaggableManager()
  slug = models.SlugField(max_length=250, unique=True)
  favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

  class Meta:
    ordering = ('-date_posted', )

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    reverse('notes:note_detail', args=[self.slug])

  def favourites(self):
    return [user for user in self.favourite.all()]

def slug_generator(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Note)