import extract
import show
from show import the_important_columns as col_names
data = extract.readfile('data.txt')
extract.writefile(data, 'processed_data.csv')

#print(data[6])
#show.show(data, 2)
#show.show_all(data)
#show.show_correlations(data)
for x, y, correlation in show.get_important_correlations(data):
  print col_names[x], 'to', col_names[y], correlation
row = '''735080.000000 1.000000 0.000000 0.000000 NaN 24.584695 63.517000 0.030988 24.584695 NaN 490.800000 23.000000 89.000000 1.341120 1.100000 1.100000 0.340000 0.440000 -1.000000 0.000000 1.000000 -2.000000 -1.000000 0.000000 NaN 2.000000 32.000000 3.000000 1.000000 1.000000 -1.000000 0.000000 4.500000 6.000000 0.000000 2.000000 NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN 4.000000 4.000000 2.000000 2.000000 2.000000 0.000000 NaN 18.333333 25.555556 26.666667 24.444444 NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN NaN 4.000000 4.000000 4.000000 0.000000 0.000000 2.000000 1.000000 1.000000 4.000000 2.000000 3.000000 0.000000 0.000000 2.000000 0.000000 0.000000 NaN 1.000000 1.000000 2.000000 4.000000 2.000000 2.000000 4.000000 -0.270899'''
#print([extract.maybeFloat(x) for x in row.split()])
