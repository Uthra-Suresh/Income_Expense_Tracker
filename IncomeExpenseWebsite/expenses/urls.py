from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.indexview, name ="expenses"),
    path('add-expenses', views.add_expenseview, name="add-expenses"),
    path('edit-expenses/<int:id>', views.edit_expenseview, name="edit-expenses"),
    path('delete-expenses/<int:id>', views.delete_expenseview, name="delete-expenses"),
    path('search-expenses', csrf_exempt(views.search_expenseview), name="search-expenses"),
    path('categorysummary-expenses', csrf_exempt(views.categorysummary_expenseview), name="categorysummary-expenses"),
    path('stats-expenses', csrf_exempt(views.stats_expenseview), name="stats-expenses"),
    path('stats-combined', csrf_exempt(views.stats_combinedview), name="stats-combined"),
    path('monthsummary-expenses', csrf_exempt(views.monthsummary_expenseview), name="monthsummary-expenses"),
    path('exportcsv-expenses', csrf_exempt(views.exportcsv_expenseview), name="exportcsv-expenses"),
    path('exportexcel-expenses', csrf_exempt(views.exportexcel_expenseview), name="exportexcel-expenses"),
    
]
