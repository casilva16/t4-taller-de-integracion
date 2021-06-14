####  TAREA 4  ####
## PAISES ESCOGIDOS: BELICE, GRECIA, SINGAPUR, JAPON, RUSIA, URUGUAY ##
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from gspread_dataframe import set_with_dataframe
import gspread

## GET DATA ##
b = requests.get('https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_BLZ.xml')
g = requests.get('https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_GRC.xml')
s = requests.get('https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_SGP.xml')
j = requests.get('https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_JPN.xml')
r = requests.get('https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_RUS.xml')
u = requests.get('https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_URY.xml')

root_belice = ET.XML(b.content)
root_greece = ET.XML(g.content)
root_singapure = ET.XML(s.content)
root_japan = ET.XML(j.content)
root_rusia = ET.XML(r.content)
root_uruguay = ET.XML(u.content)

dataframe = []

data_belice = {'GHO': None, 'YEAR': None, 'SEX': None, 'COUNTRY': None, 'AGEGROUP': None, 'GHECAUSES': None, 'Display': None, 'Numeric': None, 'Low': None, 'High': None}
data_greece = {'GHO': None, 'YEAR': None, 'SEX': None, 'COUNTRY': None, 'AGEGROUP': None, 'GHECAUSES': None, 'Display': None, 'Numeric': None, 'Low': None, 'High': None}
data_singapure = {'GHO': None, 'YEAR': None, 'SEX': None, 'COUNTRY': None, 'AGEGROUP': None, 'GHECAUSES': None, 'Display': None, 'Numeric': None, 'Low': None, 'High': None}
data_japan = {'GHO': None, 'YEAR': None, 'SEX': None, 'COUNTRY': None, 'AGEGROUP': None, 'GHECAUSES': None, 'Display': None, 'Numeric': None, 'Low': None, 'High': None}
data_rusia = {'GHO': None, 'YEAR': None, 'SEX': None, 'COUNTRY': None, 'AGEGROUP': None, 'GHECAUSES': None, 'Display': None, 'Numeric': None, 'Low': None, 'High': None}
data_uruguay = {'GHO': None, 'YEAR': None, 'SEX': None, 'COUNTRY': None, 'AGEGROUP': None, 'GHECAUSES': None, 'Display': None, 'Numeric': None, 'Low': None, 'High': None}

nodos_hijos = ['GHO',
'COUNTRY', 'SEX', 'YEAR', 'GHECAUSES', 'AGEGROUP', 'Display', 'Numeric', 'Low', 'High']

Indicadores_de_muertes = ['Number of deaths', 
'Number of infant deaths', 
'Number of under-five deaths',
'Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)',
'Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)',
'Estimates of number of homicides', 
'Crude suicide rates (per 100 000 population)', 
'Mortality rate attributed to unintentional poisoning (per 100 000 population)', 
'Number of deaths attributed to non-communicable diseases, by type of disease and sex',
'Estimated road traffic death rate (per 100 000 population)',
'Estimated number of road traffic deaths']

Indicadores_de_peso = ['Mean BMI (kg/m&#xb2;) (crude estimate)', 
'Mean BMI (kg/m&#xb2;) (age-standardized estimate)',
'Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)',
'Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)',
'Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)',
'Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)',
'Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)',
'Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)']

Otros_indicadores_de_salud = [
'Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)',
'Estimate of daily cigarette smoking prevalence (%)',
'Estimate of daily tobacco smoking prevalence (%)',
'Estimate of current cigarette smoking prevalence (%)', 
'Estimate of current tobacco smoking prevalence (%)',
'Mean systolic blood pressure (crude estimate)',
'Mean fasting blood glucose (mmol/l) (crude estimate)',
'Mean Total Cholesterol (crude estimate)']

