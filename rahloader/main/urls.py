from django.urls import path 
from main  import views


urlpatterns = [
    path('<customer_id>/invoice',views.invoice, name="invoice"),
    path('<colleague_id>/buyinvoice',views.buyinvoice, name="buyinvoice"),
    path('',views.indexView, name="index" ), 
    path('test',views.test, name="test" ), 
    path('error',views.error, name="error" ), 
    path('sell_export_PDF',views.Sell_Export_PDF , name="Sell_Export_PDF" ), 
    path('buy_export_PDF',views.Buy_Export_PDF , name="Buy_Export_PDF" ), 
    path('sell_factor',views.sell_factor , name="sell_factor" ), 
    path('buy_factor',views.buy_factor , name="buy_factor" ), 


    path('partsview',views.partsView , name="partsview" ), 
    path('createpart',views.PartCreateView.as_view(), name="createpart" ), 
    path('updatepart/<pk>/update',views.PartUpdateView.as_view(), name="updatepart" ), 
    path('deletepart/<pk>/delete',views.PartDeleteView.as_view(), name="deletepart" ), 

    path('customersview',views.customersView , name="customersview" ), 
    path('createcustomer/',views.CustomerCreateView.as_view(), name="createcustomer" ), 
    path('updatecustomer/<pk>/update',views.CustomerUpdateView.as_view(), name="updatecustomer" ), 
    path('deletecustomer/<pk>/delete',views.CustomerDeleteView.as_view(), name="deletecustomer" ), 

    path('colleaguesview',views.colleaguesView , name="colleaguesview" ), 
    path('createcolleague/',views.ColleagueCreateView.as_view(), name="createcolleague" ), 
    path('updatecolleague/<pk>/update',views.ColleagueUpdateView.as_view(), name="updatecolleague" ), 
    path('deletecolleague/<pk>/delete',views.ColleagueDeleteView.as_view(), name="deletecolleague" ), 

    path('factoritemview',views.factoritemview , name="factoritemview" ), 
    path('create_factor_item/',views.create_factor_item, name="create_factor_item" ), 
    path('update_factor_item/<id>/update',views.update_factor_item, name="update_factor_item" ), 
    path('deletefactoritem/<pk>/delete',views.FactorItemDeleteView.as_view(), name="deletefactoritem" ), 

    path('colleaguefactoritemview',views.colleaguefactoritemview , name="colleaguefactoritemview" ), 
    path('create_colleague_factor_item/',views.create_colleague_factor_item, name="create_colleague_factor_item" ), 
    path('update_colleague_factor_item/<id>/update',views.update_colleague_factor_item, name="update_colleague_factor_item" ), 
    path('deletecolleaguefactoritem/<pk>/delete',views.ColleagueFactorItemDeleteView.as_view(), name="deletecolleaguefactoritem" ), 

]
  