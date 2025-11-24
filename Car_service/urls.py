from django.urls import path

from Car_service.views import (
    index,

    CarsListView,
    CarCreateView,
    CarDetailView,
    CarUpdateView,
    CarDeleteView,

    ManufacturerListView,
    ManufacturerCarsListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,

    SellerListView,
    SellerDetailView,
    SellerCreateView,
    SellerUpdateView,
    SellerDeleteView,
)



urlpatterns = [
    # home page
    path("", index, name="index"),

    # cars
    path("cars/", CarsListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),

    # manufacturers
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("manufacturers/<int:pk>/", ManufacturerCarsListView.as_view(), name="manufacturer-cars"),
    path("manufacturers/create/", ManufacturerCreateView.as_view(), name="manufacturer-create"),
    path("manufacturers/<int:pk>/update/", ManufacturerUpdateView.as_view(), name="manufacturer-update"),
    path("manufacturers/<int:pk>/delete/", ManufacturerDeleteView.as_view(), name="manufacturer-delete"),

    # sellers
    path("sellers/", SellerListView.as_view(), name="seller-list"),
    path("sellers/<int:pk>/", SellerDetailView.as_view(), name="seller-detail"),
    path("sellers/create/", SellerCreateView.as_view(), name="seller-create"),
    path("sellers/<int:pk>/update/", SellerUpdateView.as_view(), name="seller-update"),
    path("sellers/<int:pk>/delete/", SellerDeleteView.as_view(), name="seller-delete"),
]

app_name = "cars"
