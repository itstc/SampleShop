from django.db import models
from myshop import settings
from django.core.urlresolvers import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name','id')
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        # set product image to the image uploaded to imgur
        if self.image:
            self.image = settings.imgur_client.upload_from_memory(self.image)["link"]
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_photo(self):
        if self.image:
            return self.image
        return "https://images.bigcartel.com/product_images/178489259/ss16_hoodie.jpg?auto=format&fit=max&h=1000&w=1000"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])