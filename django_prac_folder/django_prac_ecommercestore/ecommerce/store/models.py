from django.db import models



# Since, we have made our custom user model in account app, this import is no longer needed:
# from django.contrib.auth.models import User
from django.conf import settings


# 'reverse' is a function that can be used to make url
from django.urls import reverse

# When database is created, data table would named as : "(app folder's name)_(model's name) as default"

class ProductManager(models.Manager):
    """
    Q: Why we need 'ProductManger'? Why use 'models.Manager'
    A: In django, we make models.py fat and views.py slim as possible, since dealing with database or
       querying data inside of models.py seems much intuitive than doing it in views.py. And to handle 
       filtering(querying) for 'Product' datatable, we have made 'ProductManager' in models.py, where
       'Product' model exists.
    
    Q: Purpose of get_queryset?
    A: To handle filtering of 'Product' objects.
    """
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    
    # 'Slug' is a string that can only include characters, numbers, dashes, and underscores. 
    # It is the part of a URL that identifies a particular page on a website, in a human-friendly form
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        """
        'verbose_name' = A human-readable name for the object, singular
        'verbose_name_plural' = The plural name for the object. Djano would automatically pus -s 
        at the end of model name if this attribute is not specified. 
        """
        verbose_name_plural = 'categories'

    def get_absolute_url(self):

        """
        Q: Why use get_absolute_url?
        A: In order to dynamically access to url that is associated with particular object.
           'reverse' function makes url pattern. And each data objects in websites has each
           own page(like post in blog or product page in ecommerce etc). Without this function,
           we need to manually type url for every each objects. But with get_absolute_url, only by
           calling this function able us to access to that specific object.
           In this case, we have url named 'category_list' inside of urls.py file of store app folder.
           And that url requiring url-parameter called 'slug' of slug type. So we are feeding 
           'self.slug', which is slug of Category object, as args(arguments).
        """
        return reverse('store:category_list', args=[self.slug])

    
    def __str__(self):
        """
        Q: Why use __str__?
        A: to display an object in the Django admin site and as the value inserted into
           a template when it displays an object
        """
        return self.name
    
class Product(models.Model):
    
    # 'ForiegnKey' indicates many-to-one relationship. In this case, each instance of 'Product' 
    # has one link to 'Category' model, while 'Category' can have multiple(many) 'Product'.
    # For example MacBookPro is product, and its category is laptop. Category laptop has many
    # different kinds like SamSung, Dell, HP, MacBookPro etc. 
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    
    """
    Q: Why not using 'from django.contrib.auth.models import User'?
    A: Since we have made our custom user model in 'account' app, and change some settings that is
       related to spotting location of user model in settings.py file, we need to consider our default 
       'User' model is now 'UserBase' model in 'account' app's models.py. And the reason not directly 
       importing 'UserBase' from 'account' app's folder is to avoid leak of model structure(i guess) 
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_creator', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255)
    

    """
    Q: Why there is two manager assigned, objects and products each?
    A: We need these two code, since we are using custom model manager, which is given to variable 
       named 'products', along side with default model manager. So, if not specifying this code, 
       then django would think we are only using that 'ProductManager' as the only model manager 
       we are going to use for this model. However since we want to utilize both default model manager
       and custom model manager, we are explicitly setting those two model managers.
    """
    objects = models.Manager()
    
    # Since 'ProductManager' overriding 'set_queryset' from its parent(models.Manager), and filtering
    # or querying objects that column value 'is_active' is set to True, when calling 'Product.products'
    # instead of 'Product.objects', 'set_queryset' will be applied.
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title