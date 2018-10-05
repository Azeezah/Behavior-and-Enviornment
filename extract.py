import random
from utils import maybeFloat, get_input

column_names = ["Time", "Occupant Number", "INDOOR Ambient Temp.", "INDOOR Relative Humidity", "INDOOR Air Velocity", "INDOOR Mean Radiant Temp.", "Predicted Mean Vote (PMV)", "Occupancy 1"]

def sample_data(in_filename, out_filename, percent=100):
  in_file = open(in_filename, 'rb')
  out_file = open(out_filename, 'wb')
  line = in_file.readline()
  while line:
    if random.random() < percent/100.0:
      out_file.write(line)
    line = in_file.readline()
  in_file.close()
  out_file.close() 

def get_column_names():
  import xlrd as x
  wb = x.open_workbook(("cols.xlsx"))
  sheet = wb.sheet_by_index(0)
  column_names_set = set(column_names)
  #extract a list of tuples (zero'ed_index, column_name) from excel file
  indexed_cols = [
    (int(row[0].value)-1, row[2].value)
    for row in sheet.get_rows()
    if row[2].value in column_names_set
  ]
  return indexed_cols

indexed_cols = [
  (1-1, "Time"),
  (2-1, "Occupant Number"),
  (6-1, "INDOOR Ambient Temp."),
  (7-1, "INDOOR Relative Humidity"),
  (8-1, "INDOOR Air Velocity"),
  (9-1, "INDOOR Mean Radiant Temp."),
  (118-1, "Predicted Mean Vote (PMV)"),
  (3-1, "Occupancy 1"),
]

def readfile(office_env_data_file):
  with open(office_env_data_file, 'rb') as f:
    rows = [[maybeFloat(val) for val in row.split()] for row in f.readlines()]
    labeled_rows = [{col_name : row[i] for i, col_name in indexed_cols}
      for row in rows]
  return labeled_rows

def writefile(labeled_rows, output_path='data.csv'):
  import csv
  with open(output_path, 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(column_names)
    for row in labeled_rows:
      writer.writerow([row[col] for col in column_names])

if __name__ == '__main__':
  from sys import argv, exit
  if len(argv) > 2:
    input_filepath, output_filepath = argv[1], argv[2]
  else:
    print('Usage: python extract.py <input filepath> <output filepath>')
    if get_input('Use defaults? (y/n)') == 'y':
      input_filepath, output_filepath = "data.txt", "processed_data.csv"
    else:
      print('Ok bye')
      exit()
  print('Labeling rows...')
  labeled_rows = readfile(input_filepath)
  print('Writing csv...')
  writefile(labeled_rows, output_filepath)
