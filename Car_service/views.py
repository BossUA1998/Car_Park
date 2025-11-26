from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.utils import IntegrityError

from Car_service.forms import (
    SellerLicenseForm,
    CarCreateForm,
    CarSearchForm,
    ManufacturerSearchForm,
    SellerSearchForm,
)
from Car_service.models import Car, Manufacturer, Seller


def index(request):
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_sellers = Seller.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_sellers": num_sellers,
        "num_visits": num_visits,
    }

    return render(request, template_name="Car_service/index.html", context=context)


# cars
class CarsObjectValidatorMixin:
    def form_valid(self, form):
        if not self.request.user == self.object.owner.client:
            raise PermissionDenied
        return super().form_valid(form)


class CarsListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        _model = self.request.GET.get("model")
        context["search_form"] = CarSearchForm(initial={"model": _model})
        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)
        self.queryset = Car.objects.select_related("manufacturer", "owner").all()
        if form.is_valid():
            return self.queryset.filter(model__icontains=form.cleaned_data["model"])
        return self.queryset


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = Seller.objects.get(client=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cars:car-detail", kwargs={"pk": self.object.pk})


class CarUpdateView(LoginRequiredMixin, CarsObjectValidatorMixin, generic.UpdateView):
    model = Car
    fields = ["model", "year", "mileage", "price", "comment", "manufacturer"]

    def get_success_url(self):
        return reverse_lazy("cars:car-detail", kwargs={"pk": self.object.pk})


class CarDeleteView(LoginRequiredMixin, CarsObjectValidatorMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("cars:car-list")


# manufacturers
class ImportantSuperuserValidatorMixin:
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return super().form_valid(form)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        _name = self.request.GET.get("name")
        context["search_form"] = ManufacturerSearchForm(initial={"name": _name})
        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)
        self.queryset = Manufacturer.objects.all()
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class ManufacturerCarsListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5
    context_object_name = "manufacturer_cars"
    template_name = "Car_service/manufacturer_cars.html"

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context["manufacturer"] = Manufacturer.objects.get(pk=self.kwargs["pk"])

        _model = self.request.GET.get("model")
        context["search_form"] = CarSearchForm(initial={"model": _model})
        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)
        self.queryset = Manufacturer.objects.get(pk=self.kwargs["pk"]).cars.all()
        if form.is_valid():
            self.queryset = self.queryset.filter(
                model__icontains=form.cleaned_data["model"]
            )
        return self.queryset


class ManufacturerCreateView(
    LoginRequiredMixin, ImportantSuperuserValidatorMixin, generic.CreateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("cars:manufacturer-list")


class ManufacturerUpdateView(
    LoginRequiredMixin, ImportantSuperuserValidatorMixin, generic.UpdateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("cars:manufacturer-list")


class ManufacturerDeleteView(
    LoginRequiredMixin, ImportantSuperuserValidatorMixin, generic.DeleteView
):
    model = Manufacturer
    success_url = reverse_lazy("cars:manufacturer-list")


# sellers
class SellerObjectValidatorMixin:
    def form_valid(self, form):
        if not self.request.user == self.object.client:
            raise PermissionDenied
        return super().form_valid(form)


class SellerListView(LoginRequiredMixin, generic.ListView):
    model = Seller
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller_user"] = Seller.objects.filter(
            client=self.request.user
        ).exists()
        try:
            context["seller"] = Seller.objects.get(client=self.request.user)
        except Seller.DoesNotExist:
            context["seller"] = None
        _username = self.request.GET.get("username")
        context["search_form"] = SellerSearchForm(initial={"username": _username})
        return context

    def get_queryset(self):
        form = SellerSearchForm(self.request.GET)
        self.queryset = Seller.objects.all()
        if form.is_valid():
            self.queryset = Seller.objects.filter(
                client__username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class SellerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Seller


class SellerFormMixin:
    def form_valid(self, form):
        self.request.user.is_seller = True
        self.request.user.save()
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cars:seller-detail", kwargs={"pk": self.object.pk})


class SellerCreateView(LoginRequiredMixin, SellerFormMixin, generic.CreateView):
    model = Seller
    form_class = SellerLicenseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("cars:seller-detail", kwargs={"pk": self.object.pk})


class SellerUpdateView(
    LoginRequiredMixin, SellerObjectValidatorMixin, SellerFormMixin, generic.UpdateView
):
    model = Seller
    form_class = SellerLicenseForm


class SellerDeleteView(
    LoginRequiredMixin, SellerObjectValidatorMixin, generic.DeleteView
):
    model = Seller
    success_url = reverse_lazy("cars:seller-list")

    def post(self, request, *args, **kwargs):
        request.user.is_seller = False
        request.user.save()
        return super().post(request, *args, **kwargs)
