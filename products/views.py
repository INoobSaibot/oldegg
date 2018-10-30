from django.shortcuts import render
from products.models import Cart

from django.contrib.auth.models import User
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
    # some of this is all hard coded just to test will fix
    # cart model needs changed to hold one user to many carts
    # why many carts you ask? IM GLAD YOU ASKED!!!
        ##CARTS can immediatly be converted to orders, via, status atribute
        ### Example, browsing, ORder, other stuff...
    #cart = Cart.objects.get(cartOwner=request.user)
    #cart.save()
    #cart.productList.add(Product.objects.get(itemNumber=request.POST['choice']))
    
    

    user = None
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        id =(request.user.id)
        #user = User.objects.get(pk=id)
        try:
            cart = Cart.objects.get(cartOwner=request.user)
        except:
            cart = Cart()
            cart.save()
            cart.cartOwner = request.user
            cart.save()
        
    cart.productList.add(Product.objects.get(itemNumber=request.POST['choice']))
    cart.save()
    

    
    # or
    
    return HttpResponse("Youre post was accepted!!!!<br><br>" + request.POST['choice'])

