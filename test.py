import pandas as pd
data = pd.read_csv('Data\DC Battery Report.csv')

table = data.to_html()
print(table)
