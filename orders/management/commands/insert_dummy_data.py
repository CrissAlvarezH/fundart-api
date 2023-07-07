import logging

from django.core.management import BaseCommand

from faker import Faker
from faker.providers import address as address_provider

from users.models import Department, City

LOG = logging.getLogger("insert_dummy_data")


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        self._insert_departments_and_cities(faker)

    def _insert_departments_and_cities(self, faker: Faker):
        faker.add_provider(address_provider)
        counter = 0
        while counter < 10:
            try:
                Department.objects.create(name=faker.country())
                counter += 1
            except Exception as e:
                LOG.error("ERROR on insert departments")
                LOG.exception(e)

        for d in Department.objects.all():
            counter = 0
            while counter < 5:
                try:
                    City.objects.create(name=faker.city(), department=d)
                    counter += 1
                except Exception as e:
                    LOG.error("ERROR on insert city")
                    LOG.exception(e)
