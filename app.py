class Produto:
  def __init__(self, nome, preco_compra, preco_venda, data_compra, data_vencimento):
    self.nome = nome
    self.preco_compra = preco_compra
    self.preco_venda = preco_venda
    self.data_compra = data_compra
    self.data_vencimento = data_vencimento

  def __repr__(self):
    return f'nome: {self.nome}, preco_compra: {self.preco_compra}, preco_venda: {self.preco_venda}, data_compra: {self.data_compra}, data_vencimento: {self.data_vencimento}'

class Pagamento:
  def __init__(self, nome, categoria, curso, valor, data_hora):
    self.nome = nome
    self.categoria = categoria
    self.curso = curso
    self.valor = valor
    self.data_hora = data_hora

class Consumo:
  def __init__(self, consumidor, produto, pagamento):
    self.consumidor = consumidor
    self.produto = produto
    self.pagamento = pagamento

class Lista(list):
  def adicionar(self, item):
    self.append(item)

  def remover(self, item):
    pass

  def listar(self):
    return [s for s in self]

class Estoque(Lista):
  def remover_produto(self, produto: Produto, quantidade = 1):
    for p in self:
      if p.produto.nome == produto.nome:
        if p.quantidade - quantidade < 0:
          return False, 'Quantidade indisponivel'
        p.quantidade -= quantidade
      return True, None
    return False, 'Produto não encontrado'
  
class Carrinho(Lista):
  pass

class Pagamentos(Lista):
  pass

class Consumos(Lista):
  pass

class Cliente():
  def __init__(self, nome):
    self.nome = nome

class ItemEstoque(list):
  def __init__(self, produto: Produto, quantidade = 1):
    super().__init__()
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
    print(f'Produto "{produto.nome}" adiconado ao estoque')

  def remover_estoque(self, item: ItemEstoque, quantidade = 1):
    ok, message = self.estoque.remover_produto(item.produto, quantidade)
    if ok: print(f'{quantidade} produto{plural(quantidade)} "{item.produto.nome}" removido{plural(quantidade)} do estoque')
    else: print(message)

  def listar_estoque(self):
    return self.estoque.listar()
  
  def ver_cliente():
    pass

  def escolher_cliente(self):
    while True:
      print('--- Cliente ---')
      nome = input_data('nome')
      if nome:
        return Cliente(nome)

  def adicionar_cliente(self, cliente):
    self.cliente = cliente

  def escolher_estoque(self):
    while True:
      print('--- Estoque ---')
      produtos = self.listar_estoque()
      [print(f'{ix+1}. {p}') for ix, p in enumerate(produtos)]
      item = int(input('> '))
      try:
        return produtos[item-1]
      except:
        print('Produto não encontrado.')

  def quantidade_produtos(self):
    return sum([1 for _ in self.estoque.listar()])

  def adicionar_carrinho(self, produto, quantidade):
    pass

# # auxiliar

def plural(num, muitostr = 's', poucostr = ''):
  return muitostr if num > 1 else poucostr

def input_data(txt, parser = str):
  return parser(input(f'{txt}: '))

def menu():
  cantina = Cantina()

  while True:
    print('-- Menu --')
    print('1. Adicionar produto ao estoque')
    print('2. Remover produto do estoque')
    print('3. Ver estoque')
    print('4. Adicionar produto ao carrinho')
    print('5. Remover produto do carrinho')
    print('6. Ver carrinho')
    print('7. Finalizar carrinho')
    print('8. Extrair relatorio de vendas')
    print('9. Extrair relatorio de consumos')
    print('0. Sair')
  
    opcao = input('> ')

    match opcao:
      case '1':
        print('--- Adicionar produto ao estoque ---')
        nome = input_data('nome')
        preco_compra = input_data('preco de compra', float)
        preco_venda = input_data('preco de venda', float)
        data_compra = input_data('data de compra')
        data_vencimento = input_data('data de vencimento')
        quantidade = input_data('quantidade', int)
        
        produto = Produto(nome, preco_compra, preco_venda, data_compra, data_vencimento)

        cantina.adicionar_estoque(produto, quantidade)
        continue
      case '2':
        print('--- Remover produto do estoque ---')
        produto: ItemEstoque = cantina.escolher_estoque()
        quantidade = input_data('quantidade', int)
        cantina.remover_estoque(produto, quantidade)
        continue
      case '3':
        print('--- Ver estoque ---')
        [print(f'{ix+1}. {p}') for ix, p in enumerate(cantina.listar_estoque())]
        continue
      case '4':
        print('--- Adicionar produto ao carrinho ---')
        produto = cantina.escolher_estoque()
        quantidade = input_data('quantidade', int)
        if not cantina.ver_cliente():
          cliente = cantina.escolher_cliente()
          cantina.adicionar_cliente(cliente)
        # cantina.adicionar_carrinho(ProdutoCarrinho(*produto, quantidade=quantidade))
        continue
      case '5':
        print('-- item 5 --')
        continue
      case '6':
        print('-- item 6 --')
        continue
      case '7':
        print('-- item 7 --')
        continue
      case '8':
        print('-- item 8 --')
        continue
      case '9':
        print('-- item 9 --')
        continue
      case '0':
        print('-- sair --')
        exit(0)
      case _:
        print('-- opcao invalida --')
        continue
  
menu()
