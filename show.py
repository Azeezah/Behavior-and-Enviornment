import matplotlib.pyplot as plt
from math import sqrt
from random import choice

the_important_columns = ["Time", "Occupant Number", "INDOOR Ambient Temp.", "INDOOR Relative Humidity", "INDOOR Air Velocity", "INDOOR Mean Radiant Temp.", "Predicted Mean Vote (PMV)"]

# a delta just large enough to equate 1 and n/n
effective_infinitesimal = 1e-15

def show_all(data, cols=the_important_columns):
  for i, col in enumerate(cols):
    show(data, i, filename=col+'.png')

def show(data, col_num=0, filename="graph.png"):
  '''takes a list of dictionaries'''
  x = get_col(the_important_columns[col_num], data)
  print('graphing col %d, %s'%(col_num, the_important_columns[col_num]))
  x = numeric(x)
  print(stats(x))
  plt.hist(x, bins=50)
  plt.xlabel(the_important_columns[col_num])
  plt.ylabel('Frequency')
  #plt.axis([0, 60, 0, 1])
  plt.savefig(filename)

def show_correlations(data):
  cols = [get_col(label, data) for label in the_important_columns]
  for i, x in enumerate(the_important_columns):
    for j, y in enumerate(the_important_columns):
      print x, 'to', y, correlation(numeric(cols[i]), numeric(cols[j]))

def get_correlations(data):
  cols = [get_col(label, data) for label in the_important_columns]
  for i, x in enumerate(the_important_columns):
    for j, y in enumerate(the_important_columns):
      yield i, j, correlation(numeric(cols[i]), numeric(cols[j]))

def get_important_correlations(data):
  return filter(lambda (x, y, c): (c > 0.5 and c < 1-effective_infinitesimal),
    get_correlations(data))

def get_col(col_name, data):
  return [row[col_name] for row in data]

def zero(xs):
  '''takes a list and sets falsy values to 0'''
  return [x or 0 for x in xs]

def numeric(xs):
  '''takes a list and removes None values'''
  return [x for x in xs if x!=None]

def stats(x):
  return ('len', len(x), 'avg', sum(x)/len(x))

def stddev(xs):
  mu = sum(xs)/len(xs)
  return sqrt(sum((x-mu)**2 for x in xs) / (len(xs)-1))

def covariance(xs, ys):
  x_mu = sum(xs)/len(xs)
  y_mu = sum(ys)/len(ys)
  n = min(len(xs), len(ys))-1
  return sum((x_mu-x) * (y_mu-y) for x, y in zip(xs, ys)) / n

def correlation(xs, ys):
  try:
    return covariance(xs, ys)/(stddev(xs)*stddev(ys))
  except ZeroDivisionError:
    return 1


