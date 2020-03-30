from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'bookstore/home.html')

def register(request):
	return render(request, 'bookstore/register.html')

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