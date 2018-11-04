from django.shortcuts import render
from products.models import Cart
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.







from products.models import Product, Brand, ProductInstance, Category
from products.models import PaymentCard, Wallette, History

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

    ## cart stuff
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        id =(request.user.id)
        try:
            cart = Cart.objects.get(cartOwner=request.user)
        except:
            cart = Cart()
            cart.save()
            cart.cartOwner = request.user

    else:
        cart = Cart()

        
    cart.save()

    #super ugly hacky code barf
    def cartEmpty(c):
        print(len(c.productList.all()))
        return len(c.productList.all()) == False
    
    if cartEmpty(cart):
        cart = False
    
    
        




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
        'cart': cart,
    }
    # Render the html template index.html with data in the context variable
    return render(request, 'index.html', context=context)











from django.views import generic

class StoreListView(generic.ListView):
    model = Product






class ProductDetailView(generic.DetailView):
    model = Product

class CartListView(generic.ListView):
    model = Product





from django.http import HttpResponse

def addToCart(request, ):
    # some of this is all hard coded just to test will fix
    # cart model needs changed to hold one user to many carts
    # why many carts you ask? IM GLAD YOU ASKED!!!
        ##CARTS can immediatly be converted to orders, via, status atribute
        ### Example, browsing, ORder, other stuff...
   
    user = None
    username = None
    product = Product.objects.get(itemNumber=request.POST['choice'])

    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        id =(request.user.id)
        try:
            cart = Cart.objects.get(cartOwner=request.user)
        except:
            cart = Cart()
            cart.save()
            cart.cartOwner = request.user
            cart.save()
    else:
        cart = Cart()
        cart.save()
        
    cart.productList.add(product)
    cart.save()
    
    return HttpResponseRedirect('product/'+ str(product.pk))
    #return render("Youre post was accepted!!!!<br><br>" + request.POST['choice'])


def removeFromCart(request, ):
    """ Quick and dirt remove from cart method"""
    cart = Cart.objects.get(cartOwner=request.user)
    #print('posted:' + request.POST['choice'] + '<---------------------')
    #print(Product.objects.get(itemNumber=request.POST['choice']))
    cart.productList.remove(Product.objects.get(itemNumber=request.POST['choice']))
    cart.save()

    #return HttpResponse()
    return (index(request,))


def placeOrder(request,):
    """ """
    # pull post stuff out into variables
    posted = request.POST
    user = request.user
    ERRORS = []

    try:
        w = Wallette.objects.get(owner=request.user)
        w.save()
    except:
        w = Wallette()
        w.owner = user
        w.save()
        return render(request, 'addCard.html', context=context)

    #user.payments.add(pmt)
    try:
        card_holder = posted['card_holder']
        cvv = posted['cvv']
        card_number = posted['cardNumber']
        expiration_date = posted['exp_month'] + "/" + posted['exp_year']
        

        p = PaymentCard()
        p.cardHolder = card_holder
        p.cvv = cvv
        p.cardNumber = card_number
        p.exp = expiration_date
        p.save()
        w.paymentList.add(p)
    except:
        pass
    
    payment_list = w.paymentList.all()
    hasCard = (len(payment_list)) > 0

    if posted.get('addCard') == "Different Card":
        print("addcard")
        print(hasCard)

    context = {
        'user': user,
        'payment_list': payment_list,
        'ERRORS': ERRORS,
    }
    print('whoah')
    return render(request, 'completeOrder.html', context=context)


def addPayment(request,):
    """ """
    # pull post stuff out into variables
    posted = request.POST
    user = request.user
    #user.payments.add(pmt)

    card_holder = posted['card_holder']
    cvv = posted['cvv']
    card_number = posted['cardNumber']
    expiration_date = posted['exp_month'] + "/" + posted['exp_year']
    
    def printPost():
        print(posted.keys())
        print(card_holder)
        print (cvv)
        print(card_number)
        print(expiration_date)

    print(expiration_date)


def completeOrder(request):
    user = request.user
    cart = Cart.objects.get(cartOwner=user)
    cart.status = 'p'
    cart.save()
    try:
        history = History.objects.get(owner=user)

    except:
        history = History()
    
    #cart.save()
    history.save()
    cart.save()
    history.orders.add(cart)
    
    return render(request, 'completeOrder.html')
