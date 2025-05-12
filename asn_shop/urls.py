from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home_page, name='home'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('add_car/', views.add_car, name='add_car'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
