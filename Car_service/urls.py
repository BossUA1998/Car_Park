from django.urls import path

from Car_service.views import (
    index,

    CarsListView,
    CarCreateView,
    CarDetailView,

    ManufacturerListView,
    ManufacturerCarsListView,

    SellerListView,
    SellerDetailView,
    SellerCreateView,
    SellerDeleteView,
)



urlpatterns = [
    # home page
    path("", index, name="index"),

    # cars
    path("cars/", CarsListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),

    # manufacturers
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("manufacturers/<int:pk>/", ManufacturerCarsListView.as_view(), name="manufacturer-cars"),

    # sellers
    path("sellers/", SellerListView.as_view(), name="seller-list"),
    path("sellers/<int:pk>/cars/", SellerDetailView.as_view(), name="seller-detail"),
    path("sellers/create/", SellerCreateView.as_view(), name="seller-create"),
    path("sellers/<int:pk>/delete/", SellerDeleteView.as_view(), name="seller-delete"),
]

app_name = "cars"
