from rest_framework.serializers import ModelSerializer
from base.models import rooms

class RoomSerializers(ModelSerializer):
    class Meta:
        model = rooms
        fields = '__all__'