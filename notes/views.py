from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, NoteCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .models import Note
from django.utils.html import escape
from django.contrib.auth.models import User

# /
@login_required
def home(request):
  notes = Note.objects.filter(status='public')

  return render(request, 'notes/index.html', {
    'notes': notes,
    'title': 'All Public Notes'
  })

# /dashboard/
@login_required
def dashboard(request):
  public_notes = Note.objects.filter(author=request.user, status='public')
  private_notes = Note.objects.filter(author=request.user, status='private')

  return render(request, 'notes/dashboard.html', {
    'public_notes': public_notes,
    'private_notes': private_notes
  })

# /search/
@login_required
def search(request):
  notes = []
  if request.method == 'GET':
    search_word = request.GET.get('search')
    if search_word:
      search_word = escape(search_word).lower()

      notes = Note.objects.filter(status='public').filter(body__icontains=search_word).order_by('-date_posted') or Note.objects.filter(status='public').filter(title__icontains=search_word).order_by('-date_posted') or Note.objects.filter(status='public').filter(tags__name__in=[search_word]).distinct().order_by('-date_posted')
  return render(request, 'notes/index.html', {
    'notes': notes,
    'title': 'Search Results'
  })

# /delete/<slug:slug>/
@login_required
def delete(request, slug):
  if request.method == 'POST' and slug:
    note = Note.objects.filter(slug=slug).first()
    if note:
      # check if request.user == note.author are same
      if note.author == request.user:
        note.delete()
        messages.success(request, 'Successfully deleted the note!')

  return redirect('notes:home')

# /edit/<slug:slug>/
def edit(request, slug):
  note = Note.objects.filter(slug=slug).first()
  # check if request.user == note.author are same
  if note and note.author == request.user:
    # if it is a GET request
    if request.method == 'GET' and slug:
      form = NoteCreationForm(initial={
        'title': note.title,
        'body': note.body,
        'status': note.status,
        'tags': note.tags.all()
      })
      return render(request, 'notes/edit.html', {
        'form': form
      })
    elif request.method == 'POST':
      form = NoteCreationForm(data=request.POST, instance=note)
      if form.is_valid():
        form.save()
        messages.success(request, 'Note has been updated successfully!')

  return redirect('notes:home')

# /profile/
@login_required
def profile(request):
  if request.method == 'POST':
    user_form = UserUpdateForm(request.POST, instance=request.user)
    profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Your account has been updated successfully!')
      return redirect('notes:profile')
  else:
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
  
  return render(request, 'notes/profile.html', {
    'user_form': user_form,
    'profile_form': profile_form
  })

# /user/<str:username>/
@login_required
def user_notes(request, username):
  notes = []
  user = User.objects.filter(username=username).first()

  if user:
    notes = Note.objects.filter(status='public', author=user)
  return render(request, 'notes/index.html', {
    'notes': notes,
    'title': f'{user.username}\'s Notes'
  })

# /tag/<slug:slug>/
@login_required
def tag(request, slug):
  notes = []
  tag = slug
  if request.method == 'GET':
    if tag:
      tag = escape(tag).lower()

      notes = Note.objects.filter(status='public').filter(tags__name__in=[tag]).distinct().order_by('-date_posted') 
  return render(request, 'notes/index.html', {
    'notes': notes,
    'title': f'Tag: #{tag}'
  })

# /add/
@login_required
def add(request):
  if request.method == 'POST':
    form = NoteCreationForm(data=request.POST)
    if form.is_valid():
      instance = form.save(commit=False)
      tags = form.cleaned_data['tags']
      instance.author = request.user
      instance.save()
      for tag in tags:
        instance.tags.add(tag)
      messages.success(request, f'Your Note has been added!')
      return redirect('notes:home')
    else:
      messages.error(request, f'Oops, some error happened, Try Again!')
  else:
    form = NoteCreationForm()
  return render(request, 'notes/add.html', {
    'form': form
  })

# /note/<slug:slug>/
def note_detail(request, slug):
  note = get_object_or_404(Note, slug=slug)

  """ if note is private, then the user who added it can only see it """
  if note.status == 'private':
    if not (note.author == request.user):

      return redirect('notes:home')
  
  return render(request, 'notes/detail.html', {
    'note': note
  })

# /login/
def login_view(request):
  next_url = request.GET.get('next')

  if request.user.is_authenticated:
    return redirect('notes:home')

  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect(next_url) if next_url else redirect('notes:home')
  else:
    form = AuthenticationForm()
  return render(request, 'notes/login.html', {
    'form': form
  })

# /signup/
def signup(request):
  if request.user.is_authenticated:
    return redirect('notes:home')
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, f'Your Account created successfully!')
      return redirect('login')
  else:
    form = UserRegisterForm()
  return render(request, 'notes/signup.html', {
    'form': form
  })

# /logout/
def logout_view(request):
  logout(request)
  return redirect('login')