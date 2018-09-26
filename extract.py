#read excel file: https://www.geeksforgeeks.org/reading-excel-file-using-python/
#write csv headers: https://stackoverflow.com/a/47710814
the_important_columns = ["Time", "Occupant Number", "INDOOR Ambient Temp.", "INDOOR Relative Humidity", "INDOOR Air Velocity", "INDOOR Mean Radiant Temp.", "Predicted Mean Vote (PMV)"]

'''
import xlrd as x
wb = x.open_workbook(("cols.xlsx"))
sheet = wb.sheet_by_index(0)
the_important_columns_set = set(the_important_columns)
#extract a list of tuples (zero'ed_index, column_name) from excel file
indexed_cols = [
  (int(row[0].value)-1, row[2].value)
  for row in sheet.get_rows()
  if row[2].value in the_important_columns_set
]
'''
indexed_cols = [
  (1-1, "Time"),
  (2-1, "Occupant Number"),
  (6-1, "INDOOR Ambient Temp."),
  (7-1, "INDOOR Relative Humidity"),
  (8-1, "INDOOR Air Velocity"),
  (9-1, "INDOOR Mean Radiant Temp."),
  (118-1, "Predicted Mean Vote (PMV)"),
]

print(indexed_cols)

def maybeFloat(string):
  '''Converts NaN values to None.
  While NaN is a valid floating point value,
  it is truthy and cannot be tested for equality'''
  return None if string == "NaN" else float(string)

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
    writer.writerow(the_important_columns)
    for row in labeled_rows:
      writer.writerow([row[col] for col in the_important_columns])

if __name__ == '__main__':
  from sys import argv, exit
  if len(argv) > 2:
    input_filepath, output_filepath = argv[1], argv[2]
  else:
    print('Usage: python extract.py <input filepath> <output filepath>')
    if input('Use defaults?'):
      input_filepath, output_filepath = "smaller data.txt", "processed_data.csv"
    else:
      exit()
  print('labeling rows...')
  labeled_rows = readfile(input_filepath)
  print('writing csv...')
  writefile(labeled_rows, output_filepath)
