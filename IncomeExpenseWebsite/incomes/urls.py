from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.indexview, name ="incomes"),
    path('add-incomes', views.add_incomeview, name="add-incomes"),
    path('edit-incomes/<int:id>', views.edit_incomeview, name="edit-incomes"),
    path('delete-incomes/<int:id>', views.delete_incomeview, name="delete-incomes"),
    path('search-incomes', csrf_exempt(views.search_incomeview), name="search-incomes"),
    path('sourcesummary-incomes', csrf_exempt(views.sourcesummary_incomeview), name="sourcesummary-incomes"),
    path('stats-incomes', csrf_exempt(views.stats_incomeview), name="stats-incomes"),
    path('monthsummary-incomes', csrf_exempt(views.monthsummary_incomeview), name="monthsummary-incomes"),
     path('exportcsv-incomes', csrf_exempt(views.exportcsv_incomeview), name="exportcsv-incomes"),
    path('exportexcel-incomes', csrf_exempt(views.exportexcel_incomeview), name="exportexcel-incomes"), 
]