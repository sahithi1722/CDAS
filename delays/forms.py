from django import forms
from .models import Delay

class DelayForm(forms.ModelForm):

    class Meta:

        model = Delay

        exclude = ("entered_by","timestamp","delay_duration")
        fields = [
            'shop',
            'equipment',
            'sub_equipment',
            'agency',
            'delay_from',
            'delay_upto',
            'delay_desc',
            'entered_by'
        ]

        widgets={

            "shop_code":forms.HiddenInput(),

            "shop_desc":forms.Select(attrs={"class":"form-select"}),

            "eqpt_name":forms.Select(attrs={"class":"form-select"}),

            "sub_eqpt_name":forms.Select(attrs={"class":"form-select"}),

            "agency":forms.Select(attrs={"class":"form-select"}),

            "delay_from":forms.DateTimeInput(
                attrs={
                    "type":"datetime-local",
                    "class":"form-control"
                }
            ),

            "delay_upto":forms.DateTimeInput(
                attrs={
                    "type":"datetime-local",
                    "class":"form-control"
                }
            ),

            "delay_desc":forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":4
                }
            ),

        }