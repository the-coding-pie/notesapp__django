from django.contrib import admin
from .models import Note, Profile

# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
  list_display = ('title', 'date_posted', 'status')
  ordering = ['-date_posted']

admin.site.register(Profile)