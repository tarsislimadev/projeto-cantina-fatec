class Produto:
  def __init__(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
    self.nome = nome
    self.preco_compra = preco_compra
    self.preco_venda = preco_venda
    self.data_compra = data_compra
    self.data_vencimento = data_vencimento
    self.quantidade = quantidade

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

def menu():
  while True:
    print('-- menu --')
    print('1. item 1')
    print('2. item 2')
    print('0. sair')

    opcao = input('> ')

    match opcao:
      case '1':
        print('-- item 1 --')
      case '2':
        print('-- item 2 --')
      case '0':
        print('-- sair --')
        break
      case _:
        print('-- opcao invalida --')

menu()
