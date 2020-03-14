import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

'''
This was used to match up readable addresses for query again google geocode API
It output a simple dataframe:
original address || response for neighborhood || reponse for lat-long
'''

#addresses to geocode
file = 'address.xlsx'
df = pd.read_excel(file)

#formatted request
def send2google(address):
    address = address.replace(' ', '+')
    apikey = 'YOUR_API_KEY'
    request = 'https://maps.googleapis.com/maps/api/geocode/json?address='\
                + address+'&key='+apikey
    print(request)
    return request

#send/read response
def neigh(row):
    response = (requests.get(row).json())
    neighborhood = response['results'][0]['address_components'][2]['long_name']
    return neighborhood

def geo(row):
    response = (requests.get(row).json())
    geo = response['results'][0]['geometry']
    return geo

#prep address by replacing space with +
df['GoogleAPI'] = df['GoogleAPI'].replace(' ','+')

#writing the responses in the appropriate columns
df['GoogleRequest'] = df['GoogleAPI'].apply(send2google)
df['GoogleResponse'] = df['GoogleRequest'].apply(neigh)
df['GoogleResponse1'] = df['GoogleRequest'].apply(geo)


#for debug
with pd.ExcelWriter('google.xlsx') as writer:
    df.to_excel(writer, index = False)

print('Complete!')
