from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
from userpreferences.models import UserPreference
import datetime
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import csv
import xlwt
# Create your views here.
@login_required(login_url='/authentication/login')
def indexview(request):
    sources = Source.objects.all()
    incomes = Income.objects.filter(owner=request.user)

    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency=UserPreference.objects.get(user=request.user).currency
    except:
        currency = "(No currency saved)"
    context = {
        'incomes':incomes,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'incomes/index.html',context)


def add_incomeview(request):
    sources = Source.objects.all()
    context={'sources':sources,
             'values'    : request.POST
    }
    if request.method == 'GET':
        return render(request,'incomes/add_income.html',context)
        
    if request.method == 'POST':
        amount=request.POST['amount']
        description=request.POST['description']
        date=request.POST['income_date']
        source=request.POST['source']
        

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'incomes/add_income.html',context)

        if not description:
            messages.error(request,'Description is required')
            return render(request,'incomes/add_income.html',context)

        Income.objects.create(amount=amount,owner=request.user,date=date,source=source,description=description)
        messages.success(request,"Income saved sucessfully")

        return redirect('incomes')

def edit_incomeview(request,id):
    income = Income.objects.get(pk=id)
    categories = Source.objects.all()
    context={'income':income,
            'values':income,
            'categories':categories}

    if request.method == "GET":
        return render(request,'incomes/edit_income.html',context)
    
    if request.method == "POST":
        amount=request.POST['amount']
        description=request.POST['description']
        date=request.POST['income_date']
        source=request.POST['source']
        

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'incomes/edit_income.html',context)

        if not description:
            messages.error(request,'Description is required')
            return render(request,'incomes/edit_income.html',context)

        income.amount=amount
        income.owner=request.user
        income.date=date
        income.source=source
        income.description=description
        income.save()
        messages.success(request,"Income updated sucessfully")

        return redirect('incomes')


def delete_incomeview(request,id):
    income=Income.objects.get(pk=id)
    income.delete()
    messages.success(request,"Income deleted sucessfully")
    return redirect('incomes')


def search_incomeview(request):
    if request.method == 'POST':
        
        search_str = json.loads(request.body).get('searchText')
        
        incomes = Income.objects.filter(
                    amount__istartswith=search_str,owner=request.user) | Income.objects.filter(
                    date__istartswith=search_str,owner=request.user) | Income.objects.filter(
                    description__icontains=search_str,owner=request.user) | Income.objects.filter(
                    source__istartswith=search_str,owner=request.user)

        data = incomes.values()
        return JsonResponse(list(data),safe=False)


def sourcesummary_incomeview(request):
     if request.method == 'POST':
         
        days = int(json.loads(request.body).get('timelimit'))
        
        todays_date = datetime.date.today()
        from_days = todays_date-datetime.timedelta(days=days)
        incomes = Income.objects.filter(owner=request.user,date__gte=from_days,date__lte=todays_date)
        source_list=incomes.values('source').annotate(Sum('amount'))
        finalrep={}

        for x in source_list:
            finalrep[x['source']]=x['amount__sum']

        return JsonResponse({'income_source_data':finalrep},safe=False)

def monthsummary_incomeview(request):
    incomes = Income.objects.filter(owner=request.user).annotate(month=TruncMonth('date')).values('month').annotate(sum=Sum('amount')).values('month','sum')
    finalrep={}
    
    for x in incomes:
        month = str(x['month'])
        finalrep[month]=x['sum']
    
    return JsonResponse({'income_month_data':finalrep},safe=False)



def stats_incomeview(request):

    return render(request,'incomes/stats_income.html')
   
def exportcsv_incomeview(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Incomes'+ \
        str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Source','Date'])
    incomes=Income.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount,income.description,income.source,income.date])

    return response

def exportexcel_incomeview(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Incomes'+ \
        str(datetime.datetime.now())+'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Incomes')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Description','Source','Date']   
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num], font_style)     
    
    font_style = xlwt.XFStyle()

    rows = Income.objects.filter(owner=request.user).values_list('amount','description','source','date')
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]), font_style)
        wb.save(response)   

    return response
