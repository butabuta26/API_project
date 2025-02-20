from django.urls import path
from .views import CategoryListView, CategroryDetailView, CategoryImageViewSet

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categroies'),
    path('categories/<int:pk>/', CategroryDetailView.as_view(), name='categories'),
    path('categories/<int:category_id>/images/', CategoryImageViewSet.as_view(), name='categories'),
    path('categories/<int:category_id>/images/<int:pk>/', CategoryImageViewSet.as_view(), name='categories')
]
