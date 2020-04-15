#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Promotion(models.Model):
    promo_code = models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.FloatField()

    class Meta:
        db_table = 'promotion'


class Address(models.Model):
    street = models.CharField(max_length=45, blank=False)
    city = models.CharField(max_length=45, blank=False)
    zip_code = models.CharField(max_length=20, blank=False)
    state = models.CharField(max_length=20, blank=False)

    class Meta:
        db_table = 'address'


class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(db_column='ISBN', max_length=45)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=45)
    publisher = models.CharField(max_length=45)
    publication_year = models.IntegerField()
    cover_picture = models.TextField(default="")
    rating = models.FloatField()
    book_status = models.CharField(max_length=45)
    quantity = models.IntegerField()
    buying_price = models.FloatField()
    selling_price = models.FloatField()
    minimum_threshold = models.IntegerField()

    class Meta:
        db_table = 'book'
        ordering = ('title',)


class Cart(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,
                             default="")  # Had to add default bc 'user' is a non-nullable field and needs a
    # default; the database needs something to populate existing rows

    class Meta:
        db_table = 'cart'


class Order(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    promotion = models.ForeignKey('Promotion', on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.FloatField()
    order_date = models.DateField()
    order_time = models.TimeField()

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_item'
        unique_together = (('book', 'order'),)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'cart_item'


class Payment(models.Model):
    CARD_TYPES = (
        (1, 'Visa'),
        (2, 'MasterCard'),
        (3, 'American Express'),
    )

    card_no = models.CharField(max_length=20)
    card_type = models.CharField(choices=CARD_TYPES, max_length=45)
    exp_date = models.CharField(max_length=20)

    class Meta:
        db_table = 'payment'


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'transaction'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='profile_shipping')
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='profile_billing')
    payment_info = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    promotion_status = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'