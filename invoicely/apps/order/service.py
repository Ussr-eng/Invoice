from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationOrders(PageNumberPagination):
    page_size = 13
    max_page_size = 1000
