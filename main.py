import xml.etree.ElementTree as et   ##Модуль парсинга xml
from pathlib import Path             ##Модуль раскрытия папок
from os.path import getsize as gs    ##Модуль проверки рамера файла
from time import time                ##Модуль времени

config = {'default_silent': False, 'default_datareplace': True, 'default_save': False}
nodes = []
connections_amount = 0
paths_amount = 0
files_amount = [0, 0]

def initializate_InitData(path, silent = False, datareplace = False):
  '''Инициализация файла InitData.xml (файл с нитками и их связями). "path" - путь к файлу, "silent"(False) - тихий режим (в консоль не записывается лог), "datareplace"(True) - перезапись данных. На выходе выдает список имен ниток (nodes) (по "N" + "имя нитки" можно обращатся как к объекту класса Node), количество ниток (nodes_amount) и соединений (connection_counter).'''
  global nodes, connections_amount
  try:
    start_time = time()
    root = et.parse(path).getroot()  ##Открываем файл
    replace_counter = 0              ##Счетчик замен данных
    connections_counter = 0          ##Счетчик соединений
    nodes_counter = 0                ##Счетчик ниток
    if silent == False:
      print(f'Открыт файл: {path}\nразмер: {gs(path)} байт')
    for node_values in root[0][0]:   ##Перебираем нитки
      node_values = [value.attrib for value in node_values.iter()]   ##Считываем все значения нитки
      name = node_values[0]['name']
      if name in nodes and datareplace == True:
        replace_counter += 1
        globals()[name] = Node(node_values)                          ##Обновляем нитку
      elif name not in nodes:
        nodes.append(name)
        nodes_counter += 1
        globals()[name] = Node(node_values)                          ##Создаем нитку
    if silent == False:
      print(f'нитей инициализировано: {nodes_counter}, количество замен: {replace_counter}, время выполнения: {time() - start_time} с')
    start_time = time()
    for connection in root[0][1]:
      connection = [value.attrib for value in connection.iter()]
      name = connection[0]['srcNode']
      connections_counter += globals()[name].addpath(connection)
    connections_amount += connections_counter
    if silent == False:
      print(f'соединений инициализировано: {connections_counter}, время выполнения: {time() - start_time} с\nФайл закрыт')
  except:
    print(f'Ошибка открытия: {path}')


def initializate_ResultsData(path, silent = False):
  '''Инициализация файла resultsData.xml (файл с логами маршрутов). "path" - путь к файлу, "silent"(False) - тихий режим (в консоль не записывается лог). На выходе выдает количество маршрутов (path_counter), (по "track" + "номер(начиная с нуля)" можно обратиться как к объекту класса Pathway).'''
  global paths_amount
  try:
    start_time = time()
    path_counter = 0   ##Счетчик маршрутов
    root = et.parse(path).getroot()
    if silent == False:
      print(f'Открыт файл: {path}\nразмер: {gs(path)} байт')
    for pack in root[0]:
      for track in pack:
        name = 'track' + str(paths_amount + path_counter + 1)
        track_values = [value.attrib for value in track.iter()]
        globals()[name] = Pathway(track_values)
        path_counter += 1
    paths_amount += path_counter
    if silent == False:
      print(f'путей инициализировано: {path_counter}, время выполнения: {time() - start_time} с\nФайл закрыт')
  except:
    print(f'Ошибка открытия: {path}')


