#encoding:utf-8
from flask import Flask, jsonify, request, render_template
import simplejson as json
# import flaskext.couchdb
import couchdb
from couchdb.design import ViewDefinition


app = Flask(__name__)
server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')


@app.route('/')
def get_home():
    return render_template('homepage.html')


def get_dose_data(db):
    dose_x, dose_melb, dose_sy, dose_br, dose_ad, dose_da, dose_pe, dose_ho = [], [], [], [], [], [], [], []
    mango = {'selector': {}, 'fields': ['date', 'Melbourne', 'Sydney', 'Brisbane', 'Adelaide', 'Darwin', 'Perth', 'Hobart']}
    # for row in db.find(mango):
    for id in db:
        row = db.get(id)
        dose_x.append(row['date'])
        dose_melb.append(row['Melbourne'])
        dose_sy.append(row['Sydney'])
        dose_br.append(row['Brisbane'])
        dose_ad.append(row['Adelaide'])
        dose_da.append(row['Darwin'])
        dose_pe.append(row['Perth'])
        dose_ho.append(row['Hobart'])
    dose_x.reverse()
    dose_melb.reverse()
    dose_sy.reverse()
    dose_br.reverse()
    dose_ad.reverse()
    dose_da.reverse()
    dose_pe.reverse()
    dose_ho.reverse()
    # result = {'xAxis': dose_x.reverse(), 'Melbourne': dose_melb.reverse(), 'Sydney': dose_sy.reverse(), 'Brisbane': dose_br.reverse(), 'Adelaide': dose_ad.reverse(), 'Darwin': dose_da.reverse(), 'Perth': dose_pe.reverse(), 'Hobart': dose_ho.reverse()}
    # result = {'xAxis': dose_x[::-1], 'Melbourne': dose_melb[::-1], 'Sydney': dose_sy[::-1], 'Brisbane': dose_br[::-1], 'Adelaide': dose_ad[::-1], 'Darwin': dose_da[::-1], 'Perth': dose_pe[::-1], 'Hobart': dose_ho[::-1]}
    result = {'xAxis': dose_x, 'Melbourne': dose_melb, 'Sydney': dose_sy, 'Brisbane': dose_br, 'Adelaide': dose_ad, 'Darwin': dose_da, 'Perth': dose_pe, 'Hobart': dose_ho}
    return result


