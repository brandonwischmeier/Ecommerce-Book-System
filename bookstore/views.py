from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate, password_validation
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import random
from .models import Address, Payment, Book, CartItem, Order, OrderItem, Promotion
from django.db.models import Sum
from .forms import EditUserForm, RegisterForm, CheckoutForm
from .tokens import confirmation_token
import base64
import datetime
from lib2to3.fixes.fix_input import context
# Create your views here.


def home(request):
    books = list(Book.objects.all())
    random.shuffle(books)
    books = books[:8]
    context = {
        'books': books
    }
    
    return render(request, 'bookstore/home.html', context)



def loginU(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if request.POST.get('remember_me', None):
                    request.session.set_expiry(60 * 60 * 24 * 14) # 14 days
                else:
                    request.session.set_expiry(0) # 0 days
                if user.is_superuser:
                    return redirect('/admin/')
                return redirect('bookstore_home')
            else:
                username = request.POST.get('email')
                if user.is_active:
                    login(request, user)
                    return redirect('bookstore/edit_profile.html')
                return HttpResponse("Your account is inactive.")
        else:
            print("login attempted and failed.")
            return redirect('login_failure')

    else:
        print('Not POST for loginU')
    return redirect(reverse('bookstore_home'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            # Get shipping addr info
            # If shipping info filled in then save shipping address and save foreign key into user's shipping addr
            if form.cleaned_data.get('ship_street') and form.cleaned_data.get('ship_city') and form.cleaned_data.get('ship_state') and form.cleaned_data.get('ship_zip_code'):

                ship_street = form.cleaned_data.get('ship_street')
                ship_city = form.cleaned_data.get('ship_city')
                ship_state = form.cleaned_data.get('ship_state')
                ship_zip_code = form.cleaned_data.get('ship_zip_code')

                ship_addr = Address(
                    street=ship_street, city=ship_city, state=ship_state, zip_code=ship_zip_code)
                ship_addr.save()
                user.profile.shipping_address = ship_addr

                # If shipping is billing
                if form.cleaned_data.get('shipping_is_billing'):
                    user.profile.billing_address = ship_addr
                # If billing address filled in, save billing address and save foreign key into user's billing addr
                elif form.cleaned_data.get('bill_street') and form.cleaned_data.get('bill_city') and form.cleaned_data.get('bill_state') and form.cleaned_data.get('bill_zip_code'):

                    bill_street = form.cleaned_data.get('bill_street')
                    bill_city = form.cleaned_data.get('bill_city')
                    bill_state = form.cleaned_data.get('bill_state')
                    bill_zip_code = form.cleaned_data.get('bill_zip_code')

                    bill_addr = Address(
                        street=bill_street, city=bill_city, state=bill_state, zip_code=bill_zip_code)
                    bill_addr.save()
                    user.profile.billing_address = bill_addr

            if form.cleaned_data.get('card_no') and form.cleaned_data.get('exp_date'):

                card_no = form.cleaned_data.get('card_no')
                card_type = form.cleaned_data.get('card_type')
                exp_date = form.cleaned_data.get('exp_date')
                payment = Payment(
                    card_no=base64.b64encode(bytes(card_no, 'ascii')), card_type=card_type, exp_date=base64.b64encode(bytes(exp_date, 'ascii')))
                payment.save()
                user.profile.payment_info = payment

            # Get user info
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.phone_number = form.cleaned_data.get('phone_number')

            # Set user to inactive and send email confirmation
            user.is_active = False
            user.save()
            print('saved user '+str(user.username))
            current_site = get_current_site(request)
            subject = 'Please Confirm Your Email'

            message = render_to_string('bookstore/registration_confirmation_to_console.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': confirmation_token.make_token(user),
            })

            user.email_user(subject, message)
            print('redirecting to registration_confirmation ')
            return redirect('registration_confirmation')
        else:
            print('bad form')
    else:
        form = RegisterForm()
    return render(request, 'bookstore/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and confirmation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'bookstore/activation_confirmation.html')
    else:
        return render(request, 'bookstore/activation_invalid.html')


def confirmation(request):
    return render(request, 'bookstore/registration_confirmation.html')

def login_failure(request):
    return render(request, 'bookstore/login_failure.html')

@login_required
def special(request):
    return HttpResponse("You're already logged into an account.")


@login_required
def logoutU(request):
    logout(request)
    return redirect(reverse('bookstore_home'))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)

        print('request POST:')
        print(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            if form.cleaned_data.get('ship_street') and form.cleaned_data.get('ship_city') and form.cleaned_data.get('ship_state') and form.cleaned_data.get('ship_zip_code'):
                ship_street = form.cleaned_data.get('ship_street')
                ship_city = form.cleaned_data.get('ship_city')
                ship_state = form.cleaned_data.get('ship_state')
                ship_zip_code = form.cleaned_data.get('ship_zip_code')

                ship_addr = Address(
                    street=ship_street, city=ship_city, state=ship_state, zip_code=ship_zip_code)
                ship_addr.save()
                user.profile.shipping_address = ship_addr

                # If shipping is billing
                if form.cleaned_data.get('shipping_is_billing'):
                    user.profile.billing_address = ship_addr
                # If billing address filled in, save billing address and save foreign key into user's billing addr
                elif form.cleaned_data.get('bill_street') and form.cleaned_data.get('bill_city') and form.cleaned_data.get('bill_state') and form.cleaned_data.get('bill_zip_code'):

                    bill_street = form.cleaned_data.get('bill_street')
                    bill_city = form.cleaned_data.get('bill_city')
                    bill_state = form.cleaned_data.get('bill_state')
                    bill_zip_code = form.cleaned_data.get('bill_zip_code')

                    bill_addr = Address(
                        street=bill_street, city=bill_city, state=bill_state, zip_code=bill_zip_code)
                    bill_addr.save()
                    user.profile.billing_address = bill_addr

                if form.cleaned_data.get('card_no') and form.cleaned_data.get('exp_date'):
                    card_no = form.cleaned_data.get('card_no')
                    card_type = form.cleaned_data.get('card_type')
                    exp_date = form.cleaned_data.get('exp_date')
                    payment = Payment(
                        card_no=base64.b64encode(bytes(card_no, 'ascii')), card_type=card_type, exp_date=base64.b64encode(bytes(exp_date, 'ascii')))
                    payment.save()
                    user.profile.payment_info = payment

            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.save()

            subject = '[OBS] Your profile has been changed.'
            message = 'Hi' + user.profile.first_name + ',<br><br>your profile has been changed.'

            user.email_user(subject, message)

            print('saved user '+str(user.username))

            return redirect(reverse('bookstore_home'))

        else:
            print('bad form')
    else:
        form = EditUserForm(instance=request.user)

    form.fields['promotion_sign_up'].initial = request.user.profile.promotion_status

    if request.user.profile.shipping_address:
        form.fields['ship_street'].initial = request.user.profile.shipping_address.street
        form.fields['ship_city'].initial = request.user.profile.shipping_address.city
        form.fields['ship_state'].initial = request.user.profile.shipping_address.state
        form.fields['ship_zip_code'].initial = request.user.profile.shipping_address.zip_code

    if request.user.profile.billing_address:
        form.fields['bill_street'].initial = request.user.profile.billing_address.street
        form.fields['bill_city'].initial = request.user.profile.billing_address.city
        form.fields['bill_state'].initial = request.user.profile.billing_address.state
        form.fields['bill_zip_code'].initial = request.user.profile.billing_address.zip_code

    if request.user.profile.payment_info:

        form.fields['card_no'].initial = str(base64.b64decode(request.user.profile.payment_info.card_no[2:-1]))[2:-1]
        form.fields['exp_date'].initial = str(base64.b64decode(request.user.profile.payment_info.exp_date[2:-1]))[2:-1]
        form.fields['card_type'].initial = request.user.profile.payment_info.card_type

    return render(request, 'bookstore/edit_profile.html', {'form': form})

@login_required
def edit_password(request):

    if request.method == 'POST':
        currPass = request.POST.get('currPass')
        newPass = request.POST.get('newPass')
        newPass2 = request.POST.get('newPass2')

        if currPass and newPass and newPass2:
            print('curr pass: '+currPass)
            print('new pass: '+newPass)
            print('new pass 2: '+newPass2)
            if newPass == newPass2:
                try:
                    password_validation.validate_password(newPass)
                    user = authenticate(username=request.user.username, password=currPass)
                    if user:
                        user.set_password(newPass)
                        user.save()
                        login(request, user)
                    
                    print('set new password to: '+newPass)
                    return redirect(reverse('edit_profile'))
                except ValidationError:
                    messages.add_message(request, messages.ERROR, "Please enter a valid password")
            else:
                messages.add_message(request, messages.ERROR, "Password 1 and 2 do not match")
    return render(request, 'bookstore/change_password.html')


def book_detail(request, pk=None):
    if pk:
        book = Book.objects.get(pk=pk)
    else:
        book = request.book
    return render(request, 'bookstore/book_detail.html',context={'book': book})


def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        search_text_top = request.POST.get('search_text_top')
        radio_group = request.POST.get('search-radio-group')

        if search_text_top:
            results = Book.objects.filter(category__icontains=search_text_top).distinct()
            print('got subject results seaching with: '+search_text_top)

        if search_text and radio_group == 's':
            results = Book.objects.filter(category__icontains=search_text).distinct()
            print('got subject results seaching with: '+search_text)

        if search_text and radio_group == 't': #Book Title
            results = Book.objects.filter(title__icontains=search_text).distinct()
            print('got title results seaching with: '+search_text)

        elif search_text and radio_group == 'a': #Author
            results = Book.objects.filter(author__icontains=search_text).distinct()
            print('got author results seaching with: '+search_text)

        elif search_text and radio_group == 'i': #ISBN
            results = Book.objects.filter(isbn__icontains=search_text).distinct()
            print('got isbn results seaching with: '+search_text)
        else:
            results = []
        
    else:
        results = Book.objects.all()

    paginator = Paginator(results, 5)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'bookstore/search_view.html', {'books': books})

@login_required
def add_to_cart(request, pk=None):
    if pk:
        book = Book.objects.get(pk=pk)
    
    if book:
        user = request.user
        
        quantity=request.POST.get('quantity')
        if quantity!='':
            quantity = int(quantity)
            if book.quantity - quantity >= book.minimum_threshold:

                try: 

                    item = CartItem.objects.get(user=user, book=book)

                except ObjectDoesNotExist:

                    cartItem = CartItem(user=user, book=book, quantity=quantity)
                    cartItem.save()
                    return render(request, 'bookstore/book_detail.html', {'book': book})

                except MultipleObjectsReturned:

                    print('multiple found, should never happen')

                item.quantity += quantity
                item.save()
                
            else:
                messages.add_message(request, messages.ERROR, "Not enough books in stock. Only {0} left".format(book.quantity - book.minimum_threshold))

            
    return render(request, 'bookstore/book_detail.html', {'book': book})


@login_required
def cart(request, pk=None):
    if request.method == 'POST':
        quantity=request.POST.get('quantity')
        book = Book.objects.get(pk=pk)
        if quantity!='':
            quantity = int(quantity)
            if book:
                if book.quantity - quantity >= book.minimum_threshold:
                    try: 
                        item = CartItem.objects.get(user=request.user, book=Book.objects.get(pk=pk))
                    except ObjectDoesNotExist:
                        print('none found')
                    except MultipleObjectsReturned:
                        print('multiple found')
                    item.quantity=quantity
                    item.save()
                else:
                    messages.add_message(request, messages.ERROR, "Not enough books in stock. Only {0} left".format(book.quantity - book.minimum_threshold))
            else:
                print('could not find book with given pk')
        else:
            print('empty quantity not allowed')

    items = CartItem.objects.filter(user=request.user)

    total = 0.0
    for item in items:
        total += item.book.selling_price * item.quantity
    
    return render(request, 'bookstore/shopping_cart.html', {'items': items, 'total': total})

@login_required
def remove(request, pk=None):
    if pk:
        book = Book.objects.get(pk=pk)
    if book:
        user = request.user

        try: 

            item = CartItem.objects.get(user=user, book=book)

        except ObjectDoesNotExist:

            print('cart item does not exist, should never happen')

        except MultipleObjectsReturned:

            print('multiple found, should never happen')

        item.delete()
    return redirect(reverse('shopping_cart'))



@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=request.user)

        if form.is_valid():
            print('form valid')
            card_no = form.cleaned_data.get('card_no')
            card_type = form.cleaned_data.get('card_type')
            exp_date = form.cleaned_data.get('exp_date')
            
            payment = Payment(
                card_no=base64.b64encode(bytes(card_no, 'ascii')), card_type=card_type, exp_date=base64.b64encode(bytes(exp_date, 'ascii')))
            payment.save()

            print('saved payment info at: ' + str(payment))

            total = 0.0
            for item in items:
                total += item.book.selling_price * item.quantity

            if form.cleaned_data.get('promo_code') and form.cleaned_data.get('promo_code') != "":
                print('searching for promo_code: ' + str(form.cleaned_data.get('promo_code')))
                promotion = Promotion.objects.filter(promo_code=form.cleaned_data.get('promo_code'))
                total -= float(promotion.discount) * total
            else:
                promotion = None

            order = Order(user=request.user, payment=payment, promotion=promotion, total_price=total, order_date=datetime.date.today(), order_time=datetime.datetime.now().time())
            order.save()

            print('saved order info at: ' + str(order))

            for item in items:
                book = Book.objects.get(pk=item.book.pk)
                book.quantity -= item.quantity
                book.save()
                orderItem = OrderItem(order=order, book=item.book, quantity=item.quantity)
                orderItem.save()

                print('saved order item at: {0}, removed {1} \"{2}\", only {3} left!'.format(str(orderItem), str(item.quantity), str(book.title), str(book.quantity)))

            items.delete()

            return render(request, 'bookstore/checkout_success.html', {'total': total})

        else:
            print('form invalid')
    else:
        form = CheckoutForm(instance=request.user)

    if request.user.profile.shipping_address:
        form.fields['ship_street'].initial = request.user.profile.shipping_address.street
        form.fields['ship_city'].initial = request.user.profile.shipping_address.city
        form.fields['ship_state'].initial = request.user.profile.shipping_address.state
        form.fields['ship_zip_code'].initial = request.user.profile.shipping_address.zip_code

    if request.user.profile.billing_address:
        form.fields['bill_street'].initial = request.user.profile.billing_address.street
        form.fields['bill_city'].initial = request.user.profile.billing_address.city
        form.fields['bill_state'].initial = request.user.profile.billing_address.state
        form.fields['bill_zip_code'].initial = request.user.profile.billing_address.zip_code

    if request.user.profile.payment_info:
        form.fields['card_no'].initial = str(base64.b64decode(request.user.profile.payment_info.card_no[2:-1]))[2:-1]
        form.fields['exp_date'].initial = str(base64.b64decode(request.user.profile.payment_info.exp_date[2:-1]))[2:-1]
        form.fields['card_type'].initial = request.user.profile.payment_info.card_type

    return render(request, 'bookstore/check_out.html', {'form': form})

def checkout_success(request):
    return render(request, 'bookstore/checkout_success.html')

def history(request):
    return render(request, 'bookstore/history_view.html')