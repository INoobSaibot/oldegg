from django.shortcuts import render, redirect
from products.models import Cart
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone

from products.models import Product, Brand, ProductInstance, Category
from products.models import PaymentCard, Wallette, History, ShippingAddress
from cart.models import TestCart, CartItem
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
    #which is a hack to keep population of context dict from crashing :()
    cart = False
    testCart = False

    if request.user.is_authenticated:
        print(request.user.email)
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
        
        #testCart
        user = request.user
        if TestCart.objects.filter(cartOwner=user, status='b').count() < 1:
            testCart = TestCart(cartOwner=user, status='b')
            testCart.save()
        testCart = TestCart.objects.filter(cartOwner=user, status='b')[0]
        print(testCart)
        if testCart.itemsInCart.count() < 1:
            testCart = False

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
        'testCart': testCart,
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

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        ## Add in a QuerySet of all the ...
        request = self.request
        context['testCart'] = getCart(request)
        return context

class CartListView(generic.ListView):
    model = Product

def getCart(request,):
     ## cart stuff
    #intitialize cart = False
    #which is a hack to keep population of context dict from crashing :()
    cart = False
    testCart = False

    if request.user.is_authenticated:
        print(request.user.email)
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
        
        #testCart
        user = request.user
        if TestCart.objects.filter(cartOwner=user, status='b').count() < 1:
            testCart = TestCart(cartOwner=user, status='b')
            testCart.save()
        testCart = TestCart.objects.filter(cartOwner=user, status='b')[0]
        print(testCart)
        if testCart.itemsInCart.count() < 1:
            testCart = False
        return testCart
    pass

def addToCart(request, ):
    # some of this is all hard coded just to test will fix
    # cart model needs changed to hold one user to many carts
    # why many carts you ask? IM GLAD YOU ASKED!!!
        ##CARTS can immediatly be converted to orders, via, status atribute
        ### Example, browsing, ORder, other stuff...
    print("Add to cart")
    user = None
    username = None
    print(request.POST)
    product = Product.objects.get(itemNumber=request.POST['choice'])

    if request.user.is_authenticated:
        username = request.user.username
        user = request.user
        print(username)
        id =(request.user.id)

        cart = Cart.objects.filter(cartOwner=request.user, status='b')[0]
        testCart = TestCart.objects.filter(cartOwner=user, status='b')[0]
        try:
            cart.productList.add(product)
            cart.save()
            
        except:
            cart = Cart(status='b',cartOwner= request.user,shoppingSince=timezone.now())
            cart.save()
            cart.cartOwner = request.user
            cart.save()

        #same but for new test cart class
        try:
            testCart.putInCart(product)
        
        except Exception as e:
            print(e)
    
    else:
        # these next to lines ensure user is sent back
        # to that same items page upon a successful log in
        sendWhereAfterLogin = '/products/product/' + str(product.id)
        form = True
        context = {'next': sendWhereAfterLogin,
                    'form': form,}
        #return redirect('login')
        return render(request, "registration/login.html",context = context)
        

    return HttpResponseRedirect('product/'+ str(product.pk))

def removeFromTestCart(request,):
    """event handle to remove line item from TestCart """
    user = request.user
    posted = request.POST
    #removeFromCart(request,)
    for k,v in request.POST.items(): print (k, '>', v)
    removeItem = posted.get('pk')
    increaseQuantity = posted.get('increase')
    decreaseQuantity = posted.get('decrease')


    if removeItem:
        cart = TestCart.objects.filter(cartOwner=user, status='b')[0]
        pk = request.POST['pk']
        print(request.POST)
        cartItem = CartItem.objects.get(pk=pk)

        cart.itemsInCart.remove(cartItem)

    elif increaseQuantity:
        print(increaseQuantity)
        pk = increaseQuantity
        cartItem = CartItem.objects.get(pk=pk)
        cartItem.increaseQuantity()

    elif decreaseQuantity:
        pk = decreaseQuantity
        cartItem = CartItem.objects.get(pk=pk)
        cartItem.decreaseQuantity()
    
    product = cartItem.m
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


