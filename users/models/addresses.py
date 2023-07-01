from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=500, primary_key=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=500)
    department = models.ForeignKey("users.Department", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Address(models.Model):
    department = models.ForeignKey("users.Department", on_delete=models.DO_NOTHING)
    city = models.ForeignKey("users.City", on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=1000)
    indications = models.CharField(max_length=2000)
    receiver_name = models.CharField(max_length=500)
    receiver_phone = models.CharField(max_length=50)
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.address} - {self.department.name} / {self.city.name} ({self.user})"
