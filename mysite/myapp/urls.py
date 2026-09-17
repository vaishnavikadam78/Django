from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import(TokenObtainPairView,TokenRefreshView)


app_name = 'myapp'
router = DefaultRouter()
router.register(r"items", views.ItemViewSet, basename='item')
router = DefaultRouter()
router.register(r"orders", views.OrderViewSet, basename='order')

urlpatterns = [
     path("api/token/",TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path("api/token/refresh/",TokenRefreshView.as_view(),name='token_refresh_view'),
    path("api/", include(router.urls)),
    # --- API Endpoints ---
    # path('api/items.json/', views.item_list_json, name='item_list_json'),
    # path('items/api/', views.item_list_api, name='item-list-api'),
    # path('api/items/<int:pk>/', views.item_detail_api, name='item-detail-api'),
    # URL pattern of API built with DRF
# path('api/items/', views.ItemListCreateAPI.as_view(), name='item-list-api'),

# # URL pattern for single item
# path('api/items/<int:pk>/', views.ItemRetrieveUpdateDestroyAPIView.as_view(), name='item-detail-api'),



    # --- Standard Web App Views ---
    path('', views.index, name='index'),
    path('item/', views.item, name='item'),
    path('<int:id>/', views.detail, name='detail'),
    path('add/', views.create_item, name='create_item'),
    path('update/<int:pk>/', views.ItemUpdateView.as_view(), name='update_item'),
    path('delete/<int:pk>/', views.ItemDeleteView.as_view(), name='delete_item'),
]

