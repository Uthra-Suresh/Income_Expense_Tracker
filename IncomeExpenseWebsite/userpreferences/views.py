from django.shortcuts import render
import os
import json
from django.conf import settings
import pdb
from .models import UserPreference
from django.contrib import messages
# Create your views here.
#pdb.set_trace()

def indexview(request):
    currency_data=[]
    file_path = os.path.join(settings.BASE_DIR,'currencies.json')

    with open(file_path,'r') as json_file:
        data=json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})
    exists =UserPreference.objects.filter(user=request.user).exists()
    user_preference=None 
    if exists:
        user_preference=UserPreference.objects.get(user=request.user)

    if request.method=='GET':
        return render(request,'preferences/index.html',{'currencies':currency_data,'user_preference':user_preference})
    
    else:
        currency=request.POST.get('currency')
        #pdb.set_trace()

        if exists:
            user_preference.currency=currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user,currency=currency)
        messages.success(request,'Changes saved')
        return render(request,'preferences/index.html',{'currencies':currency_data,'user_preference':user_preference})
        