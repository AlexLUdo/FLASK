from flask import Flask, render_template, request, abort, redirect, url_for, send_file, jsonify
import requests, re, sqlite3
from alch import put, get

domain = 'https://api.hh.ru/'
url = f'{domain}vacancies'
params = {}
vacancies = {}

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
    vacanc = request.form['vacancy']
    region = request.form['region']
    if region == '1': area = "Москва"
    if region == '2': area = "Санкт-Петербург"
    if region == '113': area = "Россия"
    if region == '1001': area = "ДРУГИЕ РЕГИОНЫ"
    if region == '5':  area = "УКРАИНА"
    if region == '16':  area = "БЕЛОРУССИЯ"
    if region == '40':  area = "Казахстан"
    if region == '70':  area = "ЕЙСК"
    params = {}
    params['text'] = vacanc
    area_query = int(region)
    params['area'] = str(area_query)
    result=requests.get(url, params = params).json()
    all_found_vac = result['found']
    vse_stranitsy = result['found']//100+1 if result['found']//100 <= 20 else 20
    vse_skily = {}

    for i in range(vse_stranitsy):
        params['page']=i
        result=requests.get(url, params = params).json()
        for j in result['items']:
            rez_tmp=requests.get(j['url']).json()
            for i in rez_tmp['key_skills']:
                if i['name'] in vse_skily:
                    vse_skily[i['name']]+=1

                else:
                    vse_skily.setdefault(i['name'], 1)

            if all_found_vac == False: all_found_vac = 0
            put(vacanc,area,all_found_vac,vse_skily)
            return render_template('rezultat.html', salary=all_found_vac, vacanc=vacanc, data=vse_skily, area=area)

@app.route("/base/", methods=['GET'])
def queryb():
        return render_template ('zaprosb.html')

@app.route("/base/", methods=['POST'])
def show_resb():
    vacanc = request.form['vacanc']
    region = request.form['region']
    if region == '1':   area = "Москва"
    if region == '2':   area = "Санкт-Петербург"
    if region == '113': area = "Россия"
    if region == '1001':area = "ДРУГИЕ РЕГИОНЫ"
    if region == '5':   area = "УКРАИНА"
    if region == '16':  area = "БЕЛОРУССИЯ"
    if region == '40':  area = "Казахстан"
    if region == '70':  area = "ЕЙСК"

    vacancies = get(area, vacanc)
    return render_template('rezultatb.html', vacancies=vacancies, area=area, vacanc=vacanc)

if __name__ == "__main__":
    app.run(debug=True)
