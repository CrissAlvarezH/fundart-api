import os.path

from django.utils import timezone
from django.db import models
from django.utils.html import mark_safe


def phone_case_scaffold_img_path(instance, filename) -> str:
    _, ext = os.path.splitext(filename)
    return f"phone_cases/scaffold{ext}"


class PhoneCase(models.Model):

    class InventoryStatus(models.TextChoices):
        AVAILABLE = ("AVAILABLE", "Available")
        OUT_OF_STOCK = ("OUT_OF_STOCK", "Out of stock")

    price = models.FloatField()
    case_scaffold_img = models.ImageField(upload_to=phone_case_scaffold_img_path)
    inventory_status = models.CharField(max_length=200, choices=InventoryStatus.choices)
    discount = models.ForeignKey("phone_cases.Discount", null=True, blank=True, on_delete=models.DO_NOTHING)
    phone_brand_ref = models.ForeignKey("phone_cases.PhoneBrandReference", on_delete=models.DO_NOTHING)
    case_type = models.ForeignKey("phone_cases.CaseType", on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("phone_brand_ref", "case_type")

    @property
    def sale_price(self):
        if self.discount and timezone.now() < self.discount.valid_until:
            return self.price - (self.price * self.discount.rate / 1000)
        return self.price

    def scaffold_preview(self):
        path = f'<img src="{self.case_scaffold_img.url}" width="200" />'
        return mark_safe(path)

    def __str__(self):
        return f"{self.id}: {self.phone_brand_ref} (${self.price}) {self.case_type.name}"


class Discount(models.Model):
    name = models.CharField(max_length=200)
    rate = models.IntegerField(default=0)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f"{self.id}: (%{self.rate}) {self.name}"


class PhoneBrand(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name


class PhoneBrandReference(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(
        "phone_cases.PhoneBrand", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("name", "brand")

    def __str__(self):
        return f"({self.brand.name}) {self.name}"


def case_type_icon_img_path(instance, filename) -> str:
    _, ext = os.path.splitext(filename)
    return f"case_types/icon" + ext


class CaseType(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    icon = models.ImageField(upload_to=case_type_icon_img_path)

    def icon_preview(self):
        path = f'<img src="{self.icon.url}" width="150" />'
        return mark_safe(path)

    def icon_preview_mini(self):
        path = f'<img src="{self.icon.url}" width="50" />'
        return mark_safe(path)

    def __str__(self):
        return self.name


def case_type_img_path(instance, filename) -> str:
    _, ext = os.path.splitext(filename)
    return f"case_types/imgs/{instance.order_priority}{ext}"


class CaseTypeImage(models.Model):
    img = models.ImageField(upload_to=case_type_img_path)
    order_priority = models.IntegerField(default=0)
    case_type = models.ForeignKey("phone_cases.CaseType", on_delete=models.DO_NOTHING)

    def img_preview(self):
        path = f'<img src="{self.img.url}" width="150" />'
        return mark_safe(path)

    def img_preview_mini(self):
        path = f'<img src="{self.img.url}" width="50" />'
        return mark_safe(path)

    def __str__(self):
        return f"{self.case_type}"
