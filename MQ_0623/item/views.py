from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ItemModelSerializer
from .models import Category

# Create your views here.

class ItemView(APIView):
    def get(self, request):
        category = request.GET.get('category', None)
        
        items = Category.objects.prefetch_related('item_set').get(name=category).item_set.all()
        
        if items.exists:
            
        
        item_serializer = ItemModelSerializer()
        
        return Response(item_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response()