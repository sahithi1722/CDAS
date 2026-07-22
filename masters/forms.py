from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = '__all__'

        widgets = {
            'shop_code': forms.TextInput(attrs={'class':'form-control'}),
            'shop_desc': forms.TextInput(attrs={'class':'form-control'}),
            'eqpt_code': forms.TextInput(attrs={'class':'form-control'}),
            'eqpt_name': forms.TextInput(attrs={'class':'form-control'}),
            'sub_eqpt_code': forms.TextInput(attrs={'class':'form-control'}),
            'sub_eqpt_name': forms.TextInput(attrs={'class':'form-control'}),
        }