from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('signup/', views.signup, name='signup'),
  path('home/', views.home, name='home'),
  path('note/fav/', views.favourite, name='favourite'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('profile/', views.profile, name='profile'),
  path('favourites/', views.favourites, name='favourites'),
  path('add/', views.add, name='add'),
  path('note/<slug:slug>/', views.note_detail, name='note_detail'),
  path('search/', views.search, name='search'),
  path('delete/<slug:slug>/', views.delete, name='delete'),
  path('edit/<slug:slug>/', views.edit, name='edit'),
  path('user/<str:username>/', views.user_notes, name='user_notes'),
  path('tag/<slug:slug>/', views.tag, name='tag'),
]