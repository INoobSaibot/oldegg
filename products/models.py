from django.db import models

# Create your models here.







class Category(models.Model):
    """Model representing a product category. """
    name = models.CharField(max_length=200, help_text='Enter a product category(Example Video Cards)')

    def __str__(self):
        """String for repsenting the Model object."""
        return self.name



from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Product(models.Model):
    """Model representing a product-type (but not a specific instance)."""
    name = models.CharField(max_length=200)

    # Foreign key used because product can only have one Brand, but Brands can have multiple products
    # Brand as a string rather than object becuase it hasn't been declared yet in the file
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the product')
    itemNumber = models.CharField('itemNumber', max_length=7, help_text='7 character item number ie 1237428 Olive garden dressing at costco')

    # ManyToManyField used because categor can contain many products. And products can cover more than one category potentially
    # Category class has already been defined so we can specify the object above.
    category = models.ManyToManyField(Category, help_text='Select a category for this product')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this product."""
        return reverse('product-detail', args=[str(self.id)])





    
    #still needs some work, defualt, required, null etc. just added to get
    #shopping cart working
    price = models.FloatField("Price")







import uuid # Required for unique product instances

class ProductInstance(models.Model):
    """Model representing a specific instance of a product (i.e. that can be tracked in warehouse)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular product across whole system')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True) 
    productLine = models.CharField(max_length=200)
    next_ship = models.DateField(null=True, blank=True)

    PRODUCT_STATUS = (
        ('t', 'test'),
        ('o', 'Sold Out'),
        ('a', 'Available'),
        ('b', 'Back Order'),
    )

    status = models.CharField(
        max_length=1,
        choices=PRODUCT_STATUS,
        blank=True,
        default='t',
        help_text='Product availability',
    )

    class Meta:
        ordering = ['next_ship']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.product.name})'










class Brand(models.Model):
    """Model representing a Brand."""
    brand_name = models.CharField(max_length=100)
    manufacturer_name = models.CharField(max_length=100)
    making_since = models.DateField(null=True, blank=True)


    class Meta:
        ordering = ['manufacturer_name', 'brand_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular Brand instance."""
        return reverse('brand-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.manufacturer_name}, {self.brand_name}'













import uuid # Required for unique cart instances 






class Cart(models.Model):
    """Model representing a specific instance of a cart (i.e. that can be tracked in warehouse)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular product across whole system')
    #product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True) 
    productList = models.ManyToManyField(Product)
    #productLine = models.CharField(max_length=200)
    next_ship = models.DateField(null=True, blank=True)
    #category = models.ManyToManyField(Category, help_text='Select a category for this product')


    CART_STATUS = (
        ('b', 'Browsing'),
        ('o', 'ORDER'),
        ('a', 'a'),
        ('c', 'Cancelled'),
    )

    status = models.CharField(
        max_length=1,
        choices=CART_STATUS,
        blank=True,
        default='t',
        help_text='Product availability',
    )

    class Meta:
        ordering = ['next_ship']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.productList})'