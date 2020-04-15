from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Address, Payment, Book
from .forms import EditUserForm, RegisterForm
from .tokens import confirmation_token
from lib2to3.fixes.fix_input import context
# Create your views here.


def home(request):
    context = {
        'books': Book.objects.all()
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
                return redirect('bookstore_home')
            else:
                username = request.POST.get('email')
                if user.is_active:
                    login(request, user)
                    return redirect('bookstore/edit_profile.html')
                return HttpResponse("Your account is inactive.")
        else:
            print("login attempted and failed.")
            return HttpResponse("invalid login details given")

    else:
        print('Not POST for loginU')
        # return render(request, 'bookstore/home.html', {})


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
                #card_type = form.cleaned_data.get('card_type')
                exp_date = form.cleaned_data.get('exp_date')
                payment = Payment(
                    card_no=card_no, card_type='visa', exp_date=exp_date)
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
                    #card_type = form.cleaned_data.get('card_type')
                    exp_date = form.cleaned_data.get('exp_date')
                    payment = Payment(
                        card_no=card_no, card_type='visa', exp_date=exp_date)
                    payment.save()
                    user.profile.payment_info = payment

            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.save()

            print('saved user '+str(user.username))

            return redirect(reverse('bookstore_home'))

        else:
            print('bad form')
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'bookstore/edit_profile.html', {'form': form})


def book_detail(request, pk=None):
    if pk:
        book = Book.objects.get(pk=pk)
    else:
        book = request.book
    args = {'book': book}
    return render(request, 'bookstore/book_detail.html',context={'book': book})



def search(request):
    return render(request, 'bookstore/search_view.html')


def cart(request):
    return render(request, 'bookstore/shopping_cart.html')


def checkout(request):
    return render(request, 'bookstore/check_out.html')


def history(request):
    return render(request, 'bookstore/history_view.html')
