# Generated by Django 3.0.2 on 2020-04-09 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=45)),
                ('city', models.CharField(max_length=45)),
                ('zip_code', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('isbn', models.CharField(db_column='ISBN', max_length=45)),
                ('author', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=45)),
                ('publisher', models.CharField(max_length=45)),
                ('publication_year', models.IntegerField()),
                ('cover_picture', models.TextField(default='')),
                ('rating', models.FloatField()),
                ('book_status', models.CharField(max_length=45)),
                ('quantity', models.IntegerField()),
                ('buying_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('minimum_threshold', models.IntegerField()),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField()),
                ('order_date', models.DateField()),
                ('order_time', models.TimeField()),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_no', models.CharField(max_length=20)),
                ('card_type', models.CharField(max_length=45)),
                ('exp_date', models.DateField()),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.CharField(max_length=45)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('discount', models.FloatField()),
            ],
            options={
                'db_table': 'promotion',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Order')),
            ],
            options={
                'db_table': 'transaction',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(blank=True, max_length=45)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('promotion_status', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_billing', to='bookstore.Address')),
                ('payment_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Payment')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_shipping', to='bookstore.Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Promotion'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Profile'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Cart')),
            ],
            options={
                'db_table': 'cart_item',
            },
        ),
        migrations.CreateModel(
            name='BookOrder',
            fields=[
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='bookstore.Book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Order')),
            ],
            options={
                'db_table': 'book_order',
                'unique_together': {('book', 'order')},
            },
        ),
        migrations.CreateModel(
            name='BookCart',
            fields=[
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='bookstore.Book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookstore.Cart')),
            ],
            options={
                'db_table': 'book_cart',
                'unique_together': {('book', 'cart')},
            },
        ),
    ]