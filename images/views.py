from rest_framework import viewsets

from images.serializers import ImageSerializer
from images.models import Image


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
