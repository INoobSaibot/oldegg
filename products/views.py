from django.shortcuts import render

# Create your views here.







from products.models import Product, Brand, ProductInstance, Category

def index(request):
    """View function for home page of site."""

    """ Generate couns of some of the main objects"""
    num_products = Product.objects.all().count()
    num_instances = ProductInstance.objects.all().count()

    # Available items (Status = 'a')
    num_instances_available = ProductInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied for default.
    num_brands = Brand.objects.count()
    ###
    num_categories = Category.objects.count()




    # number of visis to this view, as counted in he session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1







    context = {
        'num_products': num_products,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_brands': num_brands,
        'num_categories': num_categories,
        'num_visits': num_visits,
    }
    # Render the html template index.html with data in the context variable
    return render(request, 'index.html', context=context)











from django.views import generic

class StoreListView(generic.ListView):
    model = Product






class ProductDetailView(generic.DetailView):
    model = Product







from django.http import HttpResponse

def addToCart(request, ):
    
    
    # or
    return HttpResponse("Youre post was accepted!!!!<br><br>" + request.POST['choice'])

