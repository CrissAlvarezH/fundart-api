import random
import logging
from pathlib import Path
from datetime import timedelta

from django.utils import timezone
from django.core.management import BaseCommand
from django.core.files import File

from faker import Faker

from orders.models import Coupon
from images.models import Image, ImageTag, ImageFavorite
from images.services import attach_image_from_url
from users.models import Department, City, User, Address
from phone_cases.models import (
    PhoneBrand, PhoneBrandReference, CaseType, CaseTypeImage, Discount, PhoneCase
)

LOG = logging.getLogger("insert_dummy_data")


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        self._insert_departments_and_cities(faker)
        self._insert_users(faker)
        self._insert_brands()
        self._insert_case_types()
        self._insert_discounts()
        self._insert_images(faker)
        self._insert_phone_cases()
        self._insert_coupons()

    def _insert_departments_and_cities(self, faker: Faker):
        if Department.objects.all().count() >= 10:
            return

        counter = 0
        while counter < 10:
            try:
                Department.objects.create(name=faker.country())
                counter += 1
            except Exception as e:
                LOG.error(f"ERROR on insert departments: {str(e)}")

        for d in Department.objects.all():
            counter = 0
            while counter < 5:
                try:
                    City.objects.create(name=faker.city(), department=d)
                    counter += 1
                except Exception as e:
                    LOG.error(f"ERROR on insert city {str(e)}")

    def _insert_users(self, faker: Faker):
        if User.objects.all().count() > 9:
            return

        counter = 0
        while counter < 10:
            try:
                User.objects.create(
                    full_name=faker.first_name() + " " + faker.last_name(),
                    email=faker.profile("mail")["mail"],
                    phone=faker.phone_number(),
                )
                counter += 1
            except Exception as e:
                LOG.error(f"ERROR on create user {str(e)}")

        city_ids = [c.id for c in City.objects.all()]
        for u in User.objects.all():
            counter = 0
            max = random.randint(1, 4)
            while counter < max:
                Address.objects.create(
                    city_id=random.choice(city_ids),
                    address=faker.address(),
                    indications=faker.street_address(),
                    receiver_name=faker.first_name(),
                    receiver_phone=faker.phone_number(),
                    user=u
                )
                counter += 1

    def _insert_brands(self):
        data = {
            "Iphone": ["12 Pro Max", "14 Pro", "14 Pro Max", "X"],
            "Samsung": ["Galaxy S22 Ultra", "Galaxy Note 20", "Galaxy A6"],
            "Xiaomi": ["Redmi Note 7", "Redmi Note 10"],
            "Huawei": ["Mate 10P", "Mate 20X"],
        }

        for brand, refs in data.items():
            if PhoneBrand.objects.filter(name=brand).exists():
                continue

            brand_instance = PhoneBrand.objects.create(name=brand)
            for ref in refs:
                PhoneBrandReference.objects.create(name=ref, brand=brand_instance)

    def _insert_case_types(self):
        data = ["Plastico", "Madera", "Ultra"]
        parent_dir = Path.joinpath(Path(__file__).parent, "dummy_data", "case_type_imgs")
        for i in data:
            img_path = Path.joinpath(parent_dir, i.lower(), f"icon.jpg")
            case_type, created = CaseType.objects.get_or_create(name=i)
            if not created:
                continue

            case_type.icon = img_path
            with open(img_path, "rb") as f:
                case_type, _ = CaseType.objects.get_or_create(name=i)
                case_type.icon.save(f"phone_case_icon_{i.lower()}.jpg", File(f), save=True)

            # save case type images
            for counter in range(1, 3):
                img_path = Path.joinpath(parent_dir, i.lower(), f"{i.lower()}_{counter}.jpg")
                with open(img_path, "rb") as f:
                    case_type_img = CaseTypeImage.objects.create(
                        order_priority=counter, case_type=case_type)
                    case_type_img.img.save("case_img.jgp", File(f), save=True)

    def _insert_discounts(self):
        if not Discount.objects.filter(name="Lanzamiento").exists():
            Discount.objects.create(
                name="Lanzamiento", rate=25, valid_until=(timezone.now() + timedelta(days=30)))

        if not Discount.objects.filter(name="Navidad").exists():
            Discount.objects.create(
                name="Navidad", rate=15, valid_until=(timezone.now() + timedelta(days=30)))

    def _insert_images(self, faker: Faker):
        if Image.objects.all().count() >= 100:
            return

        for _ in range(100):
            img = Image.objects.create(
                prompt=faker.sentence(),
                description=faker.sentence(),
                created_by_id=User.objects.first().id
            )
            attach_image_from_url("https://picsum.photos/400/800", img)

        # add tags
        tags = [
            "Amor", "Amistad", "Musica", "Peliculas", "Acción", "Humor",
            "Motivación", "Series", "Negro", "Blanco", "Historia", "Tecnología",
        ]
        for t in tags:
            ImageTag.objects.create(name=t)

        for img in Image.objects.all():
            for _ in range(random.randint(2, 5)):
                tag = random.choice(tags)
                img.tags.add(tag)

        # add image favorites
        users = [u for u in User.objects.all()]
        imgs = [i for i in Image.objects.all()]
        for _ in range(40):
            ImageFavorite.objects.create(
                user=random.choice(users), image=random.choice(imgs),
            )

    def _insert_phone_cases(self):
        if PhoneCase.objects.all().count() > 10:
            return

        types = [t for t in CaseType.objects.all()]
        discounts = [d for d in Discount.objects.all()]

        for ref in PhoneBrandReference.objects.all():
            for type_i in range(random.randint(1, 3)):
                PhoneCase.objects.create(
                    price=(random.randint(32, 72) * 1000),
                    inventory_status=PhoneCase.InventoryStatus.AVAILABLE,
                    discount=random.choice(discounts) if random.choice([True, False]) else None,
                    phone_brand_ref=ref,
                    case_type=types[type_i],
                )

        # set scaffold image
        parent_dir = Path.joinpath(Path(__file__).parent, "dummy_data")
        with open(Path.joinpath(parent_dir, "phone_case_scaffold.jpg"), "rb") as f:
            for pc in PhoneCase.objects.all():
                pc.case_scaffold_img.save("scaffold.jpg", File(f), save=True)

    def _insert_coupons(self):
        if Coupon.objects.all().count() > 1:
            return

        cases = [pc for pc in PhoneCase.objects.all()]
        names = ["FREE_3", "SAVE", "MONEY", "BLACK_FRIDAY", "CIBER_LUNES"]
        for name in names:
            for_all_cases = random.choice([True, False])

            coupon = Coupon.objects.create(
                value=name,
                discount_rate=random.choice([15, 20, 25, 12, 10]),
                is_free_shipping=random.choice([True, False]),
                max_uses=random.randint(1, 4),
                valid_until=(timezone.now() + timedelta(days=30)),
                for_all_phone_cases=for_all_cases,
                created_by=User.objects.first(),
            )

            if not for_all_cases:
                coupon.phone_cases.add(*[random.choice(cases) for pc in range(10)])
