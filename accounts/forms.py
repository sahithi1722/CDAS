from django import forms
from .models import User


class UserForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "emp_no",
            "emp_name",
            "password",
            "role",
            "status",
        ]

        widgets = {

            "emp_no": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "emp_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "password": forms.PasswordInput(
                render_value=True,
                attrs={
                    "class": "form-control"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }