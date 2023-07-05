from phone_cases.models import PhoneCase, PhoneBrand, PhoneBrandReference


def get_phone_case_by_type_and_ref(type_id: int, ref_id: int):
    return PhoneCase.objects.filter(
        phone_brand_ref_id=ref_id, case_type_id=type_id
    ).first()

