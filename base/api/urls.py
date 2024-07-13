from django.urls import path
from .views import *


urlpatterns = [ 
    path('', getRoutes),
    path('rooms/', getRooms),
    path('roomsz/<str:pk>/', getRoom),

]
