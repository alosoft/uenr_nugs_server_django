from django.db import models

# Create your models here.
from news.models import Media


class Color(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    color_code = models.CharField(max_length=6, blank=False, unique=True,
                                  help_text='goto https://htmlcolorcodes.com/color-names/ and pick appropriate color code without # sign eg.FF0000 for red. its very import that you get this right')

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    size_value = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    cat = (
        ('Book', 'Book'),
        ('Shirt', 'Shirt'),
        ('Cap', 'Cap')
    )

    stat = (
        ('Available', 'Available'),
        ('Out of Stock', 'Out of Stock')
    )

    name = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=1000, blank=False, null=False)
    features = models.TextField(max_length=1000, blank=False, null=False)
    specifications = models.TextField(max_length=1000, blank=False, null=False)
    diameter = models.DecimalField(max_digits=3, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unlimited = models.BooleanField(default=False)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(blank=False, null=False)
    status = models.CharField(
        choices=stat, blank=False, null=False, max_length=50)
    category = models.CharField(
        choices=cat, blank=False, null=False, max_length=50)
    image = models.ManyToManyField(Media, blank=False, unique=False,
                                   related_name='product_image')
    sizes = models.ManyToManyField(Size, blank=True, unique=False,
                                   related_name='product_sizes')
    colors = models.ManyToManyField(Color, blank=True, unique=False,
                                    related_name='product_colors')

    def __str__(self):
        return self.name

    def color_list(self):
        colors_dict = {}
        for item in self.colors.values():
            colors_dict[str(item['id']) + item['name']] = item['color_code']
        return colors_dict

    def size_list(self):
        size_dict = {}
        for item in self.sizes.values():
            size_dict[str(item['id']) + item['name']] = item['size_value']
        return size_dict

    def images(self):
        images = []
        for item in self.image.values():
            if item['media_type'] == 'Picture':
                images.append(item['image'])
            if item['media_type'] == 'Video':
                images.append(item['video'])
        return images


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, blank=False, null=False, related_name="user_order_item", on_delete=models.PROTECT)
    quantity = models.IntegerField(blank=False, null=False)
    color = models.ForeignKey(
        Color, blank=True, null=True, unique=False, related_name='product_color', on_delete=models.SET_NULL)
    size = models.ForeignKey(
        Size, blank=True, null=True, related_name='product_size', on_delete=models.SET_NULL)
    owner = models.ForeignKey(
        'users.User', related_name='order_item_owner', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def date(self):
        return self.created.strftime('%a, %d %B %Y')

    def color_name(self):
        if self.color:
            return self.color.name
        return 'Default'

    def size_name(self):
        if self.size:
            return self.size.name
        return 'Default'


class Order(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
        ('Not Paid', 'Not Paid')
    )
    items = models.ManyToManyField(
        OrderItem, related_name='user_order', blank=False)
    owner = models.ForeignKey(
        'users.User', related_name='order_owner', on_delete=models.CASCADE)
    status = models.CharField(choices=stat, default='Pending', max_length=50)
    transaction = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        summary = ''
        for order_item in self.items.values():
            product_name = None
            try:
                product_name = Product.objects.get(pk=int(order_item['product_id'])).name
            except Product.DoesNotExist:
                product_name = None
            summary += '{} x {} / '.format(str(order_item['quantity']), product_name)
        return f'{summary} Ordered by {self.owner.email}'

    def date(self):
        return self.created.strftime('%a, %d %B %Y')

    class Meta:
        ordering = ['-created']

    def price(self):
        total_price = 0
        for order_item in self.items.values():
            try:
                product = Product.objects.get(pk=int(order_item['product_id']))
                total_price += (((100 - product.discount) / 100)
                                * product.price) * order_item['quantity']
            except Product.DoesNotExist:
                print('no product with that id')
        return total_price

    def description(self):
        desc = ''
        for order_item in self.items.values():
            try:
                product = Product.objects.get(pk=int(order_item['product_id']))
                desc += '{} * {} {} '.format(
                    order_item['product_id'], product, '\n')
            except Product.DoesNotExist:
                print('no product with that id')
        return desc


class Review(models.Model):
    rating = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    owner = models.ForeignKey(
        'users.User', related_name='review_owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    product = models.ForeignKey(
        Product, related_name='review_product', on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    stars = models.CharField(choices=rating, default='1', max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def user_details(self):
        details = {}
        details['username'] = self.owner.username
        try:
            details['image'] = self.owner.image.url
        except:
            details['image'] = None
        return details

    def __str__(self):
        return self.owner.username

    def date(self):
        return self.created.strftime('%a, %d %B %Y')


class TrackingItem(models.Model):
    stat = (
        ('Not Started', 'Not Started'),
        ('Pending', 'Pending'),
        ('Completed', 'Conpleted')
    )
    types = (
        ('Ordered', 'Ordered'),
        ('packed', 'packed'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered')
    )
    type = models.CharField(choices=types, max_length=50,
                            blank=False, null=False)
    status = models.CharField(
        choices=stat, max_length=50, blank=False, null=False)
    description = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    def date(self):
        return self.created.strftime('%a, %d %B %Y')

    class Meta:
        verbose_name = 'Tracking Item'
        verbose_name_plural = 'Tracking Items'


class Tracking(models.Model):
    order = models.OneToOneField(
        Order, related_name="tracking_product", on_delete=models.CASCADE)
    ordered = models.OneToOneField(
        TrackingItem, related_name="tracking_ordered", on_delete=models.CASCADE)
    packed = models.OneToOneField(
        TrackingItem, related_name="tracking_packed", on_delete=models.CASCADE)
    shipped = models.OneToOneField(
        TrackingItem, related_name="tracking_shipped", on_delete=models.CASCADE)
    delivered = models.OneToOneField(
        TrackingItem, related_name="tracking_delivered", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order} tracking'

    class Meta:
        verbose_name = 'Tracking'
        verbose_name_plural = 'Trackings'

    def date(self):
        return self.created.strftime('%a, %d %B %Y')
