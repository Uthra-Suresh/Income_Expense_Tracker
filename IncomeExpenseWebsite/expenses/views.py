from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
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
@login_required(login_url='/authentication/home')
def indexview(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency=UserPreference.objects.get(user=request.user).currency
    except:
        currency = "(No currency saved)"
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'expenses/index.html',context)


def add_expenseview(request):
    categories = Category.objects.all()
    context={'categories':categories,
             'values'    : request.POST
    }
    if request.method == 'GET':
        return render(request,'expenses/add_expense.html',context)
        
    if request.method == 'POST':
        amount=request.POST['amount']
        description=request.POST['description']
        date=request.POST['expense_date']
        category=request.POST['category']
        

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/add_expense.html',context)

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/add_expense.html',context)

        Expense.objects.create(amount=amount,owner=request.user,date=date,category=category,description=description)
        messages.success(request,"Expense saved sucessfully")

        return redirect('expenses')


def edit_expenseview(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context={'expense':expense,
            'values':expense,
            'categories':categories}

    if request.method == "GET":
        return render(request,'expenses/edit_expense.html',context)
    
    if request.method == "POST":
        amount=request.POST['amount']
        description=request.POST['description']
        date=request.POST['expense_date']
        category=request.POST['category']
        

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/edit_expense.html',context)

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/edit_expense.html',context)

        expense.amount=amount
        expense.owner=request.user
        expense.date=date
        expense.category=category
        expense.description=description
        expense.save()
        messages.success(request,"Expense updated sucessfully")

        return redirect('expenses')


def delete_expenseview(request,id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,"Expense deleted sucessfully")
    return redirect('expenses')


def search_expenseview(request):
    if request.method == 'POST':
        
        search_str = json.loads(request.body).get('searchText')
        
        expenses = Expense.objects.filter(
                    amount__istartswith=search_str,owner=request.user) | Expense.objects.filter(
                    date__istartswith=search_str,owner=request.user) | Expense.objects.filter(
                    description__icontains=search_str,owner=request.user) | Expense.objects.filter(
                    category__istartswith=search_str,owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data),safe=False)
    


def categorysummary_expenseview(request):
    if request.method == 'POST':


        days = int(json.loads(request.body).get('timelimit'))

        todays_date = datetime.date.today()
        from_days = todays_date-datetime.timedelta(days=days)
        expenses = Expense.objects.filter(owner=request.user,date__gte=from_days,date__lte=todays_date)
        category_list=expenses.values('category').annotate(Sum('amount'))
        
        finalrep={}
        

        for x in category_list:
            finalrep[x['category']]=x['amount__sum']
        
        return JsonResponse({'expense_category_data':finalrep},safe=False)

def monthsummary_expenseview(request):
    expenses = Expense.objects.filter(owner=request.user).annotate(month=TruncMonth('date')).values('month').annotate(sum=Sum('amount')).values('month','sum')
    finalrep={}
    
    for x in expenses:
        month = str(x['month'])
        finalrep[month]=x['sum']
    
    return JsonResponse({'expense_month_data':finalrep},safe=False)

def exportcsv_expenseview(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses'+ \
        str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses=Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])

    return response

def exportexcel_expenseview(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Expenses'+ \
        str(datetime.datetime.now())+'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Expenses')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Description','Category','Date']   
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num], font_style)     
    
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]), font_style)
        wb.save(response)   

    return response


def stats_expenseview(request):

    return render(request,'expenses/stats_expense.html')

def stats_combinedview(request):

    return render(request,'expenses/stats_combined.html')


    


    