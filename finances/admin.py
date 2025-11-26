from django.contrib import admin

from accounts.models import Account
from .models import Categoria, Transacao

admin.site.register(Categoria)
admin.site.register(Transacao)
