import extract
import show
data = extract.readfile('data.txt')
extract.writefile(data, 'processed_data.csv')

#show.show_all(data)
show.show_scatterplot(data, 2, 6, 'ambient temp v. mean radiant temp.png')
#show.show_important_correlations(data)


