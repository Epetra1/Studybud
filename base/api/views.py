from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import rooms
from .serializers import *

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)
@api_view(['GET'])
def getRooms(request):
    room = rooms.objects.all()
    serializers = RoomSerializers(room, many = True) 


    return Response(serializers.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = rooms.objects.get(id = pk)
    serializers = RoomSerializers(room, many = False) 
    return Response(serializers.data)
