from django import forms
from .models import ToolDate, ToolDateDetails


class TooldateForm(forms.ModelForm):
    class Meta:
        model = ToolDate
        fields = ['lst_extra_hours', 'start_date']