import string
from flask import Flask, render_template, url_for
import pandas as pd
import numpy as np
import requests

api_url = "https://lg34yl9682.execute-api.ap-southeast-1.amazonaws.com/test/dummy-model"


'''-------------------DUMMY DATA--------------------'''

dummy_df = pd.read_csv("Data\dummy_data.csv")
dummy_df = dummy_df.drop('y', axis = 1)


result_array = np.zeros(500, dtype = object)   

for i in range(len(dummy_df.index)):
    current_x = dummy_df.iloc[i]['x']
    current_z = dummy_df.iloc[i]['z']
    response = requests.post(api_url, json= {"data":"%d, %d" %(current_x,current_z)})
    result_array[i] = response.json()[0]

print(result_array)

dummy_df['prediction'] = result_array.tolist()
print(dummy_df)


'''/-------------------DUMMY DATA--------------------'''


app = Flask(__name__)

#-----------TABLE MANIPULATION------------------
df = pd.read_csv('Data\DC Battery Report.csv')
data = df[['LRD','Rano Base Code', 'Administrative Status', 'Total Current Load']].copy()


data['Total Current Load'] = data['Total Current Load'].fillna(0).astype(float)
conditions = [
    (data['Total Current Load'] <=20),
    ((data['Total Current Load'] >20) & (data['Total Current Load'] <= 40)),
    ((data['Total Current Load'] >40) & (data['Total Current Load'] <= 70)),
    (data['Total Current Load'] >70)
]

values = ['Healthy', 'P1', 'P2', 'P3']


#set p1, p2, p3
data['Category'] = np.select(conditions, values)
data = data.sort_values(by= 'Category', ascending=False)
data = data.reset_index(drop=True)
#/-----------TABLE MANIPULATION------------------

@app.route('/')

@app.route('/index')
def index():
    category_values = {
        'P1': data.Category.value_counts().P1,
        'P2': data.Category.value_counts().P2,
        'P3': data.Category.value_counts().P3
    }
    return render_template('index.html', tables=[data.to_html(classes=["table table-striped table-bordered table-sm"])], 
    titles=[''], category_values = category_values)

@app.route('/EquipStats')
def EquipStats():
    return render_template('EquipStats.html', title='Equipment Stats')

@app.route('/MaintenanceSchedule')
def MaintenanceSchedule():
    return render_template('MaintenanceSchedule.html', title='Maintenance Schedule')


if __name__ == "__main__":
    app.run(debug=True) 