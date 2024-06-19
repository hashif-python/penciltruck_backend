import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import status
from penciltruckapp.serializers import GallerySerializer
from penciltruckadmin.models import Banner, Gallery


class GalleryData(APIView):
    
    def get(self, request):
        try:
            obj=Gallery.objects.filter(active=True)
            serializer = GallerySerializer(obj, many=True)
            res = serializer.data
            return Response({'data': res}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
