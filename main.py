import extract
import show
from os import chdir, mkdir

def describe_all_columns_separately(data):
  for name in extract.column_names:
    col = show.get_col(name, data)
    show.show_stats(col, name)
    show.create_histogram(col, name)

def relate_ambient_temp_to_mean_radiant_temp(data):
  ambient = show.get_col('INDOOR Ambient Temp.', data)
  mean_radiant = show.get_col('INDOOR Mean Radiant Temp.', data)
  show.create_scatterplot(ambient, 'INDOOR Ambient Temp.', mean_radiant, 'INDOOR Mean Radiant Temp.')
  print("Correlation coefficient: ", show.correlation(ambient, mean_radiant))
 
def relate_ambient_temp_to_relative_humidity(data):
  temp = show.get_col('INDOOR Ambient Temp.', data)
  humidity = show.get_col('INDOOR Relative Humidity', data)
  show.create_scatterplot(temp, 'INDOOR Ambient Temp.', humidity, 'INDOOR Relative Humidity')
  print("Correlation coefficient: ", show.correlation(temp, humidity))

  temp_farenheit = map(show.celsius_to_farenheit, temp)
  show.create_scatterplot(temp_farenheit, 'INDOOR Ambient Temp. (degrees Farenheit)', humidity, 'INDOOR Relative Humidity')
  temp_norm = show.normalize(temp)
  print("Correlation coefficient: ", show.correlation(temp_farenheit, humidity))
  
  humidity_norm = show.normalize(humidity)
  show.create_scatterplot(temp_norm, 'INDOOR Ambient Temp. (normalized)', humidity_norm, 'INDOOR Relative Humidity (normalized)')
  print("Correlation coefficient: ", show.correlation(temp_norm, humidity_norm))

def decribe_occupied_rooms(data):
  data = [row for row in data if row["Occupancy 1"] == 1]
  extract.writefile(data, 'occupancy_1.csv')
  describe_all_columns_separately(data)
  relate_ambient_temp_to_relative_humidity(data)

def describe_half_seconds(data): 
  data = [row for row in data if row["Time"]%1 == 0.5]
  extract.writefile(data, 'tod_1200.csv')
  describe_all_columns_separately(data)
  relate_ambient_temp_to_relative_humidity(data)

def interactive_data_analysis():
  import re
  get_input = raw_input if 'raw_input' in dir(vars()['__builtins__']) else input
  dimension = get_input('Would you like to view 1d or 2d data? (enter 1 or 2)?')
  columns = get_input("Which columns would you like to see? (enter numbers with spaces)")
  if bool(re.match(dimension, '\d')) and bool(re.match(columns, '(\d[\W])*\d')):
    columns = map(int, split(columns))
    dimension = int(dimension)
  else:
    print("Received invalid input")
    quit()
  if dimension == 1:
    for col in columns:
      show_stats(col)
      generate_histogram(col)
  elif dimension == 2:
    columns = [extract.column_names[i] for i in columns]
    for i, col_x in enumerate(columns):
      for col_y in columns[i+1::]:  #avoid duplicate pairs
        show.show_correlation(col_x, col_y)
        show.create_scatterplot(col_x, col_y)

class SubDirectory():
  def __init__(self, dir_name):
    self.dir_name = dir_name
  def __enter__(self):
    try:
      mkdir(self.dir_name)
    except:  # os specific error if directory exists already
      chdir(self.dir_name)
  def __exit__(self, *_):
    chdir('..') 

if __name__ == '__main__':
  import time
  from datetime import datetime
  finish_time = lambda delta: datetime.fromtimestamp(time.time() + delta)

  data = extract.readfile('data.txt')
  extract.writefile(data, 'processed_data.csv')
  num_cols = len(data)

  print("describing all columns separately")
  print("approx. finish time: ", finish_time(5 * num_cols))
  with SubDirectory('describe_all_columns_separately'):
    describe_all_columns_separately(data)
  
  print("relating ambient temp to mean radiant temp")
  print("approx. finish time: ", finish_time(5 * num_cols))
  with SubDirectory('relate_ambient_temp_to_mean_radiant_temp'):
    relate_ambient_temp_to_mean_radiant_temp(data)
  
  print("describing occupied rooms")
  print("approx. finish time: ", finish_time(5 * num_cols))
  with SubDirectory('describe_occupied_rooms'):
    decribe_occupied_rooms(data)
  
  print("describing half seconds")
  print("approx. finish time: ", finish_time(5 * num_cols))
  with SubDirectory('describe_half_seconds'):
    describe_half_seconds(data)
 
