from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from phone_cases.models import PhoneCase
from phone_cases.serializers import PhoneCaseSerializer
from phone_cases.services import get_phone_case_by_type_and_ref


class PhoneCaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PhoneCase.objects.all()
    serializer_class = PhoneCaseSerializer

    @action(detail=False, methods=["GET"], url_path=r"type/(?P<type_id>\d+)/ref/(?P<ref_id>\d+)")
    def retrieve_by_type_and_ref(self, request, type_id, ref_id):
        case = get_phone_case_by_type_and_ref(type_id, ref_id)

        if not case:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(PhoneCaseSerializer(case).data)

    @action(detail=False, methods=["GET"])
    def summary(self, request):
        cases = PhoneCase.objects.filter(is_active=True)
        summary = {}
        for case in cases:
            brand = case.phone_brand_ref.brand.name
            ref = case.phone_brand_ref.name
            case_type = case.case_type.name

            summary = {
                **summary,
                brand: {
                    **summary.get(brand, {}),
                    ref: {
                        **summary.get(brand, {}).get(ref, {}),
                        case_type: PhoneCaseSerializer(case).data
                    }
                }
            }

        return Response(summary)
