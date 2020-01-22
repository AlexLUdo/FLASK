from flask import Flask, render_template, request, abort, redirect, url_for, send_file, jsonify
import requests
import json
import pprint

domain = 'https://api.hh.ru/'
url = f'{domain}vacancies'
params = {}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/address/")
def contacts():
    developer_name = 'Alex Udo'
    developer_phone_number = '+0(000)000-00-01'
    developer_mail = 'alex@00000.01'
    return render_template('address.html', name=developer_name, phone=developer_phone_number, mail=developer_mail)

@app.route("/zapros/", methods=['GET'])
def query():
        return render_template ('zapros.html')

@app.route("/zapros/", methods=['POST'])
def show_res():
    vacancy = request.form['vacancy']
    region = request.form['region']
    if region == '1': area = "Москва"
    if region == '2': area = "Санкт-Петербург"
    if region == '113': area = "Россия"
    params = {}
    params['text'] = vacancy
    area_query = int(region)
    params['area'] = str(area_query)
    result=requests.get(url, params = params).json()
    all_found_vac = result['found']
    vse_stranitsy = result['found']//100+1 if result['found']//100 <= 10 else 10
    vse_skily = {}
    kolvo = 0
    for i in range(vse_stranitsy):
        params['page']=i
        result=requests.get(url, params = params).json()
        for j in result['items']:
            rez_tmp=requests.get(j['url']).json()
            for i in rez_tmp['key_skills']:
                if i['name'] in vse_skily:
                    vse_skily[i['name']]+=1
                    kolvo +=kolvo
                else:
                    vse_skily.setdefault(i['name'], 1)

            file_name = str(('query_hh') + '.json')
            with open(file_name, 'w') as f:
                json.dump({'params': params}, f)
                json.dump({'count': all_found_vac}, f)
                json.dump({'skills': vse_skily}, f)

    return render_template('rezultat.html', salary=all_found_vac, vacancy=vacancy, data=vse_skily, area = area)

if __name__ == "__main__":
    app.run(debug=True)
