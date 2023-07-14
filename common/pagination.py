import math

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "pagination": {
                "page_size": self.page_size,
                "page": self.page.number,
                "total_pages": math.ceil(self.page.paginator.count / self.page_size),
                "total_records": self.page.paginator.count,
            },
            "results": data
        })
