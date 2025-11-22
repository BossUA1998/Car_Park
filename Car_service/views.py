from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.utils import IntegrityError

from Car_service.forms import SellerCreateForm
from Car_service.models import Car, Manufacturer, Seller


def index(request):
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_sellers = Seller.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cars': num_cars,
        'num_manufacturers': num_manufacturers,
        'num_sellers': num_sellers,
        'num_visits': num_visits,
    }

    return render(
        request,
        template_name="Car_service/index.html",
        context=context
    )


# cars
class CarsListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


# manufacturers
class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5


# sellers
class SellerListView(LoginRequiredMixin, generic.ListView):
    model = Seller
    paginate_by = 5

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["seller_user"] = Seller.objects.filter(client=self.request.user).exists()
        return context


class SellerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Seller


class SellerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Seller
    form_class = SellerCreateForm
    success_url = reverse_lazy("cars:seller-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            form.instance.client = self.request.user
        except IntegrityError:
            raise ValidationError("This manufacturer is already registered")
        return super().form_valid(form)


class SellerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Seller
    success_url = reverse_lazy("cars:seller-list")
