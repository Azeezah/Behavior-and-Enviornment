import extract
import stats
import utils
from os import chdir, mkdir
from utils import print_out, get_arg, get_input

def describe_all_columns_separately(data):
  for name in extract.column_names:
    col = stats.get_col(name, data)
    stats.show_stats(col, name)
    stats.create_histogram(col, name)

def relate_ambient_temp_to_mean_radiant_temp(data):
  ambient = stats.get_col('INDOOR Ambient Temp.', data)
  mean_radiant = stats.get_col('INDOOR Mean Radiant Temp.', data)
  stats.create_scatterplot(ambient, 'INDOOR Ambient Temp.', mean_radiant, 'INDOOR Mean Radiant Temp.')
  print("Correlation coefficient: ", stats.correlation(ambient, mean_radiant))
 
def relate_ambient_temp_to_relative_humidity(data):
  temp = stats.get_col('INDOOR Ambient Temp.', data)
  humidity = stats.get_col('INDOOR Relative Humidity', data)
  stats.create_scatterplot(temp, 'INDOOR Ambient Temp.', humidity, 'INDOOR Relative Humidity')
  print('INDOOR Ambient Temp. to INDOOR Relative Humidity')
  print_out("Correlation coefficient: ", stats.correlation(temp, humidity))

  temp_farenheit = map(utils.celsius_to_farenheit, temp)
  stats.create_scatterplot(temp_farenheit, 'INDOOR Ambient Temp. (degrees Farenheit)', humidity, 'INDOOR Relative Humidity')
  print('INDOOR Ambient Temp. (degrees Farenheit) to INDOOR Relative Humidity')
  print_out("Correlation coefficient: ", stats.correlation(temp_farenheit, humidity))
  
  temp_norm = stats.normalize(temp)
  humidity_norm = stats.normalize(humidity)
  stats.create_scatterplot(temp_norm, 'INDOOR Ambient Temp. (normalized)', humidity_norm, 'INDOOR Relative Humidity (normalized)')
  print('INDOOR Ambient Temp. (normalized) to INDOOR Relative Humidity (normalized)')
  print_out("Correlation coefficient: ", stats.correlation(temp_norm, humidity_norm))

def describe_occupied_rooms(data):
  data = [row for row in data if row["Occupancy 1"] == 1]
  extract.writefile(data, 'occupancy_1.csv')
  describe_all_columns_separately(data)
  relate_ambient_temp_to_relative_humidity(data)

def describe_half_seconds(data): 
  data = [row for row in data if row["Time"]%1 == 0.5]
  extract.writefile(data, 'tod_1200.csv')
  describe_all_columns_separately(data)
  relate_ambient_temp_to_relative_humidity(data)

def interactive_data_analysis(data):
  import re
  for i, name in enumerate(extract.column_names): print_out(i, name)
  dimension = get_input('Would you like to view 1d or 2d data? (enter 1 or 2)? ')
  columns = get_input("Which columns would you like to see? (enter numbers with spaces) ")
  if bool(re.match(dimension[:-1], r'1|2')) and bool(re.match(columns[:-1], r'[0-9](\s[0-9])*')):
    columns = map(int, columns.strip().split())
    dimension = int(dimension.strip())
  else:
    print("Received invalid input")
    quit()
  if dimension == 1:
    for col_num in columns:
      name = extract.column_names[col_num]
      col = stats.get_col(name, data)
      stats.show_stats(col, name)
      stats.create_histogram(col, name)
  elif dimension == 2:
    columns = [extract.column_names[i] for i in columns]
    for i, col_x in enumerate(columns):
      for col_y in columns[i+1::]:  #avoid duplicate pairs
        stats.show_correlation(col_x, col_y)
        stats.create_scatterplot(col_x, col_y)

def default_data_analysis(data):
  print("Describing all columns separately")
  #with SubDirectory('describe_all_columns_separately'):
  describe_all_columns_separately(data)
  get_input('finished part 1 (move the graph files and hit enter for the next part)')
  
  print("Relating ambient temp to mean radiant temp")
  #with SubDirectory('relate_ambient_temp_to_mean_radiant_temp'):
  relate_ambient_temp_to_mean_radiant_temp(data)
  get_input('finished part 2 (move the graph files and hit enter for the next part)')

  print("relate_ambient_temp_to_relative_humidity")
  relate_ambient_temp_to_relative_humidity(data)
  get_input('finished part 3 (move the graph files and hit enter for the next part)')
  
  print("Describing occupied rooms")
  #with SubDirectory('describe_occupied_rooms'):
  describe_occupied_rooms(data)
  get_input('finished part 4 (move the graph files and hit enter for the next part)')
  
  print("Describing half seconds")
  #with SubDirectory('describe_half_seconds'):
  describe_half_seconds(data)
  get_input('finished part 5 (move the graph files and hit enter for the next part)')
 
if __name__ == '__main__':
  from sys import argv
  data_filepath = "data.txt"

  if get_arg('help', argv):
    print_out('''
              Usage: python main.py <options>

              Options:
              --interactive(-i),
              --datafile(-d) <filepath>

              Example: python main.py -d data.txt''')
    quit()
  if get_arg('datafile', argv, has_val=True):
    data_filepath = get_arg('datafile', argv, has_val=True)
 
  print("Extracting data")
  data = extract.readfile(data_filepath)
  extract.writefile(data, 'processed_data.csv')

  if get_arg('interactive', argv):
    interactive_data_analysis(data)
  else:
    default_data_analysis(data)

