from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)
    address = models.ForeignKey("users.Address", on_delete=models.DO_NOTHING)
    coupons = models.ManyToManyField("orders.Coupon", blank=True)
    shipping_cost = models.FloatField(default=0)

    class Meta:
        ordering = ("id",)

    def coupons_resume(self):
        resume = [str(c) for c in self.coupons.all()]
        if len(resume) > 0:
            return resume
        return "None"

    @property
    def total(self):
        total = 0
        for p in self.orderphonecase_set.all():
            total += p.total_price

        discount_shipping = False
        for c in self.coupons.all():
            total -= (total * c.discount_rate) / 100
            if c.is_free_shipping:
                discount_shipping = True

        if not discount_shipping:
            total += self.shipping_cost

        return total

    def current_status(self):
        status = self.orderstatushistory_set.all().order_by("-set_at").first()
        if status:
            return status.status
        return None

    def __str__(self):
        return f"Order: {self.id}"


@receiver(post_save, sender=Order)
def save_order_status_history_in_created(sender, instance, created, **kwargs):
    if created:
        OrderStatusHistory.objects.create(
            status=OrderStatusHistory.Status.CREATED,
            details="", order=instance, user=instance.user
        )


class OrderStatusHistory(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        CANCELED = "CANCELED", "Canceled"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        DISPATCHED = "DISPATCHED", "Dispatched"
        RECEIVED = "RECEIVED", "Received"

    status = models.CharField(max_length=50, choices=Status.choices)
    details = models.CharField(max_length=500, blank=True)
    set_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey("orders.Order", on_delete=models.DO_NOTHING)
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Order {self.order.id} - {self.status} at {self.set_at}"


class OrderPhoneCase(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.DO_NOTHING)
    phone_case = models.ForeignKey("phone_cases.PhoneCase", on_delete=models.DO_NOTHING)
    image = models.ForeignKey("images.Image", on_delete=models.DO_NOTHING)
    discount = models.ForeignKey("phone_cases.Discount", on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()

    @property
    def total_price(self):
        if self.discount:
            return self.quantity * (self.price - (self.price * self.discount.rate / 100))
        else:
            return self.quantity * self.price


class Coupon(models.Model):
    class ValidStatus:
        INVALID_USED = "NO: used"
        INVALID_EXPIRED = "NO: expired"
        VALID = "YES"

    value = models.CharField(max_length=50, primary_key=True)
    discount_rate = models.IntegerField(default=0)
    is_free_shipping = models.BooleanField(default=False)
    max_uses = models.IntegerField(default=1)
    uses = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    created_by = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)

    for_all_phone_cases = models.BooleanField(default=False)
    phone_cases = models.ManyToManyField("phone_cases.PhoneCase", blank=True)

    def is_valid(self):
        if self.uses >= self.max_uses:
            return self.ValidStatus.INVALID_USED
        if timezone.now() > self.valid_until:
            return self.ValidStatus.INVALID_EXPIRED
        return self.ValidStatus.VALID

    @transaction.atomic()
    def use(self) -> bool:
        if self.uses < self.max_uses:
            self.uses += 1
            self.save()
            return True
        return False

    def __str__(self):
        return f"Coupon: (%{self.discount_rate}) {self.value}"
