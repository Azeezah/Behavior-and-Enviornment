import matplotlib.pyplot as plt
from math import sqrt
from random import choice
from utils import print_out

def create_histogram(x, name):
  plt.hist(x, bins=50)
  plt.xlabel(name)
  plt.ylabel('Frequency')
  plt.savefig(name+'.png')
  plt.clf()

def create_scatterplot(x, name_x, y, name_y):
  length = min(len(x), len(y))
  x, y = x[:length], y[:length]
  plt.scatter(x, y)
  plt.xlabel(name_x)
  plt.ylabel(name_y)
  plt.savefig(name_x + ' to ' + name_y+'.png')
  plt.clf() 

def show_stats(x, name):
  print('\n'+name+':')
  print('length %d, mean %.2f, stddev %.2f, range %.2f, median %.2f' \
    % (len(x), mean(x), stddev(x), max(x)-min(x), median(x)))

  modes_x = modes(x)
  num_modes = len(modes_x)
  print_out('modes: ', modes_x[:3], ('and %d more' % (num_modes-3) if num_modes > 3 else ''))

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

