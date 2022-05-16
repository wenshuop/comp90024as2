"""
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
"""

import numpy as np
import pandas as pd
import os
import couchdb

cityNames = ["Melbourne", "Sydney", "Brisbane",
             "Adelaide", "Darwin", "Perth", "Hobart"]

"""
data loading and preprocessing
"""

# population
pop1 = pd.read_csv(
    'data\population\dese_sa4_pop_by_lbr_frc_stat_dec_2021-3825329153799819356.csv')
pop2 = pd.read_csv(
    'data\population\dese_sa4_pop_by_lbr_frc_stat_dec_2021-5348249873643618355.csv')
pop3 = pd.read_csv(
    'data\population\dese_sa4_pop_by_lbr_frc_stat_dec_2021-6738827427384364798.csv')
pop4 = pd.read_csv(
    'data\population\dese_sa4_pop_by_lbr_frc_stat_dec_2021-7349209524282383716.csv')

popTable = pd.DataFrame(
    np.zeros((7, 1)), index=cityNames, columns=["population"])

for l in pop1.index:
    for c in cityNames:
        if c in pop1.iloc[l, 4]:
            popTable.loc[c, "population"] = popTable.loc[c,
                                                         "population"]+pop1.iloc[l, 2]

for l in pop2.index:
    for c in cityNames:
        if c in pop2.iloc[l, 4]:
            popTable.loc[c, "population"] = popTable.loc[c,
                                                         "population"]+pop2.iloc[l, 2]

for l in pop3.index:
    for c in cityNames:
        if c in pop3.iloc[l, 4]:
            popTable.loc[c, "population"] = popTable.loc[c,
                                                         "population"]+pop3.iloc[l, 2]

for l in pop4.index:
    for c in cityNames:
        if c in pop4.iloc[l, 4]:
            popTable.loc[c, "population"] = popTable.loc[c,
                                                         "population"]+pop4.iloc[l, 2]

# hospital
hospital = pd.read_excel(
    'data\hospital\mapping-details.xlsx', sheet_name='Sheet1')
hospital = hospital.dropna(axis=0, how='any')
hospital.index = range(0, len(hospital.index), 1)
hospital['city'] = ''

for h in hospital.index:
    for c in cityNames:
        if c in hospital.loc[h, 'Name'] or c in hospital.loc[h, 'Local Hospital Network (LHN)'] or c in hospital.loc[h, 'Primary Health Network area (PHN)']:
            hospital.loc[h, 'city'] = c

hospitalTable = hospital.groupby('city').agg('count').iloc[1:8, 0]

# Economy and Industry
ecoInd = pd.read_csv(
    'data\Economy and Industry\\abs_data_by_region_economy_and_industry_lga_2011_2019-1193984204860490229.csv')
ecoInd['city'] = ''

for u in ecoInd.index:
    for c in cityNames:
        if c in ecoInd.loc[u, ' lga_name_2019']:
           ecoInd.loc[u, 'city'] = c

ecoIndTable = ecoInd.groupby('city').agg('sum').iloc[1:8, [1, 2, 3, 6, 7, 8]]
houseTable = ecoIndTable.iloc[:, [1, 3]]
businessTable = ecoIndTable.iloc[:, [0, 2, 4, 5]]
sumTable = np.sum(businessTable, axis=1)
businessPerTable = businessTable

for i in sumTable.index:
    businessPerTable.loc[i, :] = round(
        businessTable.loc[i, :]/sumTable[i]*100, 2)

# vaccination
filePath = r"data\vaccine\\"
nameList = os.listdir(filePath)
a = pd.DataFrame()

for i in nameList:
    temp = pd.read_excel(filePath+i, skiprows=[0, 1, 2, 3], header=4)
    temp['date'] = i[0:8]
    a = pd.concat([temp, a], axis=0, ignore_index=True)

