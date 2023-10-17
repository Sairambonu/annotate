from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserLoginInfo

# class UserForm(UserCreationForm):
#     # Extend the default UserCreationForm with additional fields
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = UserLoginInfo
        fields = ['usermame', 'password']

# class UserRegisterForm(UserCreationForm):
#     # Extend the custom form with additional permissions
#     email = forms.EmailField(required=True)
#     user_role = forms.CharField(max_length=20, required=False, empty_value="annotator")
#     contact = forms.CharField(max_length=20, min_length=10, required=False)
#     # Add more custom permissions fields if needed

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'user_role', 'contact']


class UserRegisterForm(UserCreationForm):
    # Extend the custom form with additional permissions
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=True)
    role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
        choices=(
            ('annotator', 'annotator'),
            ('evaluator', 'evaluator'),
            ('coordinator', 'coordinator'),
            )
        )
    phone = forms.CharField(max_length=12, min_length=10, required=False)
    # Add more custom permissions fields if needed
    languages = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ('telugu', 'telugu'),
            ('hindi', 'hindi'),
            ('marathi', 'marathi'),
        ),
        required=False,  # Not required as checkboxes can be left unselected
    )
    def clean(self):
        cleaned_data = super().clean()
        languages = cleaned_data.get('languages', [])

        if not languages:
            raise forms.ValidationError("Please select at least one language.")

    class Meta:
        model = UserLoginInfo
        fields = ['username', 'email', 'languages','status','role','phone']