indicadores = ['Number of deaths', 
'Number of infant deaths', 
'Number of under-five deaths',
'Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)',
'Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)',
'Estimates of number of homicides', 
'Crude suicide rates (per 100 000 population)', 
'Mortality rate attributed to unintentional poisoning (per 100 000 population)', 
'Number of deaths attributed to non-communicable diseases, by type of disease and sex',
'Estimated road traffic death rate (per 100 000 population)',
'Estimated number of road traffic deaths',
'Mean BMI (kg/m&#xb2;) (crude estimate)', 
'Mean BMI (kg/m&#xb2;) (age-standardized estimate)',
'Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)',
'Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)',
'Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)',
'Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)',
'Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)',
'Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)',
'Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)',
'Estimate of daily cigarette smoking prevalence (%)',
'Estimate of daily tobacco smoking prevalence (%)',
'Estimate of current cigarette smoking prevalence (%)', 
'Estimate of current tobacco smoking prevalence (%)',
'Mean systolic blood pressure (crude estimate)',
'Mean fasting blood glucose (mmol/l) (crude estimate)',
'Mean Total Cholesterol (crude estimate)']

## iter over de roots
## BELICE ##
for child in root_belice:
  for elem in child:
    if elem.tag == 'GHO':
      gho_data = [elem.text]
    if elem.tag == 'Numeric' or elem.tag == 'Low' or elem.tag == 'High':
      data_belice[elem.tag] == float(elem.text)
    if elem.tag in nodos_hijos:
      data_belice[elem.tag] = elem.text
  
  if gho_data[0] in indicadores:
    dataframe.append(data_belice)  

## GREECE ##
for child in root_greece:
  for elem in child:
    if elem.tag == 'GHO':
      gho_data = [elem.text]
    if elem.tag == 'Numeric' or elem.tag == 'Low' or elem.tag == 'High':
      data_greece[elem.tag] == float(elem.text)
    if elem.tag in nodos_hijos:
      data_greece[elem.tag] = elem.text
  
  if gho_data[0] in indicadores:
    dataframe.append(data_greece)

## SINGAPURE ##
for child in root_singapure:
  for elem in child:
    if elem.tag == 'GHO':
      gho_data = [elem.text]
    if elem.tag == 'Numeric' or elem.tag == 'Low' or elem.tag == 'High':
      data_singapure[elem.tag] == float(elem.text)
    if elem.tag in nodos_hijos:
      data_singapure[elem.tag] = elem.text
  
  if gho_data[0] in indicadores:
    dataframe.append(data_singapure)

## JAPAN ##
for child in root_japan:
  for elem in child:
    if elem.tag == 'GHO':
      gho_data = [elem.text]
    if elem.tag == 'Numeric' or elem.tag == 'Low' or elem.tag == 'High':
      data_japan[elem.tag] == float(elem.text)
    if elem.tag in nodos_hijos:
      data_japan[elem.tag] = elem.text
  
  if gho_data[0] in indicadores:
    dataframe.append(data_japan)

## RUSIA ##
for child in root_rusia:
  for elem in child:
    if elem.tag == 'GHO':
      gho_data = [elem.text]
    if elem.tag == 'Numeric' or elem.tag == 'Low' or elem.tag == 'High':
      data_rusia[elem.tag] == float(elem.text)
    if elem.tag in nodos_hijos:
      data_rusia[elem.tag] = elem.text
  
  if gho_data[0] in indicadores:
    dataframe.append(data_rusia)

## URUGUAY ##
for child in root_uruguay:
  for elem in child:
    if elem.tag == 'GHO':
      gho_data = [elem.text]
    if elem.tag == 'Numeric' or elem.tag == 'Low' or elem.tag == 'High':
      data_uruguay[elem.tag] == float(elem.text)
    if elem.tag in nodos_hijos:
      data_uruguay[elem.tag] = elem.text
  
  if(gho_data[0] in indicadores):
    dataframe.append(data_uruguay)

# for i in dataframe:
#   print(i)

## ACCES GOOGLE SHEET
gc = gspread.service_account(filename='api_keys.JSON')
sh = gc.open_by_key('1vNqUu956RUXvMPeOBJfQCyZi9pcRab0gdaFZlQ8U_hc')
worksheet = sh.get_worksheet(0)
new_dataframe = pd.DataFrame(dataframe)
set_with_dataframe(worksheet, new_dataframe)
