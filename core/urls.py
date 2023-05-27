from django.urls import path

from .views import ( 
    TankListCreateView, 
    TankRetrieveUpdateDestroyView,
    TankVolumeListCreateView,
    TankVolumeRetrieveUpdateDestroyView,
    TankSalesListView,
    TankSalesRetrieveView,
    AverageTankSalesListView,
    AverageTankSalesRetrieveView,
)

urlpatterns = [
    path('tanks/', TankListCreateView.as_view()),
    path('tanks/<int:pk>/', TankRetrieveUpdateDestroyView.as_view()),

    path('volumes/', TankVolumeListCreateView.as_view()),
    path('volumes/<int:pk>/', TankVolumeRetrieveUpdateDestroyView.as_view()),

    path('tank-sales/', TankSalesListView.as_view()),
    path('tank-sales/<int:pk>/', TankSalesRetrieveView.as_view()),

    path('avg-tank-sales/', AverageTankSalesListView.as_view()),
    path('avg-tank-sales/<int:pk>/', AverageTankSalesRetrieveView.as_view()),
]
