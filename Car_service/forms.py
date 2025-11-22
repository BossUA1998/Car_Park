from django import forms
from django.core.exceptions import ValidationError

from Car_service.models import Seller


class SellerCreateForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ["seller_license", "license_expiration_date"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_seller_license(self):
        license_value = self.cleaned_data.get("seller_license")
        if license_value:
            if len(license_value) != 8:
                raise ValidationError("License must be 8 characters long")
            elif not license_value[:3].isalpha():
                raise ValidationError("License must start with a letter")
            elif not license_value[:3].isupper():
                raise ValidationError("License must start with uppercase")
            elif not license_value[3:].isdigit():
                raise ValidationError("License must contain with digit")

            qs_license = Seller.objects.filter(seller_license=license_value)

            if self.instance.pk:
                qs_license = qs_license.exclude(pk=self.instance.pk)

            if qs_license.exists():
                raise ValidationError("License is already registered")

        return license_value

    def clean(self):
        super().clean()

        if self.user and self.user.is_authenticated:
            qs_client = Seller.objects.filter(client=self.user)

            if self.instance.pk:
                qs_client = qs_client.exclude(pk=self.instance.pk)

            if qs_client.exists():
                raise ValidationError(
                    "You are already registered"
                )

        return self.cleaned_data
