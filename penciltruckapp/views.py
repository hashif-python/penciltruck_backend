from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import status



class Banners(APIView):
    
    def get(self, request):
        try:

            res={'services':['Ordering','Enquiry','Quotation']}
            return Response({'data': res}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
