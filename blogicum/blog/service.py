from django.core.paginator import Paginator

from blog.constants import MAX_PER_PAGE


def get_paginated_items(request, query):
    paginator = Paginator(query, MAX_PER_PAGE)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
