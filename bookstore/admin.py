from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Promotion, Address, Payment, Order, CartItem, OrderItem

from .models import Profile

# Register your models here.
# admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Promotion)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderItem)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
