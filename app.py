class Produto:
  def __init__(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
    self.nome = nome
    self.preco_compra = preco_compra
    self.preco_venda = preco_venda
    self.data_compra = data_compra
    self.data_vencimento = data_vencimento
    self.quantidade = quantidade

  def __repr__(self):
    return f'nome: {self.nome}, preco_compra: {self.preco_compra}, preco_venda: {self.preco_venda}, data_compra: {self.data_compra}, data_vencimento: {self.data_vencimento}, quantidade: {self.quantidade}'

  def atualizar_a_quantidade(self, nova_qtd):
    self.quantidade = nova_qtd

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

  def listar(self):
    return [s for s in self]

class Estoque(Lista):
  pass

class Pagamentos(Lista):
  pass

class Consumos(Lista):
  pass

class Cantina:
  def __init__(self):
    self.estoque = Estoque()
    self.pagamentos = Pagamentos()
    self.consumos = Consumos()

  def adicionar_estoque(self, produto: Produto):
    self.estoque.adicionar(produto)
    print(f'Produto "{produto.nome}" adiconado ao estoque')

# # auxiliar

def input_data(txt, parser = str):
  return parser(input(f'{txt}: '))

def menu():
  cantina = Cantina()

  while True:
    print('-- menu --')
    print('1. Adicionar produto ao estoque')
    print('2. Vender produto')
    print('3. Extrair relatorio de vendas')
    print('4. Extrair relatorio de consumos')
    print('0. sair')
  
    opcao = input('> ')
  
    match opcao:
      case '1':
        nome = input_data('nome')
        preco_compra = input_data('preco_compra', float)
        preco_venda = input_data('preco_venda', float)
        data_compra = input_data('data_compra')
        data_vencimento = input_data('data_vencimento')
        quantidade = input_data('quantidade', int)
        
        produto = Produto(nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade)
    
        cantina.adicionar_estoque(produto)
        continue
      case '2':
        print('-- item 2 --')
        continue
      case '3':
        print('-- item 3 --')
        continue
      case '4':
        print('-- item 4 --')
        continue
      case '0':
        print('-- sair --')
        exit(0)
      case _:
        print('-- opcao invalida --')
        continue
  
menu()
