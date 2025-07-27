from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    #AREA LIVESTOCK 
    path('livestock/', views.livestock_list, name='livestock_list'),
    path('livestock/create/', views.livestock_create, name='livestock_create'),
    path('livestock/<int:pk>/edit/', views.livestock_update, name='livestock_update'),
    path('livestock/<int:pk>/delete/', views.livestock_delete, name='livestock_delete'),

    path('livestock/<int:pk>/', views.livestock_detail, name='livestock_detail'),


    #BREED
    path('breeds/', views.breed_list, name='breed_list'),
    path('breeds/create/', views.breed_create, name='breed_create'),
    path('breeds/<int:pk>/edit/', views.breed_edit, name='breed_edit'),
    path('breeds/<int:pk>/delete/', views.breed_delete, name='breed_delete'),

    #PARENTCHILD
    path('parentchild/', views.parentchild_list, name='parentchild_list'),
    path('parentchild/nuevo/', views.parentchild_create, name='parentchild_create'),


]
