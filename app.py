from flask import Flask, render_template, url_for
import pandas as pd
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',)

@app.route('/EquipStats')
def EquipStats():
    return render_template('EquipStats.html', title='Equipment Stats')

@app.route('/MaintenanceSchedule')
def MaintenanceSchedule():
    return render_template('MaintenanceSchedule.html', title='Maintenance Schedule')

if __name__ == "__main__":
    app.run(debug=True) 