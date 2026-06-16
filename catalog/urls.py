from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/toggle_publish/', views.ProductTogglePublishView.as_view(), name='product_toggle_publish'),
    path('category/<int:category_id>/', views.ProductsByCategoryView.as_view(), name='products_by_category'),
    path('categories/', views.CategoriesListView.as_view(), name='categories_list'),
]