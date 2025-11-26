from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["usuario", "nome", "saldo_atual", "tipo", "cor"]
