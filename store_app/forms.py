from django import forms
from django.contrib.auth.models import User, Group


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Roles"
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups']
        help_texts = {
            'is_staff': "Designates whether this user can log into the admin site (not your custom admin, but Django's main admin).",
            'is_active': "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()

        return user

class UserEditForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Roles"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {
            'name': 'Role Name'
        }