from django.http import HttpResponse
from django.shortcuts import render
import pickle
import pandas as pd
import numpy as np
from django.contrib.staticfiles.storage import staticfiles_storage
df = pd.read_csv('./model/data_2.csv')
pipe = pickle.load(open('./model/pipe.pkl', 'rb'))

def index(request):
    global df
    full_name = sorted(df['full_name'].unique())
    seller_type = sorted(df['seller_type'].unique())
    owner_type = sorted(df['owner_type'].unique())
    fuel_type = sorted(df['fuel_type'].unique())
    transmission_type = sorted(df['transmission_type'].unique())
    contex = {
        'full_name': full_name,
        'seller_type': seller_type,
        'owner_type': owner_type,
        'fuel_type': fuel_type,
        'transmission_type': transmission_type,
       
    }
    return render(request, 'myApp/index.html', contex)


def predict(request):
    global pipe
    if request.method == "POST":
        name = request.POST.get('name')
        seller_type = request.POST.get('seller_type')
        owner_type = request.POST.get('owner_type')
        fuel_type = request.POST.get('fuel_type')
        transmission_type = request.POST.get('transmission_type')
        engine = int(request.POST.get('engine'))
        year = int(request.POST.get('year'))
        km_driven =int( request.POST.get('kmDriven'))
        mileage = int(request.POST.get('mileage'))
        max_power = int(request.POST.get('maxPower'))

        try:
            
            prediction =pipe.predict(pd.DataFrame([[name, year, seller_type, km_driven, owner_type, fuel_type, transmission_type, mileage, engine, max_power]], columns=[
                         'full_name', 'year', 'seller_type', 'km_driven', 'owner_type', 'fuel_type', 'transmission_type', 'mileage', 'engine', 'max_power']))
            return HttpResponse(str(np.round(prediction[0],2)))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse('Not Allowed')