def get_twitter_data(db):
    melb_y, y = [], []
    melb_pos, melb_neg, sy_pos, sy_neg, br_pos, br_neg, ad_pos, ad_neg = [], [], [], [], [], [], [], []
    da_pos, da_neg, pe_pos, pe_neg, ho_pos, ho_neg, ca_pos, ca_neg = [], [], [], [], [], [], [], []
    melb_pos_rate, melb_neg_rate, melb_neu_rate, sy_pos_rate, sy_neg_rate, sy_neu_rate, br_pos_rate, br_neu_rate, br_neg_rate, ad_pos_rate, ad_neu_rate, ad_neg_rate = [], [], [], [], [], [], [], [], [], [], [], []
    da_pos_rate, da_neg_rate, da_neu_rate, pe_pos_rate, pe_neg_rate, pe_neu_rate, ho_pos_rate, ho_neg_rate, ho_neu_rate, ca_pos_rate, ca_neg_rate, ca_neu_rate = [], [], [], [], [], [], [], [],[], [], [], []
    melb_pol_score, melb_sub_score, sy_pol_score, sy_sub_score, br_pol_score, br_sub_score,ad_pol_score,ad_sub_score = [], [], [], [], [], [], [], []
    da_pol_score, da_sub_score, pe_pol_score, pe_sub_score, ho_pol_score, ho_sub_score = [], [], [], [], [], []
    pol_score, sub_score = [], []
    # mango = {'selector': {}, 'fields': ['date', 'Melbourne', 'Sydney', 'Brisbane', 'Adelaide', 'Darwin', 'Perth', 'Hobart']}
    # mango = {'selector': {}, 'fields': ['month', 'city', 'total', 'pos', 'neg', 'pol_score', 'sub_score']}
    # city = ['Melbourne', 'Sydney', 'Brisbane', 'Adelaide', 'Darwin', 'Perth', 'Hobart']
    X, Y = 0, 0
    # for row in db.find(mango):
    for id in db:
        row = db.get(id)
        if X > 15:
            X = 0
            Y += 1
        if row['city'] == 'melbourne':
            melb_pos.append(row['pos'])
            melb_neg.append(-row['neg'])
            melb_pos_rate.append(round(row['pos']/row['total']*100, 2))
            melb_neg_rate.append(round(row['neg']/row['total']*100, 2))
            melb_neu_rate.append(round(row['neu']/row['total']*100, 2))
            melb_y.append(row['month'])
        elif row['city'] == 'sydney':
            sy_pos.append(row['pos'])
            sy_neg.append(-row['neg'])
            sy_pos_rate.append(round(row['pos']/row['total']*100, 2))
            sy_neg_rate.append(round(row['neg']/row['total']*100, 2))
            sy_neu_rate.append(round(row['neu']/row['total']*100, 2))
            y.append(row['month'])
        elif row['city'] == 'brisbane':
            br_pos.append(row['pos'])
            br_neg.append(-row['neg'])
            br_pos_rate.append(round(row['pos']/row['total']*100, 2))
            br_neg_rate.append(round(row['neg']/row['total']*100, 2))
            br_neu_rate.append(round(row['neu']/row['total']*100, 2))
        elif row['city'] == 'adelaide':
            ad_pos.append(row['pos'])
            ad_neg.append(-row['neg'])
            ad_pos_rate.append(round(row['pos']/row['total']*100, 2))
            ad_neg_rate.append(round(row['neg']/row['total']*100, 2))
            ad_neu_rate.append(round(row['neu']/row['total']*100, 2))
        elif row['city'] == 'darwin':
            da_pos.append(row['pos'])
            da_neg.append(-row['neg'])
            da_pos_rate.append(round(row['pos']/row['total']*100, 2))
            da_neg_rate.append(round(row['neg']/row['total']*100, 2))
            da_neu_rate.append(round(row['neu']/row['total']*100, 2))
        elif row['city'] == 'perth(wa)':
            pe_pos.append(row['pos'])
            pe_neg.append(-row['neg'])
            pe_pos_rate.append(round(row['pos']/row['total']*100, 2))
            pe_neg_rate.append(round(row['neg']/row['total']*100, 2))
            pe_neu_rate.append(round(row['neu']/row['total']*100, 2))
        elif row['city'] == 'hobart':
            ho_pos.append(row['pos'])
            ho_neg.append(-row['neg'])
            ho_pos_rate.append(round(row['pos']/row['total']*100, 2))
            ho_neg_rate.append(round(row['neg']/row['total']*100, 2))
            ho_neu_rate.append(round(row['neu']/row['total']*100, 2))
        elif row['city'] == 'canberra':
            ca_pos.append(row['pos'])
            ca_neg.append(-row['neg'])
            ca_pos_rate.append(round(row['pos']/row['total']*100, 2))
            ca_neg_rate.append(round(row['neg']/row['total']*100, 2))
            ca_neu_rate.append(round(row['neu']/row['total']*100, 2))
        if row['month'] != '2022/5/1':
            pol_score.append([Y, X, round(row['pol_score'], 3)])
            sub_score.append([Y, X, round(row['sub_score'], 3)])
        X += 1
    pos_neg = {
        'y': y,
        'melb_y': melb_y,
        'melb_pos': melb_pos,
        'melb_neg': melb_neg,
        'sy_pos': sy_pos,
        'sy_neg': sy_neg,
        'br_pos': br_pos,
        'br_neg': br_neg,
        'da_pos': da_pos,
        'da_neg': da_neg,
        'ad_pos': ad_pos,
        'ad_neg': ad_neg,
        'pe_pos': pe_pos,
        'pe_neg': pe_neg,
        'ho_pos': ho_pos,
        'ho_neg': ho_neg,
        'ca_pos': ca_pos,
        'ca_neg': ca_neg
    }
    sentiment_rate = {
        'y': y,
        'melb_y': melb_y,
        'melb_pos_rate': melb_pos_rate,
        'melb_neg_rate': melb_neg_rate,
        'melb_neu_rate': melb_neu_rate,
        'sy_pos_rate': sy_pos_rate,
        'sy_neg_rate': sy_neg_rate,
        'sy_neu_rate': sy_neu_rate,
        'br_pos_rate': br_pos_rate,
        'br_neu_rate': br_neu_rate,
        'br_neg_rate': br_neg_rate,
        'ad_pos_rate': ad_pos_rate,
        'ad_neu_rate': ad_neu_rate,
        'ad_neg_rate': ad_neg_rate,
        'da_neg_rate': da_neg_rate,
        'da_neu_rate': da_neu_rate,
        'da_pos_rate': da_pos_rate,
        'pe_neg_rate': pe_neg_rate,
        'pe_neu_rate': pe_neu_rate,
        'pe_pos_rate': pe_pos_rate,
        'ho_pos_rate': ho_pos_rate,
        'ho_neg_rate': ho_neg_rate,
        'ho_neu_rate': ho_neu_rate,
        'ca_pos_rate': ca_pos_rate,
        'ca_neu_rate': ca_neu_rate,
        'ca_neg_rate': ca_neg_rate
    }
    heat_score = {'pol_score': pol_score, 'sub_score': sub_score}
    return pos_neg, heat_score, sentiment_rate


