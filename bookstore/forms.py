from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import datetime
from .models import Profile, Address, Payment, Promotion

class RegisterForm(UserCreationForm):

    CARD_TYPES = (
        (1, 'Visa'),
        (2, 'MasterCard'),
        (3, 'American Express'),
    )
	# Get user Info
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First name', 'required' : '',}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last name', 'required' : '',}))
    username = forms.CharField(label='Username', min_length=5, max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username', 'required' : '',}))
    phone_number = forms.CharField(label='Phone Number', required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'name' : 'phone', 'placeholder': '123-456-7890', 'pattern':'[0-9]{3}-[0-9]{3}-[0-9]{4}'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'example@uga.edu', 'aria-describedby':'emailHelp', 'required' : ''}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password', 'required' : ''}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Confirm Password', 'required' : ''}))

    # Get Shippinng Address Info
    ship_street = forms.CharField(label='Street', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234 Main St'}))
    ship_city = forms.CharField(label='City', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Athens'}))
    ship_state = forms.CharField(label='State', max_length=2, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'GA'}))
    ship_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '30602', 'onKeyPress':'if(this.value.length==5) return false;'}))

    # Get Billing Address Info
    bill_street = forms.CharField(label='Street', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234 Main St'}))
    bill_city = forms.CharField(label='City', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Athens'}))
    bill_state = forms.CharField(label='State', max_length=2, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'GA'}))
    bill_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '30602', 'onKeyPress':'if(this.value.length==5) return false;'}))

    ship_is_billing = forms.BooleanField(label='Shipping Address is the same as Billing Address', required=False, widget=forms.CheckboxInput(attrs={'class' : 'custom-control-input', 'id':'same-address'}))
    promotion_sign_up = forms.BooleanField(label='Sign Up for Promotions', required=False, widget=forms.CheckboxInput(attrs={'class' : 'custom-control-input', 'id':'promote', 'checked':''}))

    # Get Payment Info
    card_no = forms.CharField(label='Card Number', max_length=20, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '1234567890123456'}))
    card_type = forms.ChoiceField(label='Card Type', choices=CARD_TYPES, required=False, widget=forms.Select(attrs={'class' : 'form-control'}))
    exp_date = forms.CharField(label='Expiration Date', required=False, widget=forms.DateInput(attrs={'class' : 'form-control', 'placeholder' : '02/20'}))

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
            'ship_is_billing', 'promotion_sign_up',
        	'ship_street', 'ship_city', 'ship_state', 'ship_zip_code',
        	'bill_street', 'bill_city', 'bill_state', 'bill_zip_code',
        	'card_no', 'card_type', 'exp_date')

class EditUserForm(UserChangeForm):

    CARD_TYPES = (
        (1, 'Visa'),
        (2, 'MasterCard'),
        (3, 'American Express'),
    )

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First name', 'required' : '', 'value': ''}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last name', 'required' : '',}))
    ship_is_billing = forms.BooleanField(label='Shipping Address is the same as Billing Address', required=False, widget=forms.CheckboxInput(attrs={'class' : 'custom-control-input', 'id':'same-address'}))
    promotion_sign_up = forms.BooleanField(label='Sign Up for Promotions', required=False, widget=forms.CheckboxInput(attrs={'class' : 'custom-control-input', 'id':'promote'}))
    
    ship_street = forms.CharField(label='Street', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234 Main St'}))
    ship_city = forms.CharField(label='City', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Athens'}))
    ship_state = forms.CharField(label='State', max_length=2, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'GA'}))
    ship_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '30602', 'onKeyPress':'if(this.value.length==5) return false;'}))

    bill_street = forms.CharField(label='Street', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234 Main St'}))
    bill_city = forms.CharField(label='City', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Athens'}))
    bill_state = forms.CharField(label='State', max_length=2, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'GA'}))
    bill_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '30602', 'onKeyPress':'if(this.value.length==5) return false;'}))

    card_no = forms.CharField(label='Card Number', max_length=20, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '1234567890123456'}))
    card_type = forms.ChoiceField(label='Card Type', choices=CARD_TYPES, required=False, widget=forms.Select(attrs={'class' : 'form-control'}))
    exp_date = forms.CharField(label='Expiration Date', max_length=20, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '02/20'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'promotion_sign_up',
            'ship_street', 'ship_city', 'ship_state', 'ship_zip_code',
            'bill_street', 'bill_city', 'bill_state', 'bill_zip_code', 'ship_is_billing',
            'card_no', 'card_type', 'exp_date')

