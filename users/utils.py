def get_page_url(request):
    return request.build_absolute_uri('/')[:-1].strip("/")