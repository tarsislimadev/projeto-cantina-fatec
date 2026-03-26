def print_title(title):
  print(f'[ {title} ]')

def opcao_invalida():
  print_title('quantidade invalida')

def plural(num, muitostr = 's', poucostr = ''):
  return muitostr if num > 1 else poucostr

def input_parsed(txt, parser = str):
  while True:
    ret = input(f'{txt}: ')
    if ret != '':
      return parser(ret)

