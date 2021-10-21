##Парсинг данных из InitData.xml##
##Потестить можно в colab'е https://colab.research.google.com/drive/1DjlWeSJdl-a3c6HKhUe1oYCKQPiQPjIa?usp=sharing ##
import xml.etree.ElementTree as et
nodes = []   ##Здесь будут храниться имена ниток (начинаются с буквы 'N' (тк в путоне имена переменных не могут начинаться с цифр))##

##Функция запуска парсинга на вход принимает путь к InitData.xml##
def initialization(path):
  root = et.parse(path).getroot()
  global nodes
  for node_values in root[0][0]:    ##Парсинг самих ниток##
    node_values = [value.attrib for value in node_values.iter()]
    name = 'N' + node_values[0]['name']
    nodes.append(name)
    globals()[name] = Node(node_values)
  for connection in root[0][1]:     ##Парсинг связей с другими нитками##
    connection = [value.attrib for value in connection.iter()]
    name = 'N' + connection[0]['srcNode']
    globals()[name].addpath(connection)

    
##Создание класса Node (нитка)##
class Node:
  def __init__(self, data):
    self.name = data[0]['name']                #Имя нитки#
    self.dist_size = data[0]['dist_size']      #Длина#
    self.connections = {}                      #Связи с другими нитками#
    types = {}
    for standart_times in data[2:]:
      types[standart_times['type']] = [standart_times['time'], standart_times['timeRev']]
    self.types = types                         #Времена проезда разных типов поездов#
  def addpath(self, data):                     #Добавление связи с другой ниткой#
    self.connections[data[0]['dstNode']] = [data[1]['value'], data[2]['value']]
  def __str__(self):                           #Информация о нитке для print#
    t = str(self.types)[1:-1]
    t = t.replace('], ', ']\n')
    c = str(self.connections)[1:-1]
    c = c.replace('], ', ']\n')
    return f'имя: {self.name}, дистанция: {self.dist_size}м\nвремена поездов (в формате "тип": "[время туда, время обратно]"):\n{t}\nсвязи с другими нитками (в формате "конечная нитка": "[начальный путь, конечный путь]"):\n{c}'

  
initialization('documents/xml example/InitData.xml')
for i in nodes:
  print(globals()[i])
  print('-------------------------------')
