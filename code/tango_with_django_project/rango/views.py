from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[:5]
    top_5_pages = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'top_5_pages': top_5_pages
    }
    
    # Replace spaces in category names for category urls
    for category in category_list:
        category.url = encode_url(category.name)
    
    return render_to_response('rango/index.html', context_dict, context)

def about_page(request):
    return render_to_response("rango/about.html")

def category(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name}
    
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    
    return render_to_response('rango/category.html', context_dict, context)

def encode_url(url):
    return url.replace(' ', '_')

def decode_url(encoded_url):
    return encoded_url.replace('_', ' ')