
from .models import Titulo, Cliente


def criar_titulos():
    clientes = Cliente.objects.all()
    for cliente in clientes:
        Titulo.objects.create(cliente=cliente, descricao='Título gerado via API')
    return f"{clientes.count()} títulos criados"
 


