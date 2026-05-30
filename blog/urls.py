from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='list'),
    path('<int:pk>/', views.BlogPostDetailView.as_view(), name='detail'),
    path('create/', views.BlogPostCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='delete'),
]