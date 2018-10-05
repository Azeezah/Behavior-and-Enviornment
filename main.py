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
  print('INDOOR Ambient Temp. to INDOOR Relative Humidity')
  print("Correlation coefficient: ", show.correlation(temp, humidity))

  temp_farenheit = map(show.celsius_to_farenheit, temp)
  show.create_scatterplot(temp_farenheit, 'INDOOR Ambient Temp. (degrees Farenheit)', humidity, 'INDOOR Relative Humidity')
  print('INDOOR Ambient Temp. (degrees Farenheit) to INDOOR Relative Humidity')
  print("Correlation coefficient: ", show.correlation(temp_farenheit, humidity))
  
  temp_norm = show.normalize(temp)
  humidity_norm = show.normalize(humidity)
  show.create_scatterplot(temp_norm, 'INDOOR Ambient Temp. (normalized)', humidity_norm, 'INDOOR Relative Humidity (normalized)')
  print('INDOOR Ambient Temp. (normalized) to INDOOR Relative Humidity (normalized)')
  print("Correlation coefficient: ", show.correlation(temp_norm, humidity_norm))

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
  print("Extracting data")
  data = extract.readfile('data.txt')
  extract.writefile(data, 'processed_data.csv')
  get_input = raw_input if 'raw_input' in dir(vars()['__builtins__']) else input

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
 
