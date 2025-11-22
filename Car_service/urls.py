from django.urls import path

from Car_service.views import (
    index,
    CarsListView,
    ManufacturerListView,
    ManufacturerCarsListView,
    SellerListView,
    CarDetailView,
    SellerDetailView,
    SellerCreateView,
    SellerDeleteView,
)



urlpatterns = [
    path("", index, name="index"),
    path("cars/", CarsListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("manufacturers/<int:pk>/", ManufacturerCarsListView.as_view(), name="manufacturer-cars"),
    path("sellers/", SellerListView.as_view(), name="seller-list"),
    path("sellers/<int:pk>/cars/", SellerDetailView.as_view(), name="seller-detail"),
    path("sellers/create/", SellerCreateView.as_view(), name="seller-create"),
    path("sellers/<int:pk>/delete/", SellerDeleteView.as_view(), name="seller-delete"),
]

app_name = "cars"
