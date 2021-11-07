from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


# category of listings
class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

# Item Listing


class Listing(models.Model):
    # who posting this item
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Title of the item
    title = models.CharField(max_length=64)
    # Item descriptions
    description = models.TextField()
    # item price
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Item Catgory
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="listing_category")
    # all categories to select from
    categories = models.ManyToManyField(
        Category, blank=True, related_name="select_category")
    # item Images
    image_url = models.URLField(default='google.com')
    # item sold or NOT sold , Default is valid for bid
    sold = models.BooleanField(default=False)
    # date_created
    create_date = models.DateTimeField(default=timezone.now())

    # default format
    def __str__(self):
        return f"{self.title}"


# Item Bidding
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"bid on item: {self.listing} by {self.user} with price: {self.price}"

# Item Comments


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.TextField(max_length=255, blank="Title for the comment")
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"

# Add to WatchList


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watching = models.BooleanField(default=False)