def placeOrder(request, ):
    """ """
    # pull post stuff out into variables
    posted = request.POST
    user = request.user
    ERRORS = []
    print('place orderssss')
    
    # get address's
    addressList = ShippingAddress.objects.filter(owner=request.user)
    print(addressList.count())
    if addressList.count() < 1:
        return render(request, 'addAddress.html')

    try:
        shippingAddress = ShippingAddress.objects.filter(owner=request.user)[0]
    except Exception as e:
        print('ship addy xcept')
        print(e)
        return render(request, 'addAddress.html')

    addressList = ShippingAddress.objects.filter(owner=request.user)

    # get payment types done more like address's
    payment_list = PaymentCard.objects.filter(owner=request.user)
    print(payment_list)
    if payment_list.count() < 1:
        print("render payment bleh")
        return render(request, 'addPaymentCard.html')
    
    try:
        payment = PaymentCard.objects.filter(owner=request.user)
    except Exception as e:
        print('payment cards except')
        print(e)
        return render(request, 'addPaymentCard.html')
    
    # test cart newwer cart stuff
    orders = TestCart.objects.filter(cartOwner=user)
    cart = orders.filter(status='b')[0]
    order = cart

    context = {
        'user': user,
        'payment_list': payment_list,
        'ERRORS': ERRORS,
        'shippingAddress': shippingAddress,
        'addressList': addressList,
        'order': order,
    }
    #print(p.exp)
    #return HttpResponse("Your order is complete")
    return render(request, 'completeOrder.html', context=context)

def cardForm(request,):
    return render(request, "addPaymentCard.html")



def addPaymentCard(request,):
    """ """
    print("addPaymentCard")
    # pull post stuff out into variables
    posted = request.POST
    user = request.user
    #user.payments.add(pmt)
    def lame():    
        try:
            w = Wallette.objects.get(owner=request.user)
            w.save()
        except:
            w = Wallette()
            w.owner = user
            w.save()
    if request.method == "POST":
        card_holder = posted['card_holder']
        cvv = posted['cvv']
        card_number = posted['cardNumber']
        expiration_date = posted['exp_month'] + "/" + posted['exp_year']
        
        p = PaymentCard()
        p.owner = user
        p.cardHolder = card_holder
        p.cvv = cvv
        p.cardNumber = card_number
        p.exp = expiration_date
        p.save()
    
    addressList = ShippingAddress.objects.filter(owner=request.user)

    payment_list = PaymentCard.objects.filter(owner=request.user)

    shippingAddress = ShippingAddress.objects.filter(owner=request.user)[0]
    
    ERRORS = None
    
    context = {
        'user': user,
        'payment_list': payment_list,
        'ERRORS': ERRORS,
        'shippingAddress': shippingAddress,
        'addressList': addressList,
    }

    #return HttpResponseRedirect(request, "completeOrder.html")
    return render(request, "completeOrder.html", context = context)


def completeOrder(request,):
    user = request.user
    orders = Cart.objects.filter(cartOwner=user)
    cart = orders.filter(status='b')[0]
    
    # test cart newwer cart stuff
    orders = TestCart.objects.filter(cartOwner=user)
    cart = orders.filter(status='b')[0]
    #for context to get id etc
    order = cart
    
    #continue with original code with newer cart injected
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


    context = {
        'user': user,
        'order': order,
    }


    #return HttpResponse("Your order is complete")
    return render(request, 'OrderAccepted.html', context=context)


def addressForm(request,):
    print(request.method)
    print('address form')
    if request.method == "POST": #If the form has been submitted...
        # pull post stuff out into variables
        posted = request.POST
        user = request.user

    try:
        streetNameAndNumber = posted['streetNameAddress']
    except:
        print("post fail in add address")
        print(posted)
    return render(request, "addAddress.html")

def addAddress(request,):
    print('add address')
    user = request.user
    if request.method == "POST":
        posted = request.POST
        
        address_name = posted['address_name']
        streetNameAndNumber = posted['streetNameAndNumber']
        theCity = posted['theCity']
        state = posted['state']
        print(posted)
        
        
        sh = ShippingAddress(owner=user, address=streetNameAndNumber, city=theCity, state=state)
        sh.save()

        return HttpResponseRedirect("order")
        return HttpResponse(address_name + " " +
         " " + streetNameAndNumber + " " + theCity +
           " " + state)
    else:
        return HttpResponse("addAddress")
