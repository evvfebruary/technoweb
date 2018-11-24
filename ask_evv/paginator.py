def paginate(objects, request, key=''):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    key += '_page'

    page = request.GET.get(key)
    p = Paginator(objects, 8)

    try:
        result = p.page(page)
    except PageNotAnInteger:
        result = p.page(1)
    except EmptyPage:
        result = p.page(1)

    result.from_left = result.number - 4
    result.from_right = result.number + 4
    result.key = key

    return result