# python -m pip install Faker

import pickle
from faker import Faker
from datetime import datetime

fake = Faker('pt-br')

class Produto:
  def __init__(self, nome: str, preco_compra: float, preco_venda: float):
    self.nome = nome
    self.preco_compra = preco_compra
    self.preco_venda = preco_venda
    Faker.seed(0)
    self.data_compra = f'{datetime.year}-{datetime.month}-01'
    Faker.seed(0)
    self.data_vencimento = fake.future_date().isoformat()

  def __repr__(self):
    return f'nome: {self.nome}, preco_compra: {self.preco_compra}, preco_venda: {self.preco_venda}, data_compra: {self.data_compra}, data_vencimento: {self.data_vencimento}'

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
          print(f'{quantidade} {plural(quantidade, 'itens', 'item')} do produto "{produto.nome}" removido{plural(quantidade)} do estoque')
        else:
          print('--- quantidade não pode ser menor que 0 ---')

    self.dump()
  
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
    return f'{self.produto.nome} ({self.quantidade} {plural(self.quantidade, 'itens', 'item')})'
  
class Cantina:
  def __init__(self):
    self.estoque = Estoque()
    self.carrinho = Carrinho()
    self.pagamentos = Pagamentos()
    self.consumos = Consumos()
    self.cliente = None

  def adicionar_estoque(self, produto: Produto, quantidade = 1):
    self.estoque.adicionar(ItemEstoque(produto, quantidade))
    print(f'--- produto "{produto.nome}" adiconado ao estoque ---')

  def remover_estoque(self, item: ItemEstoque, quantidade = 1):
    self.estoque.remover_produto(item.produto, quantidade)

  def listar_estoque(self):
    return self.estoque.listar()
  
  def ver_cliente():
    pass

  def escolher_cliente(self):
    while True:
      print('--- cliente ---')
      nome = input_data('nome')
      if nome:
        return Cliente(nome)

  def adicionar_cliente(self, cliente):
    self.cliente = cliente

  def escolher_estoque(self):
    while True:
      print('--- estoque ---')
      produtos = self.listar_estoque()
      [print(f'{ix+1}. {p}') for ix, p in enumerate(produtos)]
      try:
        item = int(input('> '))
        return produtos[item-1]
      except:
        print('--- produto não encontrado ---')

  def quantidade_produtos(self):
    return sum([1 for _ in self.estoque.listar()])

  def adicionar_carrinho(self, produto, quantidade):
    pass

  def listar_carrinho(self):
    return self.carrinho.listar()
  
  def escolher_carrinho(self):
    pass

  def remover_carrinho(self, produto, quantidade):
    pass

# # auxiliar

def plural(num, muitostr = 's', poucostr = ''):
  return muitostr if num > 1 else poucostr

def input_data(txt, parser = str):
  return parser(input(f'{txt}: '))

def menu():
  cantina = Cantina()

  while True:
    print('-- menu --')
    print('1. adicionar produto ao estoque')
    print('2. remover produto do estoque')
    print('3. ver estoque')
    print('4. adicionar produto ao carrinho')
    print('5. remover produto do carrinho')
    print('6. ver carrinho')
    print('7. finalizar carrinho')
    print('8. extrair relatorio de vendas')
    print('9. extrair relatorio de consumos')
    print('0. sair')
  
    opcao = input('> ')

    match opcao:
      case '1':
        print('--- adicionar produto ao estoque ---')
        nome = input_data('nome')
        preco_compra = input_data('preco de compra', float)
        preco_venda = input_data('preco de venda', float)
        quantidade = input_data('quantidade', int)
        
        produto = Produto(nome, preco_compra, preco_venda)

        cantina.adicionar_estoque(produto, quantidade)
        continue
      case '2':
        print('--- remover produto do estoque ---')
        produto: ItemEstoque = cantina.escolher_estoque()
        quantidade = input_data('quantidade', int)
        cantina.remover_estoque(produto, quantidade)
        continue
      case '3':
        print('--- ver estoque ---')
        [print(f'{ix+1}. {p}') for ix, p in enumerate(cantina.listar_estoque())]
        continue
      case '4':
        print('--- adicionar produto ao carrinho ---')
        produto: ItemEstoque = cantina.escolher_estoque()
        quantidade = input_data('quantidade', int)
        cantina.adicionar_carrinho(produto, quantidade)
        cantina.remover_estoque(produto, quantidade)
        continue
      case '5':
        print('--- remover produto do carrinho ---')
        produto: ItemEstoque = cantina.escolher_carrinho()
        quantidade = input_data('quantidade', int)
        cantina.remover_carrinho(produto, quantidade)
        cantina.adicionar_estoque(produto, quantidade)
        continue
      case '6':
        print('--- ver carrinho ---')
        continue
      case '7':
        print('--- finalizar carrinho ---')
        continue
      case '8':
        print('--- relatorio de vendas ---')
        continue
      case '9':
        print('--- relatorio de consumos ---')
        continue
      case '0':
        print('-- sair --')
        exit(0)
  
menu()
