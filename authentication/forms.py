from .admin import UserCreationForm, UserChangeForm
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm


class UserRegistrationForm(UserCreationForm):
    telephone = PhoneNumberField()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'address', 'telephone', 'occupation', 'is_member', 'is_pastor',
                  'is_worker',)


class UserEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'address', 'telephone', 'occupation', 'password')


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password', 'new_password2')
