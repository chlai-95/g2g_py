from flask import Flask, request, render_template, redirect
import requests
import json
import os

from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('dashboard.html')
    
def getOptions(api_key):
    url = "https://free.currconv.com/api/v7/currencies?apiKey=" + api_key
    options = requests.get(url)
    if options.status_code == 200:
        _options = json.loads(options.content)
        return _options["results"]
    else:
        return ""
        
def getConvertedCurrency(api_key, _from, _to, _amount):
    value = {}
    base_q = _from + "_" + _to
    to_q = _to + "_" + _from
    url = "https://free.currconv.com/api/v7/convert?q=" + base_q + "," + to_q + "&compact=ultra&apiKey=" + api_key
    converted = requests.get(url)
    if converted.status_code == 200:
        _converted = json.loads(converted.content)
        print(str(_converted))
        normal_rate = _converted[base_q]
        revert_rate = _converted[to_q]
        
        normal_total = float(normal_rate) * _amount
        revert_total = float(revert_rate) * _amount
        formatted_normal_total = "{:.2f}".format(normal_total)
        formatted_revert_total = "{:.2f}".format(revert_total)
        
        value["normal"] = formatted_normal_total
        value["revert"] = formatted_revert_total
        
    return value
    
@app.route('/q1', methods=['GET', 'POST'])
def q1():
    return render_template('q1.html')
    
@app.route('/q2', methods=['GET', 'POST'])
def q2():
    apiKey = "95d300510ceee726ffc1"
    _from = ""
    _to = ""
    _amount = 0
    _options = getOptions(apiKey)
    _value = {}
    
    if request.method == "GET":
        _from = request.args.get('from')
        _to = request.args.get('to')
        _amount = request.args.get('amount')
        converted = False
        
        if _from and _to and _amount:
            converted = True
            _value = getConvertedCurrency(apiKey,_from,_to,int(_amount))
        else:
            converted = False
        
    return render_template('q2.html', converted=converted, _options=_options, _from=_from, _to=_to,_amount=_amount,_value=_value)

@app.route('/convert', methods=['POST'])
def lowercaseConvert():
    if request.form['target_text']:
        target_text = request.form['target_text']
        return str(target_text).lower()

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, Threading=True)
    app.run(host='0.0.0.0', debug=True, threaded=True)