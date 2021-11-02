import xml.etree.ElementTree as et   ##Модуль парсинга xml
from os import listdir as ld         ##Модуль проверки файла а наличие


def initializate_InitData(path = 'InitData.xml', silent = False):
  '''Инициализация файла InitData.xml (файл с нитками и их связями). "path"('InitData.xml') - путь к файлу, "silent"(False) - тихий режим (в консоль не записывается лог). На выходе выдает список имен ниток (nodes) (по "N" + "имя нитки" можно обращатся как к объекту класса Node), количество ниток (node_counter) и соединений (connection_counter).'''
  root = et.parse(path).getroot()
  if silent == False:
    print('Файл ниток открыт')
  globals()['nodes'] = []
  node_counter = len(root[0][0])   ##Счетчик ниток
  globals()['node_counter'] = node_counter
  for node_values in root[0][0]:
    node_values = [value.attrib for value in node_values.iter()]
    name = 'N' + node_values[0]['name']
    nodes.append(name)
    globals()[name] = Node(node_values)
  if silent == False:
    print(node_counter, 'нитей инициализировано')
  connection_counter = len(root[0][1])   ##Счетчик соединений
  globals()['connection_counter'] = connection_counter
  for connection in root[0][1]:
    connection = [value.attrib for value in connection.iter()]
    name = 'N' + connection[0]['srcNode']
    globals()[name].addpath(connection)
  if silent == False:
    print(connection_counter, 'соединений инициализировано')
    print('Файл ниток закрыт')


def initializate_ResultsData(path = 'resultsData.xml', silent = False):
  '''Инициализация файла resultsData.xml (файл с логами маршрутов). "path"('resultsData.xml') - путь к файлу, "silent"(False) - тихий режим (в консоль не записывается лог). На выходе выдает количество маршрутов (path_counter), (по "track" + "номер(начиная с нуля)" можно обратиться как к объекту класса Pathway).'''
  root = et.parse(path).getroot()
  if silent == False:
    print('Файл результатов открыт')
  path_counter = 0   ##Счетчик маршрутов
  for pack in root[0]:
    for track in pack:
      name = 'track' + str(path_counter)
      track_values = [value.attrib for value in track.iter()]
      globals()[name] = Pathway(track_values)
      path_counter += 1
  globals()['path_counter'] = path_counter
  if silent == False:
    print(path_counter, 'путей инициализировано')
    print('Файл результатов закрыт')


class Node:
  '''Класс Node принимает формат ниток'''
  def __init__(self, data):
    self.name = data[0]['name']
    self.dist_size = int(data[0]['dist_size'])
    self.abs_type = int(data[0]['ABS_Type'])
    self.connections = {}
    self.timming = []
    self.stats = None
    types = {}
    for standart_times in data[2:]:
      types[standart_times['type']] = [int(standart_times['time']), int(standart_times['timeRev'])]
    self.types = types
  def addpath(self, data):
    self.connections[data[0]['dstNode']] = [int(data[1]['value']), int(data[2]['value'])]
  def statistic(self):
    stats = {}
    if len(self.timming) > 0:
      stats['среднее арифмитическое'] = sum(self.timming) / len(self.timming)
      stats['максимальное'] = max(self.timming)
      stats['минимальное'] = min(self.timming)
      self.stats = stats
    else:
      self.stats = 'Нет данных'
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
      name = 'N' + station['name']
      t_track = int(station['dt'])
      if addtimming_bool == True:
        globals()[name].timming.append(t_track)
      types_normal = globals()[name].types
      types_normal = types_normal.get(self.train_type, types_normal['train'])
      t_normal = types_normal[int(station['KPType'])]
      t = t_normal - t_track
      com[station['name']] = t
      time += t
    self.compare_com = com
    self.compare_time = time
  def __init__(self, data, compare_bool=True, addtimming_bool=True):
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
  initializate_InitData('C:/Users/FireStrike/PycharmProjects/pythonProject/BIGDATA/InitData.xml')
  initializate_ResultsData('C:/Users/FireStrike/PycharmProjects/pythonProject/BIGDATA/resultsData.xml')
  print('-'*100)
  for name in nodes:
    globals()[name].statistic()
    print(name[1:], globals()[name].stats)
  print('Done, "q" for exit')
  while True:
    if input() in ['q', 'quit', 'end', 'close', '']:
      print('Done')
      break
