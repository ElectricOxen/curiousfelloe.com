from django.shortcuts import render


def home(request):
    return render(request, 'landing/home.html')


def page_forbidden(request, exception):
    return render(request, 'errors/403.html', status=403)


def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)