for l in a.index:
    if pd.isnull(a.iloc[l, 8]) == False:
        a.iloc[l, 0] = a.iloc[l, 8]
    if pd.isnull(a.iloc[l, 9]) == False:
        a.iloc[l, 6] = a.iloc[l, 9]
    if pd.isnull(a.iloc[l, 10]) == False:
        a.iloc[l, 3] = a.iloc[l, 10]
    if pd.isnull(a.iloc[l, 11]) == False:
        a.iloc[l, 4] = a.iloc[l, 11]
    if pd.isnull(a.iloc[l, 12]) == False:
        a.iloc[l, 3] = a.iloc[l, 12]
    if pd.isnull(a.iloc[l, 13]) == False:
        a.iloc[l, 4] = a.iloc[l, 13]
    if pd.isnull(a.iloc[l, 14]) == False:
        a.iloc[l, 0] = a.iloc[l, 14]
    if pd.isnull(a.iloc[l, 15]) == False:
        a.iloc[l, 1] = a.iloc[l, 15]
    if pd.isnull(a.iloc[l, 16]) == False:
        a.iloc[l, 3] = a.iloc[l, 16]
    if pd.isnull(a.iloc[l, 17]) == False:
        a.iloc[l, 4] = a.iloc[l, 17]
    if pd.isnull(a.iloc[l, 18]) == False:
        a.iloc[l, 6] = a.iloc[l, 18]
    if isinstance(a.iloc[l, 3], str) and '>' in a.iloc[l, 3]:
        a.iloc[l, 3] = a.iloc[l, 3].replace('>', '')
    if isinstance(a.iloc[l, 4], str) and '>' in a.iloc[l, 4]:
        a.iloc[l, 4] = a.iloc[l, 4].replace('>', '')
    if isinstance(a.iloc[l, 3], str) and '%' in a.iloc[l, 3]:
        a.iloc[l, 3] = a.iloc[l, 3].replace('%', '')
        a.iloc[l, 3] = float(a.iloc[l, 3])/100
    if isinstance(a.iloc[l, 4], str) and '%' in a.iloc[l, 4]:
        a.iloc[l, 4] = a.iloc[l, 4].replace('%', '')
        a.iloc[l, 4] = float(a.iloc[l, 4])/100

vacc = a.dropna(axis=0, subset='LGA 2020 Name of Residence')
vacc.index = range(0, len(vacc.index), 1)
col = list(set(vacc['date']))
col.sort(key=list(vacc['date']).index)
does1Table = pd.DataFrame(index=cityNames, columns=col)
does2Table = pd.DataFrame(index=cityNames, columns=col)

for l in vacc.index:
    for c in cityNames:
        if c in vacc.iloc[l, 0]:
            does1Table.loc[c, vacc.iloc[l, 7]] = vacc.iloc[l, 3]
            does2Table.loc[c, vacc.iloc[l, 7]] = vacc.iloc[l, 4]

# 2016census
# income
income = pd.read_csv(
    'data\\2016census\lga_g17c_total_weekly_income_by_age_by_sex_census_2016-8922474670371012024.csv')
incomeTable = pd.DataFrame(index=cityNames, columns=income.columns)

for i in income.index:
    for c in cityNames:
        if c in income.loc[i, ' lga_name_2016']:
            incomeTable.loc[c, :] = income.loc[i, :]

incomeTable = incomeTable.drop(
    axis=1, columns=[' p_tot_tot', ' lga_name_2016', ' lga_code_2016'])
sumTable = np.sum(incomeTable, axis=1)
incomePerTable = incomeTable

for i in sumTable.index:
    incomePerTable.loc[i, :] = round(pd.to_numeric(
        incomeTable.loc[i, :]/sumTable[i])*100, 2)

# unpaid assist
asst = pd.read_csv(
    'data\\2016census\lga_g21_unpaid_asst_disability_by_age_by_sex_census_2016-4202822233078350057.csv')
asstTable = pd.DataFrame(index=cityNames, columns=asst.columns)

for a in asst.index:
    for c in cityNames:
        if c in asst.loc[a, ' lga_name_2016']:
            asstTable.loc[c, :] = asst.loc[a, :]

asstTable = asstTable.drop(axis=1, columns=[
                           ' lga_name_2016', ' lga_code_2016', ' p_35_44_prvided_unpaid_assist', ' p_tot_prvided_unpaid_assist'])
