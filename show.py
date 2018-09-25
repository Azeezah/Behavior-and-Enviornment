import matplotlib.pyplot as plt
the_important_columns = ["Time", "Occupant Number", "INDOOR Ambient Temp.", "INDOOR Relative Humidity", "INDOOR Air Velocity", "INDOOR Mean Radiant Temp.", "Predicted Mean Vote (PMV)"]

def show_all(data, cols=the_important_columns):
  for i, col in enumerate(cols):
    show(data, i, filename=col+'.png')

def show(data, col_num=0, filename="graph.png"):
  '''takes a list of dictionaries'''
  x = get_col(the_important_columns[col_num], data)
  print('graphing col %d, %s'%(col_num, the_important_columns[col_num]))
  x = numeric(x)
  print(stats(x))
  plt.hist(x, 50, density=1, facecolor='green')
  plt.xlabel(the_important_columns[col_num])
  plt.ylabel('Probability %')
  #plt.axis([0, 60, 0, 1])
  plt.savefig(filename)

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
