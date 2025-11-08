from django import forms
from django.core.exceptions import ValidationError

class UserCreationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class GroupCreationForm(forms.Form):
    group_name = forms.CharField(label="Nom du groupe", widget=forms.TextInput(attrs={'class': 'form-control'}))

class AddUserToGroupForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    group_name = forms.CharField(label="Nom du groupe", widget=forms.TextInput(attrs={'class': 'form-control'}))

class AddUserToGroupSudoForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))

class RemoveUserToGroupForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    group_name = forms.CharField(label="Nom du groupe", widget=forms.TextInput(attrs={'class': 'form-control'}))

class DeleteGroupForm(forms.Form):
    group_name = forms.CharField(label="Nom du groupe", widget=forms.TextInput(attrs={'class': 'form-control'}))

class DeleteUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))

class GroupToUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))

class UserToGroupForm(forms.Form):
    group_name = forms.CharField(label="Nom du groupe", widget=forms.TextInput(attrs={'class': 'form-control'}))

class SearchUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Entrez un nom d\'utilisateur'}))

class SearchGroupForm(forms.Form):
    group_name = forms.CharField(label="Nom du groupe", required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Entrez un nom du groupe'}))

class SearchLoggedInUsersForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Entrez un nom d\'utilisateur'}))

class ChangePasswordForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class PasswordForgetForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserInfoForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))


class LogCodeForm(forms.Form):
    code = forms.CharField(label="Code de vérification", widget=forms.TextInput(attrs={'class': 'form-control'}))


ALLOWED_LOG_EMAILS = [
    "admin1@gmail.com",
    "superadmin@example.com",
    "tonadresse@gmail.com",
    "manoach456@gmail.com"
]

class LogInfoForm(forms.Form):
    email = forms.EmailField(label="Adresse email autorisée")

    def clean_email(self):
        email = self.cleaned_data['email']
        if email not in ALLOWED_LOG_EMAILS:
            raise ValidationError("Cette adresse n'est pas autorisée à accéder aux logs.")
        return email