sumTable = np.sum(asstTable, axis=1)
asstPerTable = asstTable

for i in sumTable.index:
    asstPerTable.loc[i, :] = round(pd.to_numeric(
        asstTable.loc[i, :]/sumTable[i]*100), 2)

# education
edu = pd.read_csv(
    'data\\2016census\lga_p15_type_of_edu_institute_by_age_by_sex_census_2016-8799573898846241340.csv')
eduTable = pd.DataFrame(index=cityNames, columns=edu.columns)

for a in edu.index:
    for c in cityNames:
        if c in edu.loc[a, ' lga_name16']:
            eduTable.loc[c, :] = edu.loc[a, :]

eduTable = eduTable.drop(axis=1, columns=[' lga_name16', ' lga_code_2016'])
sumTable = np.sum(eduTable, axis=1)
eduPerTable = eduTable

for i in sumTable.index:
    eduPerTable.loc[i, :] = round(pd.to_numeric(
        eduTable.loc[i, :]/sumTable[i]*100), 2)

# highest school
highSchool1 = pd.read_csv(
    'data\\2016census\lga_g16a_highest_yr_sch_by_age_by_sex_census_2016-242818756609709776.csv')
highSchool2 = pd.read_csv(
    'data\\2016census\lga_g16b_highest_yr_sch_by_age_by_sex_census_2016-4224916417172492654.csv')
highSchool = pd.concat(
    [highSchool1.iloc[:, [0, 1, 2, 5]], highSchool2], axis=1)
highSchoolTable = pd.DataFrame(index=cityNames, columns=highSchool.columns)

for a in highSchool.index:
    for c in cityNames:
        if c in highSchool.loc[a, 'lga_name_2016']:
           highSchoolTable.loc[c, :] = highSchool.loc[a, :]

highSchoolTable = highSchoolTable.drop(
    axis=1, columns=['lga_name_2016', ' lga_code_2016'])
sumTable = np.sum(highSchoolTable, axis=1)
highSchoolPerTable = highSchoolTable

for i in sumTable.index:
    highSchoolPerTable.loc[i, :] = round(pd.to_numeric(
        highSchoolTable.loc[i, :]/sumTable[i]*100), 2)

# motor vechicles
vechicles = pd.read_csv(
    'data\\2016census\lga_p29_number_motor_vehicles_by_dwelling_census_2016-401818911354611350.csv')
vechiclesTable = pd.DataFrame(index=cityNames, columns=vechicles.columns)

for a in vechicles.index:
    for c in cityNames:
        if c in vechicles.loc[a, ' lga_name16']:
           vechiclesTable.loc[c, :] = vechicles.loc[a, :]

vechiclesTable = vechiclesTable.drop(
    axis=1, columns=[' lga_name16', ' lga_code_2016', ' num_mvs_per_dweling_tot'])
sumTable = np.sum(vechiclesTable, axis=1)
vechiclesPerTable = vechiclesTable

for i in sumTable.index:
    vechiclesPerTable.loc[i, :] = round(pd.to_numeric(
        vechiclesTable.loc[i, :]/sumTable[i]*100), 2)

# medical benefits
medBenefit = pd.read_csv(
    'data\\2016census\lga11_mbsservices-5858320487229155198.csv')
medBenefitTable = pd.DataFrame(index=cityNames, columns=medBenefit.columns)

for a in medBenefit.index:
    for c in cityNames:
        if c in medBenefit.loc[a, ' area_name']:
          medBenefitTable.loc[c, :] = medBenefit.loc[a, :]

medBenefitTable = medBenefitTable.drop(
    axis=1, columns=[' area_name', ' area_code'])
sumTable = np.sum(medBenefitTable, axis=1)
medBenefitPerTable = medBenefitTable

for i in sumTable.index:
    medBenefitPerTable.loc[i, :] = round(pd.to_numeric(
        medBenefitTable.loc[i, :]/sumTable[i]*100), 2)

