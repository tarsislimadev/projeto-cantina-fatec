# python -m pip install Faker

import pickle
from faker import Faker
from datetime import datetime, timedelta
from text import print_title, opcao_invalida, plural, input_parsed

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

class Cliente():
  def __init__(self, nome: str, tipo: str, curso: str, periodo: str):
    self.nome = nome
    self.tipo = tipo
    self.curso = curso
    self.periodo = periodo

  def __repr__(self) -> str:
    match self.tipo:
      case 'aluno':
        return f'cliente "{self.nome}", aluno (tipo), {self.curso} (curso), {self.periodo} (periodo)'
      case 'professor':
        return f'cliente "{self.nome}", professor (tipo), {self.curso} (curso)'
      case 'funcionario':
        return f'cliente "{self.nome}", funcionario (tipo)'
    return f''

class Pagamento:
  def __init__(self, produto: Produto, cliente: Cliente, data_hora: datetime):
    self.produto = produto
    self.cliente = cliente
    self.data_hora = data_hora

class DataManager():
  def __init__(self, arquivo):
    self.arquivo = arquivo
    self.dados = list()

class Lista(DataManager):
  def adicionar(self, item):
    self.dados.append(item)

  def listar(self):
    return [s for s in self.dados]

class ListaProdutos(Lista):
  def adicionar_produto(self, produto: Produto, quantidade = 1) -> bool:
    for p in self.dados:
      if f'{p.produto}' == f'{produto}':
        p.quantidade += quantidade
        print_title(f'adicionado {quantidade} {plural(quantidade, 'itens', 'item')}: {produto}')
        return True
    return False

  def remover_produto(self, produto: Produto, quantidade = 1) -> bool:
    for p in self.dados:
      if f'{p.produto}' == f'{produto}':
        if p.quantidade - quantidade >= 0:
          p.quantidade -= quantidade
          print_title(f'removido {quantidade} {plural(quantidade, 'itens', 'item')}: {produto}')
          return True
        else:
          opcao_invalida()
    return False
  
class Estoque(ListaProdutos):
  def __init__(self):
    super().__init__('estoque.pkl')

  def adicionar_produto(self, produto: Produto, quantidade = 1) -> bool:
    if not super().adicionar_produto(produto, quantidade):
      self.dados.append(ItemEstoque(produto, quantidade))
      return True
    return False

class Carrinho(ListaProdutos):
  def __init__(self):
    super().__init__('carrinho.pkl')

  def limpar(self):
    self.dados.clear()

  def adicionar_produto(self, produto: Produto, quantidade = 1) -> bool:
    if not super().adicionar_produto(produto, quantidade):
      self.dados.append(ItemCarrinho(produto, quantidade))
      return True
    return False

class Pagamentos(Lista):
  def __init__(self):
    super().__init__('pagamentos.pkl')

class Consumos(Lista):
  def __init__(self):
    super().__init__('consumos.pkl')

class Item:
  def __init__(self):
    self.datahora = datetime.now().isoformat().split('T')[0]

class ItemProduto(Item):
  def __init__(self, produto: Produto, quantidade = 1):
    super().__init__()
    self.produto = produto
    self.quantidade = quantidade

  def __repr__(self) -> str:
    return f'{self.produto} ({self.quantidade} {plural(self.quantidade, 'itens', 'item')})'
  
class ItemEstoque(ItemProduto):
  pass

class ItemCarrinho(ItemProduto):
  pass
  
class ItemPagamento(Item):
  def __init__(self, pagamento: Pagamento, produtos = [], total = 0):
    super().__init__()
    self.pagamento = pagamento
    self.produtos = produtos
    self.total = total

  def __repr__(self):
    return f'pagamento "{self.datahora}", {self.pagamento} (pagamento), R$ {self.total} (total), {len(self.produtos)} (produtos)'

class ItemConsumo(Item):
  def __init__(self, cliente: Cliente, produtos: list[ItemCarrinho] = []):
    super().__init__()
    self.cliente = cliente
    self.produtos = produtos

  def __repr__(self):
    itens = ', '.join([f'"{p.produto.nome}"' for p in self.produtos])
    return f'consumo "{self.datahora}", {self.cliente} (cliente), {itens} (itens)'

