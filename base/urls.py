from django.urls import path
from .views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('', home,name = 'home'),
    path('room/<str:pk>/', room, name = 'room'),
    path('room_create/', room_create, name = 'room_create'),
    path('room_update/<str:pk>', room_update, name = 'room_update'),
    path('room_delete/<str:pk>', room_delete, name = 'room_delete'),
    path('message_delete/<str:pk>', delete_message, name = 'message_delete'),
    path('login/', login_page, name = 'login_page'),
    path('register/', register_user, name = 'register_page'),
    path('logout/', logout_user, name = 'logout_page'),
    path('profile/<str:pk>', profile, name = 'profile'),
    path('edit_user', edit_user, name = 'edit_user'),
    path('topics', topics, name = 'topics'),
    path('activity', activity, name = 'activity'),
    path('delete_message/<str:pk>', delete_message, name = 'delete_message')
    
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)