def get_doc_data(doc):
    doc = dict(doc)
    del doc['_id']
    del doc['_rev']
    if 'variable' in doc:
        del doc['variable']
    return doc


@app.route('/vaccination')
def get_vaccination():
    dose1 = get_dose_data(server['does1'])
    dose2 = get_dose_data(server['does2'])
    return render_template('vaccination_rate.html', dose1=dose1, dose2=dose2)


@app.route('/infection')
def get_infection():
    new_case = {
        'xAxis': list(get_doc_data(server['new_case'].get('AUS')).keys()),
        'new_case_AUS': list(get_doc_data(server['new_case'].get('AUS')).values()),
        'new_case_VIC': list(get_doc_data(server['new_case'].get('VIC')).values()),
        'new_case_Melb': list(get_doc_data(server['new_case'].get('Melb')).values())
    }
    new_case_per_million = {
        'xAxis': list(get_doc_data(server['new_case_per_million'].get('AUS')).keys()),
        'new_case_per_million_AUS': list(get_doc_data(server['new_case_per_million'].get('AUS')).values()),
        'new_case_per_million_VIC': list(get_doc_data(server['new_case_per_million'].get('VIC')).values()),
        'new_case_per_million_Melb': list(get_doc_data(server['new_case_per_million'].get('Melb')).values())
    }
    total_case = {
        'xAxis': list(get_doc_data(server['total_case'].get('AUS')).keys()),
        'total_case_AUS': list(get_doc_data(server['total_case'].get('AUS')).values()),
        'total_case_VIC': list(get_doc_data(server['total_case'].get('VIC')).values()),
        'total_case_Melb': list(get_doc_data(server['total_case'].get('Melb')).values())
    }
    total_case_per_million = {
        'xAxis': list(get_doc_data(server['total_case_per_million'].get('AUS')).keys()),
        'total_case_per_million_AUS': list(get_doc_data(server['total_case_per_million'].get('AUS')).values()),
        'total_case_per_million_VIC': list(get_doc_data(server['total_case_per_million'].get('VIC')).values()),
        'total_case_per_million_Melb': list(get_doc_data(server['total_case_per_million'].get('Melb')).values())
    }
    return render_template('infection_status.html', new_case=new_case, new_case_per_million=new_case_per_million, total_case=total_case, total_case_per_million=total_case_per_million)


