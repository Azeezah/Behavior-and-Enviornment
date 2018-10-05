import matplotlib.pyplot as plt
from math import sqrt
from random import choice

from extract import column_names

the_important_columns = ["Time", "Occupant Number", "INDOOR Ambient Temp.", "INDOOR Relative Humidity", "INDOOR Air Velocity", "INDOOR Mean Radiant Temp.", "Predicted Mean Vote (PMV)", "Occupancy 1"]

# a delta just large enough to equate 1 and n/n
effective_infinitesimal = 1e-15

def show_all(data, cols=the_important_columns):
  for i, col in enumerate(cols):
    show(data, i, filename=col+'.png')

def create_histogram(x, name):
  '''takes a list of dictionaries'''
  plt.hist(x, bins=50)
  plt.xlabel(name)
  plt.ylabel('Frequency')
  plt.savefig(name+'.png')
  plt.clf()  #wontha suggested that I use clf to clear the pyplot state machine

def create_scatterplot(x, name_x, y, name_y):
  '''takes a list of dictionaries'''
  plt.scatter(x, y)
  plt.xlabel(name_x)
  plt.ylabel(name_y)
  plt.savefig(name_x + ' to ' + name_y+'.png')
  plt.clf() 

def show_scatterplot(data, col_num_x=0, col_num_y=0, filename="graph.png"):
  '''takes a list of dictionaries'''
  x = get_col(the_important_columns[col_num_x], data)
  y = get_col(the_important_columns[col_num_y], data)
  x = numeric(x)
  y = numeric(y)
  show_stats(x, the_important_columns[col_num_x])
  show_stats(y, the_important_columns[col_num_y])
  plt.scatter(x, y)
  plt.xlabel(the_important_columns[col_num_x])
  plt.ylabel(the_important_columns[col_num_y])
  plt.savefig(filename)
  plt.clf()

def show_correlations(data):
  col_names = the_important_columns
  print("\nCorrelations:")
  for x, y, correlation in get_correlations(data):
    print col_names[x], 'to', col_names[y], correlation

def show_important_correlations(data):
  col_names = the_important_columns
  print("\nThe Larger Correlations:")
  for x, y, correlation in get_important_correlations(data):
    print col_names[x], 'to', col_names[y], correlation

def show_stats(x, name):
  print('\n'+name+':')
  print('length %d, mean %.2f, stddev %.2f, range %.2f, median %.2f' \
    % (len(x), mean(x), stddev(x), max(x)-min(x), median(x)))

  modes_x = modes(x)
  num_modes = len(modes_x)
  print('modes: ', modes_x[:3], ('and %d more' % (num_modes-3) if num_modes > 3 else ''))

def get_correlations(data):
  cols = [get_col(label, data) for label in the_important_columns]
  for i, x in enumerate(the_important_columns):
    for j, y in enumerate(the_important_columns):
      yield i, j, correlation(numeric(cols[i]), numeric(cols[j]))

def get_important_correlations(data):
  return filter(lambda (x, y, c): (c > 0.5 and c < 1-effective_infinitesimal),
    get_correlations(data))

def get_col(col_name, data):
  return remove_none([row[col_name] for row in data])

def normalize(xs):
  '''sets mean to 0 and standard deviation to 1'''
  mu = mean(xs)
  range_x = max(xs) - min(xs)
  dev = stddev(xs)
  return [(x-mu)/dev for x in xs]

def celsius_to_farenheit(x):
  return (x+32)*9/5

def falsy_to_zero(xs):
  '''takes a list and sets falsy values to 0'''
  return [x or 0 for x in xs]

def remove_none(xs):
  '''takes a list and removes None values'''
  return [x for x in xs if x!=None]

def mean(x):
  return sum(x)/len(x)

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
    return 1.0

def modes(xs):
  counts = dict()
  for x in xs:
     if x in counts: counts[x]+=1
     else: counts[x] = 1
  max_count = max(counts.values())
  return [x for x, count in counts.items() if count == max_count]

def median(xs):
  n = len(xs)
  return mean(sorted(xs)[n//2+n%2-1 : n//2+1])

