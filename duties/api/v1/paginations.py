from rest_framework.pagination import PageNumberPagination

""" a custom pagination for duties"""


class DutyPagination(PageNumberPagination):
    page_size = 2