@app.route('/sentiment')
def get_sentiment():
    pos_neg, heat_score, sentiment_rate = get_twitter_data(server['results_covid'])
    return render_template('sentiment_analysis.html', sentiment_rate=sentiment_rate, pos_neg=pos_neg, heat_score=heat_score)


@app.route('/enterprise')
def get_enterprise():
    income = []
    for id in server['income']:
        row = get_doc_data(server['income'].get(id))
        income.append(list(row.values()))
    return render_template('medical_status.html', income=income)


@app.route('/housing')
def get_housing():
    house = {
        '1': list(server['economic_and_industry'].get('e78cc88ab97d696a019b20be4636c46e').values())[2:-1],
        '2': list(server['economic_and_industry'].get('e78cc88ab97d696a019b20be4636cdff').values())[2:-1]
    }
    house_source = [
        ['product', 'Attached Dwelling', 'Housing'],
        ['Melbourne', house['1'][5], house['2'][5]],
        ['Adelaide', house['1'][0], house['2'][0]],
        ['Brisbane', house['1'][1], house['2'][1]],
        ['Darwin', house['1'][2], house['2'][2]],
        ['Hobart', house['1'][3], house['2'][3]],
        ['Perth', house['1'][4], house['2'][4]],
        ['Sydney', house['1'][6], house['2'][6]]
    ]
    return render_template('housing.html', house_source=house_source)


@app.route('/household')
def get_household():
    income = []
    for id in server['income']:
        row = get_doc_data(server['income'].get(id))
        income.append(list(row.values()))
    vehicle = []
    for id in server['motor_vechicles']:
        row = get_doc_data(server['motor_vechicles'].get(id))
        vehicle.append(list(row.values()))
    return render_template('household.html', income=income, vehicle=vehicle)


