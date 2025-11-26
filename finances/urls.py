from django.urls import path

from accounts.views import AccountViewSet
from .views import (
    CategoriaListCreateView,
    CategoriaDetailView,
    TransacaoListCreateView,
    TransacaoDetailView,
    CriarCompraParceladaView,
)

# Mapeamento manual do ViewSet (DRF)
account_list_api = AccountViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

account_detail_api = AccountViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Categorias
    path("categorias/", CategoriaListCreateView.as_view(), name="categoria-list"),
    path("categorias/<int:pk>/", CategoriaDetailView.as_view(), name="categoria-detail"),

    # Transações
    path("transacoes/", TransacaoListCreateView.as_view(), name="transacao-list"),
    path("transacoes/<int:pk>/", TransacaoDetailView.as_view(), name="transacao-detail"),
    path("transacoes/parcelada/", CriarCompraParceladaView.as_view()),

    # Accounts API (DRF)
    path('accounts/', account_list_api, name='api_account_list'),
    path('accounts/<int:pk>/', account_detail_api, name='api_account_detail'),
]
