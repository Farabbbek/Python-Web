from django.urls import path 
from authapp import views

urlpatterns = [
    path('',views.Home, name='Home'),  # Home page
    path('register',views.register, name="register"),  # register page
    path('login',views.handlelogin, name="login"),  # Login page
    path('logout',views.handleLogout, name="handleLogout"),  # Logout page
    path('contact',views.contact, name="contact"),  # Contact page
    path('profile',views.profile, name="profile"),  # Profile page
    path('notes/', views.food_log_list, name='food_log_list'),
    path('notes/create/', views.food_log_create, name='food_log_create'),
    path('notes/<int:pk>/edit/', views.food_log_edit, name='food_log_edit'),
    path('notes/<int:pk>/delete/', views.food_log_delete, name='food_log_delete'),
    path('sets/', views.workout_set_list, name='workout_set_list'),
    path('sets/create/', views.workout_set_create, name='workout_set_create'),
    path('sets/edit/<int:pk>/', views.workout_set_edit, name='workout_set_edit'),
    path('sets/delete/<int:pk>/', views.workout_set_delete, name='workout_set_delete'),
    path('progress/',views.exercise_progress, name='exercise_progress'),  # Progress page
    path('about',views.about, name='about'),  # About page
    path('coach',views.coach, name='coach'),  # Cauch page
    path('password-reset/', views.password_reset, name='password_reset'),
]