class Commands:

  def openfile(path, silent):
    path = path.replace('"', '')
    init_path = []
    results_path = []
    if '.xml' in path:
      files_path = [path]
    else:
      files = []
      for p in Path(path).rglob('*'):
        files.append(str(p.parent) + '/' + p.name)
      files_path = list(filter(lambda x: '.xml' in x, files))
    for file in files_path:
      if 'init' in file.lower():
        init_path.append(file)
      elif 'result' in file.lower():
        results_path.append(file)
    for i in init_path:
      initializate_InitData(i, silent)
      files_amount[0] += 1
    for i in results_path:
      initializate_ResultsData(i, silent)
      files_amount[1] += 1

  def checknodes(com, silent):
    for name in com:
      try:
        ans = globals()[name].check()
        if silent == False:
          print(name, ans)
      except:
        if silent == False:
          print(name, 'не определена')

  def statnodes(data, silent):
    for name in data:
      try:
        ans = globals()[name].statistic()
        if silent == False:
          print(name, ans)
      except:
        if silent == False:
          print(name, 'не определена')

  def info(data):
    for i in data:
      print(globals()[i])


  def execute(data):
    global nodes, connections_amount, paths_amount, files_amount, config
    if '/silent' == data[:7]:
      data = data[8:]
      silent = True
    else:
      silent = config['default_silent']
    if '/save' == data[:5]:
      data = data[6:]
      save = True
    else:
      save = config['default_save']
    if '/datareplace' == data[:12]:
      datareplace = True
      data = data[13:]
    else:
      datareplce = config['default_datareplace']
    if '/help' == data[:5]:
      print(f'Словарь команд:\n/help - помощь\n/statistic - общая статистика по программе\n/info [имя нитки/маршрута(например: "track23")/пусто(все)] - информация\n/statnodes [имя нитки/пусто(все)] - статистика нитки(ок)\n/checknodes [имя нитки/пусто(все)] - проверяет нитку на ошибки\n[путь к файлу/папке] - инициализация файлов\n/q - закрыть программу\nМожно указывать несколько значений(имен) через пробел\nДобавочные команды:\n/silent (по умолчанию: {config["default_silent"]})- выполнение команд без записи логов в консоль\n/datareplace (по умолчанию {config["default_datareplace"]})  - замена значений ниток при инициализации файлов')
      print('-' * 50)
    elif '/statistic' == data[:10]:
      print(f'Нитки:\n{nodes}\nкол-во соединений: {connections_amount}\nкол-во маршрутов: {paths_amount}\nкол-во инициализированных файлов: {sum(files_amount)}')
      print('-' * 50)
    elif '/checknodes' == data[:11]:
      data = data[12:]
      if data == '':
        data = nodes
      else:
        data = data.split()
      Commands.checknodes(data, silent)
      print('-' * 50)
    elif '/statnodes' == data[:10]:
      data = data[11:]
      if data == '':
        data = nodes
      else:
        data = data.split()
      Commands.statnodes(data, silent)
      print('-' * 50)
    elif '/info' == data[:5]:
      data = data[6:]
      if data == '':
        data = nodes  + ['track' + str(i) for i in range(1, paths_amount+1)]
      else:
        data = data.split()
      Commands.info(data)
      print('-' * 50)
    elif data == '':
      print('/help - помощь')
      print('-'*50)
    else:
      Commands.openfile(data, silent)
      print('-' * 50)



class Node:
  '''Класс Node принимает формат ниток'''
  def __init__(self, data):
    self.name = data[0]['name']
    self.dist_size = int(data[0]['dist_size'])
    self.abs_type = int(data[0]['ABS_Type'])
    self.connections = {}
    self.timing = []
    self.stats = None
    types = {}
    for standart_times in data[2:]:
      types[standart_times['type']] = [int(standart_times['time']), int(standart_times['timeRev'])]
    self.types = types

  def addpath(self, data):
    if data[0]['dstNode'] not in self.connections:
      self.connections[data[0]['dstNode']] = [int(data[1]['value']), int(data[2]['value'])]
      return 1
    else:
      return 0

  def statistic(self):
    if len(self.timing) > 0:
      stats = {}
      lenght = len(self.timing)
      total = sum(self.timing)
      mean = total / lenght
      stats['среднее арифмитическое'] = mean
      stats['максимальное'] = max(self.timing)
      stats['минимальное'] = min(self.timing)
      stats['среднеквадратическое отклонение'] = (sum([(elem-mean)**2 for elem in self.timing]) / lenght) ** 0.5
      self.stats = stats
    else:
      self.stats = 'Нет данных'
    return self.stats

  def check(self):
    if len(self.connections) > 0 and self.name not in self.connections:
      return 'OK'
    else:
      return 'Error'

  def __str__(self):
    t = str(self.types)[1:-1].replace('], ', ']\n')
    c = str(self.connections)[1:-1].replace('], ', ']\n')
    self.statistic()
    return f'имя: {self.name}, дистанция: {self.dist_size}м, тип ABS: {self.abs_type}\nвремена поездов \
(в формате "тип": "[время туда, время обратно]"):\n{t}\nсвязи с другими нитками \
(в формате "конечная нитка": "[начальный путь, конечный путь]"):\n{c}\nстатистика {self.stats}'


class Pathway:
  def compare(self, addtimming_bool):
    time = 0
    com = {}
    for station in self.track:
      name = station['name']
      t_track = int(station['dt'])
      if addtimming_bool == True:
        globals()[name].timing.append(t_track)
      types_normal = globals()[name].types
      types_normal = types_normal.get(self.train_type, types_normal['train'])
      t_normal = types_normal[int(station['KPType'])]
      t = t_normal - t_track
      com[station['name']] = t
      time += t
    self.compare_com = com
    self.compare_time = time
  def __init__(self, data, compare_bool = True, addtimming_bool = True):
    self.id_last_position = int(data[0]['idLastPosition'])
    self.train_type = data[1]['type']
    self.priority = int(data[1]['priority'])
    self.train_number = int(data[1]['trainNumber'])
    self.track = data[3:]
    if compare_bool == True:
      self.compare(addtimming_bool)
  def __str__(self):
    t = str(self.track)[1:-1].replace('}, ', '}\n')
    return f'номер поезда: {self.train_number}, тип: {self.train_type}, приоритет: {self.priority}\nпуть:\n{t}'


if __name__ == '__main__':
  while True:
    com = input()
    if com in ['/q', '/kill', '/exit', '/break', '/quit']:
      break
    Commands.execute(com)
