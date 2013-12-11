from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says Hello World! Click <a href='/rango/about/'>here</a> to get to the About page.")

def about_page(request):
    return HttpResponse("Rango says: Here is the about page. Click <a href='/rango/'>here</a> to go back.")