# confirmed case
# AUS
caseAUS = pd.read_csv('data\confirmed case\owid-covid-data.csv')
caseAUSTable = caseAUS.iloc[:, [3, 4, 5, 10, 11]]
caseAUSTable.index = caseAUSTable.loc[:, 'date']
caseAUSTable = caseAUSTable.iloc[:, 1:]
caseAUSTable = caseAUSTable.dropna()
caseAUSj = caseAUSTable.to_dict()

caseAUSj['new_cases']['_id'] = 'AUS'
caseAUSj['new_cases_per_million']['_id'] = 'AUS'
caseAUSj['total_cases']['_id'] = 'AUS'
caseAUSj['total_cases_per_million']['_id'] = 'AUS'

# VIC
caseVIC = pd.read_csv(
    'data\confirmed case\\NCOV_COVID_Cases_by_LGA_Source_20220504.csv')
newcaseVIC = caseVIC.groupby('diagnosis_date').agg('count')['Postcode']
caseVICTable = pd.DataFrame(np.zeros((len(caseAUSTable.index), len(
    caseAUSTable.columns))), index=caseAUSTable.index, columns=caseAUSTable.columns)

for c in newcaseVIC.index:
    if c in caseVICTable.index:
        caseVICTable.loc[c, 'new_cases'] = newcaseVIC.loc[c]

VICdate = pd.to_datetime(newcaseVIC.index.to_series(), format='%Y/%m/%d')
case2020 = sum(newcaseVIC[VICdate.dt.year == 2020])

for t in range(0, len(caseVICTable.index), 1):
    if t == 0:
        caseVICTable.iloc[t, 0] = case2020+caseVICTable.iloc[t, 1]
    else:
        caseVICTable.iloc[t, 0] = caseVICTable.iloc[t-1, 0] + \
            caseVICTable.iloc[t, 1]

VICpop1 = pop1.loc[pop1[' state_name_abbr'] == 'VIC']
VICpop2 = pop2.loc[pop2[' state_name_abbr'] == 'VIC']
VICpop3 = pop3.loc[pop3[' state_name_abbr'] == 'VIC']
VICpop4 = pop4.loc[pop4[' state_name_abbr'] == 'VIC']
VICpop = sum(VICpop1[' p'])+sum(VICpop2[' p']) + \
    sum(VICpop3[' p'])+sum(VICpop4[' p'])
caseVICTable['new_cases_per_million'] = caseVICTable['new_cases']/VICpop*1000000
caseVICTable['total_cases_per_million'] = caseVICTable['total_cases']/VICpop*1000000
caseVICj = caseVICTable.to_dict()
caseVICj['new_cases']['_id'] = 'VIC'
caseVICj['total_cases']['_id'] = 'VIC'
caseVICj['new_cases_per_million']['_id'] = 'VIC'
caseVICj['total_cases_per_million']['_id'] = 'VIC'

# Melbourne
caseMelb = caseVIC[caseVIC['Localgovernmentarea'] == 'Melbourne (C)']
newcaseMelb = caseMelb.groupby('diagnosis_date').agg('count')['Postcode']
caseMelbTable = pd.DataFrame(np.zeros((len(caseAUSTable.index), len(
    caseAUSTable.columns))), index=caseAUSTable.index, columns=caseAUSTable.columns)

for c in newcaseMelb.index:
    if c in caseMelbTable.index:
        caseMelbTable.loc[c, 'new_cases'] = newcaseMelb.loc[c]

Melbdate = pd.to_datetime(newcaseMelb.index.to_series(), format='%Y/%m/%d')
case2020 = sum(newcaseMelb[Melbdate.dt.year == 2020])

for t in range(0, len(caseMelbTable.index), 1):
    if t == 0:
        caseMelbTable.iloc[t, 0] = case2020+caseMelbTable.iloc[t, 1]
    else:
        caseMelbTable.iloc[t, 0] = caseMelbTable.iloc[t -
                                                      1, 0]+caseMelbTable.iloc[t, 1]

Melbpop = popTable.loc['Melbourne', 'population']
caseMelbTable['new_cases_per_million'] = caseMelbTable['new_cases'] / \
    Melbpop*1000000
caseMelbTable['total_cases_per_million'] = caseMelbTable['total_cases'] / \
    Melbpop*1000000

