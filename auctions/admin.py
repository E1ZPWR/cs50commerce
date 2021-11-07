from django.contrib import admin

from .models import User, Listing, Category, Bid, Comment, WatchList
# Register your models here.
# Admin Pasge Display Layout


class CategoryLauout(admin.ModelAdmin):
    list_display = ("id",
                    "category",
                    )


admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Category, CategoryLauout)
admin.site.register(Comment)
admin.site.register(WatchList)
