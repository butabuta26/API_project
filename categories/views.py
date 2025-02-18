from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Category, CategoryImage
from .serializers import CategoryDetailSerializer, CategoryImageSerializer, CategorySerializer

class CategoryListView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CategroryDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    
class CategoryImageViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(category__id=self.kwargs.get('category_id'))
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
