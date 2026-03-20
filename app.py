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
