# python -m pip install Faker

import pickle
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt-br')

class Produto:
  def __init__(self, nome: str, preco_compra: float, preco_venda: float):
    self.nome = nome
    self.preco_compra = preco_compra
    self.preco_venda = preco_venda
    self.data_compra = fake.date_between(datetime.now() + timedelta(days=-30), datetime.now()).isoformat()
    self.data_vencimento = fake.date_between(datetime.now(), datetime.now() + timedelta(days=30)).isoformat()

  def __repr__(self):
    return f'produto "{self.nome}", R$ {self.preco_compra} (compra), R$ {self.preco_venda} (venda), {self.data_compra} (aquisicao), {self.data_vencimento} (validade)'

class Pagamento:
  def __init__(self, produto, cliente, data_hora):
    self.produto = produto
    self.cliente = cliente
    self.data_hora = data_hora

class Consumo:
  def __init__(self, cliente, produto, pagamento):
    self.cliente = cliente
    self.produto = produto
    self.pagamento = pagamento

class PickleManager():
  def __init__(self, arquivo):
    self.arquivo = arquivo
    self.dados = list()
    self.dump()

  def load(self):
    with open(self.arquivo, 'rb') as f:
      self.dados = pickle.load(f)

  def dump(self):
    with open(self.arquivo, 'wb') as f:
      pickle.dump(self.dados, f)

class Lista(PickleManager):
  def adicionar(self, item):
    self.load()
    self.dados.append(item)
    self.dump()

  def listar(self):
    self.load()
    return [s for s in self.dados]

class Estoque(Lista):
  def __init__(self):
    super().__init__('estoque.pkl')

  def remover_produto(self, produto: Produto, quantidade = 1):
    self.load()

    for ix, p in enumerate(self.dados):
      if p.produto.nome == produto.nome:
        if p.quantidade - quantidade >= 0:
          self.dados[ix].quantidade -= quantidade
          print_title(f'{quantidade} {plural(quantidade, 'itens', 'item')} do produto "{produto.nome}" removido{plural(quantidade)} do estoque')
          return True
        else:
          quantidade_invalida()

    self.dump()
    return False
  
class Carrinho(Lista):
  def __init__(self):
    super().__init__('carrinho.pkl')

class Pagamentos(Lista):
  def __init__(self):
    super().__init__('pagamentos.pkl')

class Consumos(Lista):
  def __init__(self):
    super().__init__('consumos.pkl')

class Cliente():
  def __init__(self, nome):
    self.nome = nome

class ItemEstoque():
  def __init__(self, produto: Produto, quantidade = 1):
    self.produto = produto
    self.quantidade = quantidade

  def __repr__(self):
    return f'{self.produto} ({self.quantidade} {plural(self.quantidade, 'itens', 'item')})'
  
class ItemCarrinho():
  def __init__(self, produto: Produto, quantidade = 1):
    self.produto = produto
    self.quantidade = quantidade

  def __repr__(self):
    return f'{self.produto} ({self.quantidade} {plural(self.quantidade, 'itens', 'item')})'
  
class Cantina:
  def __init__(self):
    self.estoque = Estoque()
    self.carrinho = Carrinho()
    self.pagamentos = Pagamentos()
    self.consumos = Consumos()
    self.cliente = None

  def adicionar_estoque(self, produto: Produto, quantidade = 1):
    self.estoque.adicionar(ItemEstoque(produto, quantidade))
    print_title(f'produto "{produto.nome}" adiconado ao estoque')

  def remover_estoque(self, produto: Produto, quantidade = 1):
    self.estoque.remover_produto(produto, quantidade)

  def listar_estoque(self) -> list[ItemEstoque]:
    return self.estoque.listar()
  
  def ver_cliente():
    pass

  def escolher_cliente(self):
    while True:
      print_title('cliente')
      nome = input_parsed('nome')
      if nome:
        return Cliente(nome)

  def adicionar_cliente(self, cliente):
    self.cliente = cliente

  def escolher_estoque(self) -> ItemEstoque:
    return escolher('estoque', self.listar_estoque())

  def quantidade_produtos(self):
    return sum([1 for _ in self.estoque.listar()])

  def adicionar_carrinho(self, produto: Produto, quantidade = 1):
    self.carrinho.adicionar(ItemCarrinho(produto, quantidade))
    print_title(f'produto "{produto.nome}" adiconado ao carrinho')

  def listar_carrinho(self):
    return self.carrinho.listar()
  
  def escolher_carrinho(self):
    return escolher('carrinho', self.listar_carrinho())

  def remover_carrinho(self, produto, quantidade):
    pass

# # auxiliar

def print_title(title):
  print(f'[ {title} ]')

def escolher(title, items):
  while True:
    print_title(title)
    print('0. sair')
    [print(f'{ix+1}. {p}') for ix, p in enumerate(items)]
    try:
      item = int(input('> ')) # valida escolha como numero
      return item, items[item-1] # retorna como texto
    except:
      print_title('item não encontrado')
      return item, None

def quantidade_invalida():
  print_title('quantidade não pode ser menor que 0')

def plural(num, muitostr = 's', poucostr = ''):
  return muitostr if num > 1 else poucostr

def input_parsed(txt, parser = str):
  return parser(input(f'{txt}: '))

def menu():
  cantina = Cantina()

  while True:
    opcoes = ['adicionar produto ao estoque','remover produto do estoque','ver estoque','adicionar produto ao carrinho','remover produto do carrinho','ver carrinho','finalizar carrinho','extrair relatorio de vendas','extrair relatorio de consumos']

    opcao, titulo = escolher('menu', opcoes)

    print_title(titulo)

    match str(opcao):
      case '1':
        nome = input_parsed('nome')
        preco_compra = input_parsed('preco de compra', float)
        preco_venda = input_parsed('preco de venda', float)
        quantidade = input_parsed('quantidade', int)
        produto = Produto(nome, preco_compra, preco_venda)
        cantina.adicionar_estoque(produto, quantidade)
        continue
      case '2':
        _, produto = cantina.escolher_estoque()
        quantidade = input_parsed('quantidade', int)
        cantina.remover_estoque(produto.produto, quantidade)
        continue
      case '3':
        [print(p) for p in cantina.listar_estoque()]
        continue
      case '4':
        _, produto = cantina.escolher_estoque()
        quantidade = input_parsed('quantidade', int)
        if cantina.remover_estoque(produto.produto, quantidade):
          cantina.adicionar_carrinho(produto.produto, quantidade)
        continue
      case '5':
        _, produto = cantina.escolher_carrinho()
        quantidade = input_parsed('quantidade', int)
        if cantina.remover_carrinho(produto.produto, quantidade):
          cantina.adicionar_estoque(produto.produto, quantidade)
        continue
      case '6':
        [print(p) for p in cantina.listar_carrinho()]
        continue
      case '7':
        # _, pagamento = cantina.escolher_pagamento()
        cliente = input_parsed('nome do cliente')
        produtos = cantina.listar_carrinho()
        # cantina.adicionar_pagamento(ItemPagamento(pagamento, produtos))
        # cantina.adicionar_consumo(ItemConsumo(cliente, produtos))
        continue
      case '8':
        # [print(f'{ix+1}. {p}') for ix, p in enumerate(cantina.listar_pagamentos())]
        continue
      case '9':
        # [print(f'{ix+1}. {p}') for ix, p in enumerate(cantina.listar_consumos())]
        continue
      case '0':
        exit(0)
  
menu()
