from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone


class Item(models.Model):

    class Meta:
        indexes = [
            models.Index(
                fields=['user_name', 'item_price'],
                name='user_price_idx'
            )
        ]

    def __str__(self):
        return self.item_name + ":" + str(self.item_price)

    def get_absolute_url(self):
        return reverse('myapp:index')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        db_index=True
    )

    item_name = models.CharField(max_length=200)

    item_desc = models.CharField(max_length=200)

    item_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    # item_image = models.URLField(
    #     max_length=500,
    #     default="https://placehold.co/200x200"
    item_image = models.ImageField(
        upload_to='item_images/',null=True, blank=True
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # Soft delete flag
    # Saves timestamp

    objects = ItemManager()

    all_objects = models.Manager()


class Category(models.Model):

    name = models.CharField(max_length=100)

    added_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, related_name="orders")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"    