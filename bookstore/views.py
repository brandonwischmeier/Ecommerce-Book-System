from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Address
from .forms import RegisterForm
# Create your views here.
def home(request):
    return render(request, 'bookstore/home.html')

def register(request):
	if request.method == 'POST':
	    form = RegisterForm(request.POST)
	    if form.is_valid():
	        user = form.save()
	        user.refresh_from_db()

	        #Get shipping addr info
	        #If shipping info filled in then save shipping address and save foreign key into user's shipping addr
	        if form.cleaned_data.get('ship_street') and form.cleaned_data.get('ship_city') and form.cleaned_data.get('ship_state') and form.cleaned_data.get('ship_zip_code'):

	            ship_street = form.cleaned_data.get('ship_street')
	            ship_city = form.cleaned_data.get('ship_city')
	            ship_state = form.cleaned_data.get('ship_state')
	            ship_zip_code = form.cleaned_data.get('ship_zip_code')

	            ship_addr = Address(street=ship_street, city=ship_city, state=ship_state, zip_code=ship_zip_code)
	            ship_addr.save()
	            user.profile.shipping_address = ship_addr

	            # If shipping is billing
	            if form.cleaned_data.get('shipping_is_billing'):
	                user.profile.billing_address = ship_addr
	            # If billing address filled in, save billing address and save foreign key into user's billing addr
	            elif form.cleaned_data.get('bill_street') and form.cleaned_data.get('ship_city') and form.cleaned_data.get('ship_state') and form.cleaned_data.get('ship_zip_code'):

	                bill_street = form.cleaned_data.get('bill_street')
	                bill_city = form.cleaned_data.get('bill_city')
	                bill_state = form.cleaned_data.get('bill_state')
	                bill_zip_code = form.cleaned_data.get('bill_zip_code')

	                bill_addr = Address(street=bill_street, city=bill_city, state=bill_state, zip_code=bill_zip_code)
	                bill_addr.save()
	                user.profile.shipping_address = bill_addr

	        #Get user info
	        user.profile.first_name = form.cleaned_data.get('first_name')
	        user.profile.last_name = form.cleaned_data.get('last_name')
	        user.profile.phone_number = form.cleaned_data.get('phone_number')
	        user.profile.last_name = form.cleaned_data.get('last_name')
	        user.profile.username = form.cleaned_data.get('username')
	        user.profile.phone_number = form.cleaned_data.get('phone_number')


	        user.profile.email = form.cleaned_data.get('email')
	        user.save()
	        username = form.cleaned_data.get('username')
	        password = form.cleaned_data.get('password2')
	        user = authenticate(username=username, password=password)
	        return redirect('.')
	else:
	    form = RegisterForm()
	return render(request, 'bookstore/register.html', {'form': form})

def confirmation(request):
    return render(request, 'bookstore/registration_confirmation.html')

def book_detail(request):
    return render(request, 'bookstore/book_detail.html')

def search(request):
    return render(request, 'bookstore/search_view.html')

def cart(request):
    return render(request, 'bookstore/shopping_cart.html')

def checkout(request):
    return render(request, 'bookstore/check_out.html')

def history(request):
    return render(request, 'bookstore/history_view.html')