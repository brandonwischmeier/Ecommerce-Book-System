from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):

	# Get user Info
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name', required=False)
    username = forms.CharField(label='Username', min_length=5, max_length=20)
    phone_number = forms.CharField(label='Phone Number', required=False)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    # Get Shippinng Address Info
    ship_street = forms.CharField(label='Street', max_length=45, required=False)
    ship_city = forms.CharField(label='City', max_length=45, required=False)
    ship_state = forms.CharField(label='State', max_length=2, required=False)
    ship_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False)

    # Get Billing Address Info
    bill_street = forms.CharField(label='Street', max_length=45, required=False)
    bill_city = forms.CharField(label='City', max_length=45, required=False)
    bill_state = forms.CharField(label='State', max_length=2, required=False)
    bill_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False)

    ship_is_billing = forms.BooleanField(label='Shipping Address is the same as Billing Address', required=False)
    promotion_sign_up = forms.BooleanField(label='Sign Up for Promotions', required=False)

    # Get Payment Info
    card_no = forms.CharField(label='Card Number', max_length=20, required=False)
    card_type = forms.CharField(label='Card Type', max_length=45, required=False)
    exp_date = forms.DateField(label='Expiration Date', required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
        	'ship_street', 'ship_city', 'ship_state', 'ship_zip_code',
        	'bill_street', 'bill_city', 'bill_state', 'bill_zip_code', 'ship_is_billing',
        	'card_no', 'card_type', 'exp_date')