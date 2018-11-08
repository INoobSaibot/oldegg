from django.shortcuts import render, redirect
from products.models import Cart
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone

from products.models import Product, Brand, ProductInstance, Category
from products.models import PaymentCard, Wallette, History, ShippingAddress
from django.contrib.auth.forms import UserCreationForm

# create your views here!


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
    #intitialize cart = False
    cart = False

    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        id =(request.user.id)
        try:
            cart = Cart.objects.filter(cartOwner=request.user, status = 'b')[0]
        except:
            c = Cart(cartOwner=request.user, status='b', shoppingSince=timezone.now())
            c.save()
        if cart:
            if cart_is_empty(cart):
                cart=False

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


def flattenCarts(qs):    
        for cart in carts:
            print(cart.id)
            for productList in cart.productList.all():
                #print("\t" + str(productList))
                for product in [productList]:
                    print("item: " + str(product))

#super ugly hacky code barf
def cart_is_empty(c):
    print('users browsing carts query length: '+ str(len(c.productList.all())))

    
    return len(c.productList.all()) == False


from django.views import generic

class StoreListView(generic.ListView):
    model = Product


class ProductDetailView(generic.DetailView):
    model = Product

class CartListView(generic.ListView):
    model = Product


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

        cart = Cart.objects.filter(cartOwner=request.user, status='b')[0]
        try:
            cart.productList.add(product)
            cart.save()
            
        except:
            cart = Cart(status='b',cartOwner= request.user,shoppingSince=timezone.now())
            cart.save()
            cart.cartOwner = request.user
            cart.save()
    else:
        # these next to lines ensure user is sent back
        # to that same items page upon a successful log in
        sendWhereAfterLogin = '/products/product/' + str(product.id)
        form = True
        context = {'next': sendWhereAfterLogin,
                    'form': form,}
        return redirect('login')
        return render(request, "registration/login.html",context = context)
        
    
    
    return HttpResponseRedirect('product/'+ str(product.pk))


def removeFromCart(request, ):
    """ Quick and dirt remove from cart method"""

    # fix at some point to cart = users.getCart()
    #  and make that method in User... or .....
    # or even maybe cart= Cart.getThisUsersCart(user)
    cart = Cart.objects.filter(cartOwner=request.user, status='b')[0]
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

    # eeew
    def is_walletteEmpty(w):
        """ public int evaluates as Bool Returns True or False 
            Returns True if users walete collection of payment types 
            has one or more payment card, returns False if users wallette has zero
            or less payment card in the collection"""
        return len(w.paymentList.all())
    
    # get address
    shippingAddress = ShippingAddress.objects.get(owner=request.user)
        

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
        'shippingAddress': shippingAddress,
    }
    print('whoah')
    #print(p.exp)
    #return HttpResponse("Your order is complete")
    return render(request, 'completeOrder.html', context=context)

def cardForm(request,):
    return render(request, "addPaymentCard.html")



def addPaymentCard(request,):
    """ """
    # pull post stuff out into variables
    posted = request.POST
    user = request.user
    #user.payments.add(pmt)
        
    try:
        w = Wallette.objects.get(owner=request.user)
        w.save()
    except:
        w = Wallette()
        w.owner = user
        w.save()

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
    w.save()
    


    def printPost():
        print(posted.keys())
        print(card_holder)
        print (cvv)
        print(card_number)
        print(expiration_date)

    print(expiration_date)
    return HttpResponseRedirect(request, "complereOrder.html")
    return render(request, "completeOrder.html")


def completeOrder(request):
    user = request.user
    orders = Cart.objects.filter(cartOwner=user)
    cart = orders.filter(status='b')[0]
    cart.status = 'p'
    cart.save()
    try:
        history = History.objects.get(owner=user)

    except:
        history = History()

    #cart.save()
    #db persistance dql actions
    history.save()
    history.orders.add(cart)
    history.save()
    
    # new cart associated to user
    cart = Cart(shoppingSince = timezone.now())
    cart.save()
    cart.cartOwner = request.user
    cart.save()

    #return HttpResponse("Your order is complete")
    return render(request, 'OrderAccepted.html')


def addAddress(request,):
    
    # pull post stuff out into variables
    posted = request.POST
    user = request.user
    try:
        streetNameAndNumber = posted['streetNameAddress']
    except:
        print("post fail in add address")
    
    return render(request, "addPaymentCard.html")
