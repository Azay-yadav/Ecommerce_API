from rest_framework.pagination import PageNumberPagination

class CustomPageSizePagination(PageNumberPagination):
    page_size = 2