class Cantina:
  def __init__(self):
    self.estoque = Estoque()
    self.carrinho = Carrinho()
    self.pagamentos = Pagamentos()
    self.consumos = Consumos()
    self.cliente = None

  def adicionar_estoque(self, produto: Produto, quantidade = 1):
    ret = self.estoque.adicionar(ItemEstoque(produto, quantidade))
    print_title(f'adicionado {quantidade} {plural(quantidade, 'itens', 'item')} {produto} ao estoque')
    return ret

  def remover_estoque(self, produto: Produto, quantidade = 1) -> bool:
    return self.estoque.remover_produto(produto, quantidade)

  def listar_estoque(self) -> list[ItemEstoque]:
    return self.estoque.listar()
  
  def escolher_cliente(self) -> Cliente:
    nome = input_parsed('nome do cliente')
    opcao_tipo, tipo = escolher('tipo de cliente', ['aluno', 'professor', 'funcionario'], False)
    curso, periodo = None, None
    if opcao_tipo == 1 or opcao_tipo == 2:
      _, curso = escolher('curso da fatec', ['ia', 'esg'], False)
    if opcao_tipo == 1:
      _, periodo = escolher('periodo do curso', [1, 2, 3], False)
    return Cliente(nome, tipo, curso, periodo)

  def adicionar_cliente(self, cliente: Cliente) -> None:
    self.cliente = cliente

  def escolher_estoque(self) -> ItemEstoque:
    return escolher('estoque', self.listar_estoque())

  def quantidade_produtos(self) -> int:
    return sum([1 for _ in self.estoque.listar()])

  def adicionar_carrinho(self, produto: Produto, quantidade = 1) -> None:
    self.carrinho.adicionar(ItemCarrinho(produto, quantidade))
    print_title(f'adicionado {quantidade} {plural(quantidade, 'itens', 'item')} {produto} ao carrinho')

  def somar_total(self) -> int:
    return sum([p.quantidade * p.produto.preco_venda for p in self.listar_carrinho()])
  
  def adicionar_pagamento(self, item: ItemPagamento) -> None:
    self.pagamentos.adicionar(item)

  def adicionar_consumo(self, item: ItemConsumo) -> None:
    self.consumos.adicionar(item)

  def listar_carrinho(self) -> list[ItemCarrinho]:
    return self.carrinho.listar()
  
  def escolher_carrinho(self) -> ItemCarrinho:
    return escolher('carrinho', self.listar_carrinho())

  def remover_carrinho(self, produto: Produto, quantidade = 1) -> None:
    self.carrinho.remover_produto(produto, quantidade)

  def escolher_pagamento(self) -> str:
    return escolher('pagamento', ['pix'])
  
  def limpar_carrinho(self) -> None:
    self.carrinho.limpar()

  def listar_pagamentos(self) -> list[ItemPagamento]:
    return self.pagamentos.listar()

  def listar_consumos(self) -> list[ItemConsumo]:
    return self.consumos.listar()

# # auxiliar

def escolher(title, items, out = True) -> int | Item:
  while True:
    print_title(title)
    if out:
      print('0. sair')
    [print(f'{ix+1}. {p}') for ix, p in enumerate(items)]
    try:
      item = int(input('> ')) # valida escolha como numero
      if out:
        if item == 0:
          return item, 'sair'
      return item, items[item-1] # retorna como texto
    except:
      pass

def menu():
  cantina = Cantina()

  while True:
    opcoes = ['adicionar produto ao estoque (Faker)','remover produto do estoque','ver estoque','adicionar produto ao carrinho','remover produto do carrinho','ver carrinho','finalizar carrinho','extrair relatorio de vendas','extrair relatorio de consumos', 'carregar lista de produtos (Pickle)', 'salvar lista de produtos (Pickle)']

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
        opcao_estoque, produto = cantina.escolher_estoque()
        if opcao_estoque != 0:
          quantidade = input_parsed('quantidade', int)
          cantina.remover_estoque(produto.produto, quantidade)
        continue
      case '3':
        [print(p) for p in cantina.listar_estoque()]
        continue
      case '4':
        opcao_estoque, produto = cantina.escolher_estoque()
        if opcao_estoque != 0:
          quantidade = input_parsed('quantidade', int)
          if cantina.remover_estoque(produto.produto, quantidade):
            cantina.adicionar_carrinho(produto.produto, quantidade)
        continue
      case '5':
        opcao_carrinho, produto = cantina.escolher_carrinho()
        if opcao_carrinho != 0:
          quantidade = input_parsed('quantidade', int)
          if cantina.remover_carrinho(produto.produto, quantidade):
            cantina.adicionar_estoque(produto.produto, quantidade)
        continue
      case '6':
        [print(p) for p in cantina.carrinho.listar()]
        continue
      case '7':
        opcao_pagamento, pagamento = cantina.escolher_pagamento()
        if opcao_pagamento != 0:
          cliente = cantina.escolher_cliente()          
          produtos = cantina.listar_carrinho()
          cantina.adicionar_pagamento(ItemPagamento(pagamento, produtos, cantina.somar_total()))
          cantina.adicionar_consumo(ItemConsumo(cliente, produtos))
          cantina.limpar_carrinho()
        continue
      case '8':
        [print(p) for p in cantina.listar_pagamentos()]
        continue
      case '9':
        [print(p) for p in cantina.listar_consumos()]
        continue
      case '10':
        with open("estoque.pkl", "rb") as f:
          try:
            estoque = pickle.load(f)
          except:
            estoque = []
          [cantina.adicionar_estoque(e) for e in estoque]
      case '11':
        estoque = cantina.listar_estoque()
        with open("estoque.pkl", "wb") as f:
            pickle.dump(estoque, f)
      case '0':
        exit(0)
      case _:
        opcao_invalida()
  
menu()