caseMelbj = caseMelbTable.to_dict()
caseMelbj['new_cases']['_id'] = 'Melb'
caseMelbj['total_cases']['_id'] = 'Melb'
caseMelbj['new_cases_per_million']['_id'] = 'Melb'
caseMelbj['total_cases_per_million']['_id'] = 'Melb'

"""
data storing
"""

# couchDB
def createDB(serverDB, db):
    if db in serverDB:
        serverDB.delete(db)
    return serverDB.create(db)

DBpath = 'http://admin:admin@172.26.128.22:5984/'
couch = couchdb.Server(DBpath)

popDB = createDB(couch, 'population2021')
popj = popTable['population'].to_dict()
for j in popj.keys():
    popDB.save({j: popj[j]})

hospitalDB = createDB(couch, 'hospital')
hospitalj = hospitalTable.to_dict()
for j in hospitalj.keys():
    hospitalDB.save({j: hospitalj[j]})

businessPerDB = createDB(couch, 'business')
businessPerj = businessPerTable.to_dict()
for j in businessPerj.keys():
    businessPerj[j]['variable'] = j
    businessPerDB.save(businessPerj[j])

houseDB = createDB(couch, 'house_price')
housej = houseTable.to_dict()
for j in housej.keys():
    housej[j]['variable'] = j
    houseDB.save(housej[j])

does1DB = createDB(couch, 'does1')
does1j = does1Table.to_dict()
for j in does1j.keys():
    does1j[j]['date'] = j
    does1DB.save(does1j[j])

does2DB = createDB(couch, 'does2')
does2j = does2Table.to_dict()
for j in does2j.keys():
    does2j[j]['date'] = j
    does2DB.save(does2j[j])

incomeDB = createDB(couch, 'income')
incomej = incomeTable.to_dict()
for j in incomej.keys():
    incomej[j]['variable'] = j
    incomeDB.save(incomej[j])

asstDB = createDB(couch, 'unpaid_assist')
asstj = asstTable.to_dict()
for j in asstj.keys():
    asstj[j]['variable'] = j
    asstDB.save(asstj[j])

eduDB = createDB(couch, 'education')
eduj = eduTable.to_dict()
for j in eduj.keys():
    eduj[j]['variable'] = j
    eduDB.save(eduj[j])

highSchoolDB = createDB(couch, 'highest_school_year')
highSchoolj = highSchoolTable.to_dict()
for j in highSchoolj.keys():
    highSchoolj[j]['variable'] = j
    highSchoolDB.save(highSchoolj[j])

vechiclesDB = createDB(couch, 'motor_vechicles')
vechiclesj = vechiclesTable.to_dict()
for j in vechiclesj.keys():
    vechiclesj[j]['variable'] = j
    vechiclesDB.save(vechiclesj[j])


medBenefitDB = createDB(couch, 'medical_benefits')
medBenefitj = medBenefitTable.to_dict()
for j in medBenefitj.keys():
    medBenefitj[j]['variable'] = j
    medBenefitDB.save(medBenefitj[j])


newCaseDB = createDB(couch, 'new_case')
newCaseDB.save(caseAUSj['new_cases'])
newCaseDB.save(caseVICj['new_cases'])
newCaseDB.save(caseMelbj['new_cases'])

totalCaseDB = createDB(couch, 'total_case')
totalCaseDB.save(caseAUSj['total_cases'])
totalCaseDB.save(caseVICj['total_cases'])
totalCaseDB.save(caseMelbj['total_cases'])

newCasePerMillionDB = createDB(couch, 'new_case_per_million')
newCasePerMillionDB.save(caseAUSj['new_cases_per_million'])
newCasePerMillionDB.save(caseVICj['new_cases_per_million'])
newCasePerMillionDB.save(caseMelbj['new_cases_per_million'])

totalCasePerMillionDB = createDB(couch, 'total_case_per_million')
totalCasePerMillionDB.save(caseAUSj['total_cases_per_million'])
totalCasePerMillionDB.save(caseVICj['total_cases_per_million'])
totalCasePerMillionDB.save(caseMelbj['total_cases_per_million'])