class CheckoutForm(forms.ModelForm):

    CARD_TYPES = (
        (1, 'Visa'),
        (2, 'MasterCard'),
        (3, 'American Express'),
    )

    promo_code = forms.CharField(label='Promo Code', required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Promo code', 'value': ''}))

    first_name = forms.CharField(label='First Name', required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First name', 'required' : '', 'value': ''}))
    last_name = forms.CharField(label='Last Name', required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last name', 'required' : '',}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'example@uga.edu', 'aria-describedby':'emailHelp', 'required' : ''}))
    
    ship_is_billing = forms.BooleanField(label='Shipping Address is the same as Billing Address', required=False, widget=forms.CheckboxInput(attrs={'class' : 'custom-control-input', 'id':'ship_is_billing', 'checked':''}))
    ship_street = forms.CharField(label='Street', max_length=45, required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234 Main St'}))
    ship_city = forms.CharField(label='City', max_length=45, required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Athens'}))
    ship_state = forms.CharField(label='State', max_length=2, required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'GA'}))
    ship_zip_code = forms.CharField(label='Zip Code', max_length=5, required=True, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '30602', 'onKeyPress':'if(this.value.length==5) return false;'}))

    bill_street = forms.CharField(label='Street', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '1234 Main St'}))
    bill_city = forms.CharField(label='City', max_length=45, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Athens'}))
    bill_state = forms.CharField(label='State', max_length=2, required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'GA'}))
    bill_zip_code = forms.CharField(label='Zip Code', max_length=5, required=False, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '30602', 'onKeyPress':'if(this.value.length==5) return false;'}))

    card_no = forms.CharField(label='Card Number', max_length=20, required=True, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '1234567890123456'}))
    card_type = forms.ChoiceField(label='Card Type', choices=CARD_TYPES, required=True, widget=forms.Select(attrs={'class' : 'form-control'}))
    exp_date = forms.CharField(label='Expiration Date', max_length=20, required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '02/20'}))

    def clean_bill_street(self):
        if not self.data.get('ship_is_billing'):
            if not self.cleaned_data['bill_street'] or not self.data.get('bill_city') or not self.data.get('bill_state') or not self.data.get('bill_zip_code'):
                raise  ValidationError("Billing address must be completed")
        return self.cleaned_data['bill_street']

    def clean_promo_code(self):
        print(self.data.get('promo_code'))
        if self.data.get('promo_code') and self.data.get('promo_code') != "":
            print('MADE IT')
            if not Promotion.objects.filter(promo_code__iexact=self.data.get('promo_code')):
                raise  ValidationError("Promo code does not exist")
            promo = Promotion.objects.get(promo_code__iexact=self.data.get('promo_code'))
            today = datetime.date.today()
            if today < promo.start_date:
                raise  ValidationError("This promotion has not started. It will start "+str(promo.start_date))
            if today > promo.end_date:
                raise  ValidationError("This promotion ended on "+str(promo.end_date))
        return self.data.get('promo_code')

    class Meta:
        model = User
        fields = ('promo_code', 'first_name', 'last_name', 'email',
            'ship_street', 'ship_city', 'ship_state', 'ship_zip_code',
            'bill_street', 'bill_city', 'bill_state', 'bill_zip_code', 'ship_is_billing',
            'card_no', 'card_type', 'exp_date')