@app.route('/education')
def get_education():
    secondary = dict(get_doc_data(server['education'].get('e78cc88ab97d696a019b20be463ddf77')))
    preschool = dict(get_doc_data(server['education'].get('e78cc88ab97d696a019b20be463dfbcb')))
    technical = dict(get_doc_data(server['education'].get('e78cc88ab97d696a019b20be463dfab8')))
    other = dict(get_doc_data(server['education'].get('e78cc88ab97d696a019b20be463e0063')))
    oversea = dict(get_doc_data(server['education'].get('e78cc88ab97d696a019b20be463dedaf')))
    university = dict(get_doc_data(server['education'].get('e78cc88ab97d696a019b20be463deccb')))
    # melb, ade, br, da, ho, pe, sy = ['Melbourne',secondary['M'Melbourne'], ['Adelaide'], ['Brisbane'], ['Darwin'], ['Hobart'], ['Perth'], ['Sydney']
    # for i in range(6):
    #     melb.append(secondary['Melb'])
    # 'Preschool', 'Secondary', 'Technical or Further Educational',
    # 'University or other Tertiary', 'Oversea Visitor', 'Other Type'],
    source ={
        'cat':['product', 'Preschool', 'Secondary', 'Technical or Further Educational',
         'University or other Tertiary', 'Oversea Visitor', 'Other Type'],
        'Melbourne':[ preschool['Melbourne'], secondary['Melbourne'], technical['Melbourne'], university['Melbourne'], oversea['Melbourne'], other['Melbourne']],
        'Adelaide':[ preschool['Adelaide'], secondary['Adelaide'], technical['Adelaide'], university['Adelaide'], oversea['Adelaide'], other['Adelaide']],
        'Brisbane':[ preschool['Brisbane'], secondary['Brisbane'], technical['Brisbane'], university['Brisbane'], oversea['Brisbane'], other['Brisbane']],
        'Darwin':[ preschool['Darwin'], secondary['Darwin'], technical['Darwin'], university['Darwin'], oversea['Darwin'], other['Darwin']],
        'Hobart':[ preschool['Hobart'], secondary['Hobart'], technical['Hobart'], university['Hobart'], oversea['Hobart'], other['Hobart']],
        'Perth':[preschool['Perth'], secondary['Perth'], technical['Perth'], university['Perth'], oversea['Perth'], other['Perth']],
        'Sydney':[ preschool['Sydney'], secondary['Sydney'], technical['Sydney'], university['Sydney'], oversea['Sydney'], other['Sydney']],
    }
    # years_11 = dict(get_doc_data(server['highest_school_year'].get('e78cc88ab97d696a019b20be4639cdcb')))
    # years_9 = dict(get_doc_data(server['highest_school_year'].get('e78cc88ab97d696a019b20be4639d35e')))
    # years_10 = dict(get_doc_data(server['highest_school_year'].get('e78cc88ab97d696a019b20be4639da1c')))
    # years_12 = dict(get_doc_data(server['highest_school_year'].get('e78cc88ab97d696a019b20be4639e060')))
    # years_8 = dict(get_doc_data(server['highest_school_year'].get('e78cc88ab97d696a019b20be4639ee5a')))
    # highest_school_year = {
    # 'Melbourne' : [years_8['Melbourne'], years_9['Melbourne'], years_10['Melbourne'], years_11['Melbourne'],years_12['Melbourne']],
    # 'Adelaide' : [years_8['Adelaide'], years_9['Adelaide'], years_10['Adelaide'], years_11['Adelaide'],years_12['Adelaide']],
    # 'Brisbane' : [years_8['Brisbane'], years_9['Brisbane'], years_10['Brisbane'], years_11['Brisbane'],years_12['Brisbane']],
    # 'Darwin' : [years_8['Darwin'], years_9['Darwin'], years_10['Darwin'], years_11['Darwin'],years_12['Darwin']],
    # 'Hobart' : [years_8['Hobart'], years_9['Hobart'], years_10['Hobart'], years_11['Hobart'],years_12['Hobart']],
    # 'Perth' : [years_8['Perth'], years_9['Perth'], years_10['Perth'], years_11['Perth'],years_12['Perth']],
    # 'Sydney' : [years_8['Sydney'], years_9['Sydney'], years_10['Sydney'], years_11['Sydney'],years_12['Sydney']]
    # }
    # highest_school_year = {
    #     'years_8': list(years_8.values()),
    #     'years_9': list(years_9.values()),
    #     'years_10': list(years_10.values()),
    #     'years_11': list(years_11.values()),
    #     'years_12': list(years_12.values()),
    # }
    highest_school_year = []
    for id in server['highest_school_year']:
        row = get_doc_data(server['highest_school_year'].get(id))
        highest_school_year.append(list(row.values()))
    return render_template('education.html', source=source, highest_school_year=highest_school_year)


@app.route('/assistance')
def get_unpaid_assist():
    unpaid_assist = []
    for id in server['unpaid_assist']:
        row = get_doc_data(server['unpaid_assist'].get(id))
        unpaid_assist.append(list(row.values()))
    return render_template('unpaid_assistance.html', unpaid_assist=unpaid_assist)


@app.route('/mental')
def get_mental():
    pos_neg, heat_score, sentiment_rate = get_twitter_data(server['results_all'])
    return render_template('mental_health.html', sentiment_rate=sentiment_rate, pos_neg=pos_neg, heat_score=heat_score)


@app.route('/medical')
def get_medical():
    hospital = []
    for id in server['hospital']:
        row = get_doc_data(server['hospital'].get(id))
        hospital.append(list(row.values())[0])
    medical = []
    source = {
        'Melbourne': [i[0] for i in medical],
        'Adelaide': [i[3] for i in medical],
        'Brisbane': [i[2] for i in medical],
        'Darwin': [i[4] for i in medical],
        'Hobart': [i[6] for i in medical],
        'Perth': [i[5] for i in medical],
        'Sydney': [i[1] for i in medical]
    }
    return render_template('medical_status.html', hospital=hospital, source=source)


@app.route('/topic_trend')
def getTopic():
    vis_dict = dict(server['topics'].get('melbourne_2023-01_covid'))
    
    return render_template('topic_trend.html',vis_dict = vis_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)