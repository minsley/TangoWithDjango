from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page, UserProfile, User
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query

from datetime import datetime

def index(request):
    context = RequestContext(request)
    
    top_5_pages = Page.objects.order_by('-views')[:5]
    context_dict = {  
        'pages': top_5_pages,
        'categories': get_category_list()
    }
    
    response = render_to_response('rango/index.html', context_dict, context) 

    # Count visits using session data
    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
        
    return response

def about_page(request):
    context = RequestContext(request)
    
    if (request.session.get('visits')):
        visits = request.session.get('visits', 0)
    else:
        request.session['visits'] = 1
        visits = 1
        
    context_dict = {
                    'visits': visits,
                    'categories': get_category_list()
                    }
    return render_to_response("rango/about.html", context_dict, context)

def category(request, category_id):
    context = RequestContext(request)
    try:
        category = Category.objects.get(id=category_id)
        pages = Page.objects.filter(category=category)
        context_dict = {
                        'pages': pages,
                        'category': category,
                        'category_name': category.name,
                        'categories': get_category_list()
                        }
    except Category.DoesNotExist:
        pass
    
    return render_to_response('rango/category.html', context_dict, context)

@login_required
def add_category(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    
    context_dict = {
                    'form': form,
                    'categories': get_category_list()
                    }
    
    return render_to_response('rango/add_category.html', context_dict, context)

@login_required
def add_page(request, category_id):
    context = RequestContext(request)
    category = Category.objects.get(id=category_id)
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            page = form.save(commit=false)
            page.category = category
            page.views = 0
            page.save()
            
            return category(request, category)
        else:
            print form.errors
    else:
        form = PageForm()
        
    context_dict = {
                    'category': category, 
                    'form': form, 
                    'categories': get_category_list()
                    }
    return render_to_response('rango/add_page.html', context_dict, context)

def search(request):
    context = RequestContext(request)
    result_list = []
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        
        if query:
            result_list = run_query(query)
    
    return render_to_response('rango/search.html', {'result_list': result_list}, context)

def register(request):
    context = RequestContext(request)
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            # Hash password using set_password method, then update user
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
            
        else:
            print user_form.errors, profile_form.errors
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render_to_response(
            'rango/register.html',
            {
                'user_form': user_form, 
                'profile_form': profile_form,
                'registered': registered
            },
            context )
            
def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Get the user object if the name/pass is valid
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # User is valid and active. Log them in!
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        # Probably a GET. Show login form.
        return render_to_response('rango/login.html', {}, context)
   
@login_required
def profile(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('rango/profile.html', context_dict, context)
    
@login_required
def restricted(request):
    context = RequestContext(request)
    return render_to_response('rango/restricted.html', {}, context)

@login_required
def user_logout(request):
    # @login_required guarantees they're logged in, so we can safely log them out
    logout(request)
    return HttpResponseRedirect('/rango/')
 
def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
        
        try:
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return HttpResponseRedirect(page.url)
        except Page.DoesNotExist:
            pass
         
    return HttpResponseRedirect('/rango/')
           
#
# Helper Methods
#
def slugify_url(url):
    return url.replace(' ', '-')

def get_category_list():
    
    category_list = Category.objects.order_by('-likes')[:5]
    
    # Replace spaces in category names for category urls
    for category in category_list:
        category.url = slugify_url(category.name)
        
    return category_list