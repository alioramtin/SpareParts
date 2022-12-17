from django.shortcuts import render, redirect
from main.models import Part, FactorItem, Customer, Colleague, ColleagueFactorItem
from django.views import generic
from django.urls import reverse_lazy, reverse
from main.forms import  SearchForm , create_factor_itemForm, create_colleague_factor_itemForm, SellFactorForm, BuyFactorForm
from django import forms
from django.shortcuts import ( render, HttpResponseRedirect, HttpResponse)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)

import os
from itertools import chain
# invoice
from django.forms import inlineformset_factory
from django.utils import translation
from django.utils.translation import gettext  as _ 
from xhtml2pdf import pisa
from django.template.loader import get_template
import datetime





#/////////////////////////////////////////////////
def sell_factor(request):  
    sellFactorForm=SellFactorForm(request.GET)     
    if sellFactorForm.is_valid():
        searchText=sellFactorForm.cleaned_data['SearchText']
        parts=FactorItem.objects.filter( Q(customer_id__Name__contains=searchText)|Q(customer_id__Family__contains=searchText)|Q(customer_id__Code__contains=searchText)|Q(customer_id__Company__contains=searchText))
        context={
        'sellFactorForm': sellFactorForm,
        'parts': parts,
        }
        return render(request, "main/sell_factor.html", context)
    else:
        return render(request, "main/sell_factor.html", {'sellFactorForm': sellFactorForm,})

    
               



#/////////////////////////////////////////////////
def buy_factor(request):  
    buyFactorForm=BuyFactorForm(request.GET)     
    if buyFactorForm.is_valid():
        searchText=buyFactorForm.cleaned_data['SearchText']          
        parts=ColleagueFactorItem.objects.filter(Q(colleague_id__Name__contains=searchText)|Q(colleague_id__Family__contains=searchText)|Q(colleague_id__Code__contains=searchText)|Q(colleague_id__Company__contains=searchText))
        context={
        'buyFactorForm': buyFactorForm,
        'parts': parts,
        }
        return render(request, "main/buy_factor.html", context)
    else:
        context={
        'buyFactorForm': buyFactorForm,
         }
        return render(request, "main/buy_factor.html", context)
    

#/////////////////////////////////////////////////
def test(request):       
    return render(request, "main/test.html", {})
    

        

#/////////////////////////////////////////////////
def error(request):
    return render(request,'main/error.html' ,{})



def Buy_Export_PDF(request):
    response=HttpResponse(content_type="aplication/pdf")
    response["content-Disposition"]=\
        'attachment;filename=buy'+ \
        str(datetime.datetime.now())+'.pdf'
    template_path="main/buyListPDF.html"
    template=get_template(template_path)
    parts=ColleagueFactorItem.objects.all()
    context={"parts":parts}
    html=template.render(context)
    pisa.CreatePDF(html,dest=response)
    return response



def Sell_Export_PDF(request):
    response=HttpResponse(content_type="aplication/pdf")
    response["content-Disposition"]=\
        'attachment;filename=sell'+ \
        str(datetime.datetime.now())+'.pdf'
    template_path="main/sellListPDF.html"
    template=get_template(template_path)
    parts=FactorItem.objects.all()
    context={"parts":parts}
    html=template.render(context)
    pisa.CreatePDF(html,dest=response)
    return response



#/////////////////////////////////////////////////
def partAmountUpdateForCustomers(request,mycode,myamount):
    mypart=Part.objects.filter(Code=mycode)   

    print ("from partUpdate Code is "+ mycode )
    print ("from partitem Amount is ", str(myamount))
    print ("from part Amount is ", mypart)
    print ("###########################################")
    context = {       
        'mycode': mycode,
        'myamount': myamount,
        'mypart': mypart,
   }
    return render(request,'main/test.html' ,context)




# formset for colleagues 
def buyinvoice(request,colleague_id):
    colleague= Colleague.objects.get(pk=colleague_id)
    LanguageFormset= inlineformset_factory(Colleague, ColleagueFactorItem, fields=('part_id','Code','single_price', 'amount', 'total_price' ,'date_factor',), extra=1)
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, instance= colleague)
        if formset.is_valid():
            formset.save()
            return redirect('buyinvoice' ,colleague_id = colleague.id) 

    formset = LanguageFormset(instance= colleague) 
    context= {
        'formset':formset,
        'colleague':colleague,
        
        }
    return render(request,'main/buyinvoice.html' , context ) 
 

# formset for customers 
def invoice(request,customer_id):
    customer= Customer.objects.get(pk=customer_id)
    LanguageFormset= inlineformset_factory(Customer, FactorItem, fields=('part_id','Code','single_price', 'amount', 'total_price' ,'date_factor',), extra=1)
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, instance= customer)
        if formset.is_valid():
            formset.save()
            return redirect('invoice' ,customer_id = customer.id) 

    formset = LanguageFormset(instance= customer) 
    context= {
        'formset':formset,
        'customer':customer,
        
        }
    return render(request,'main/invoice.html' , context ) 
 




#/////////////////////////////////////////////////
def indexView(request):
    return render(request,'main/index.html' ,{})

    

###########################################
# Part
###########################################

def partsView(request):
    searchForm=SearchForm(request.GET)
    if searchForm.is_valid():
        SearchText=searchForm.cleaned_data['SearchText']
        parts=Part.objects.filter(Q(Name__contains=SearchText ) | Q(VehicleName__contains=SearchText ) | Q(Code__contains=SearchText ) | Q(VehicleName__contains=SearchText )| Q(MadeIn__contains=SearchText ) | Q(Place__contains=SearchText )) 
    else:
        parts=Part.objects.all()

    paginator = Paginator(parts,4)
    page=request.GET.get('page',1)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    return render(request, "main/partsView.html", {
        'result':result,
        "searchForm":searchForm,
        })

#/////////////////////////////////////////////////
class PartCreateView(generic.CreateView):
    model=Part
    fields = ['Name', 'VehicleName', 'Code', 'MadeIn','Amount', 'Picture', 'Place']
    success_url:reverse_lazy('partsview')  # name in urls
    def get_success_url(self):
      return reverse('partsview')

#/////////////////////////////////////////////////
class PartUpdateView(generic.UpdateView):
    model=Part
    fields = ['Name', 'VehicleName', 'Code', 'MadeIn','Amount', 'Picture', 'Place']
    success_url:reverse_lazy('partsview')  # name in urls
    def get_success_url(self):
      return reverse('partsview')

#/////////////////////////////////////////////////
class PartDeleteView(generic.DeleteView):
    model=Part
    success_url:reverse_lazy('partsview')  # name in urls
    def get_success_url(self):
      return reverse('partsview')

###########################################
# FactorItem
###########################################

def factoritemview(request):
    searchForm=SearchForm(request.GET)
    if searchForm.is_valid():
        SearchText=searchForm.cleaned_data['SearchText']
        parts=FactorItem.objects.filter(Q(part_id__Name__contains=SearchText)|Q(part_id__VehicleName__contains=SearchText)|Q(part_id__Code__contains=SearchText)|Q(part_id__MadeIn__contains=SearchText)|Q(part_id__Place__contains=SearchText)) 
    else:
        parts=FactorItem.objects.all()

    paginator = Paginator(parts,4)
    page=request.GET.get('page',1)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    return render(request, "main/factoritemview.html", {
        'result':result,
        "searchForm":searchForm,
        })


#/////////////////////////////////////////////////
def create_factor_item(request):
    context = {}
    form = create_factor_itemForm(request.POST, request.FILES or None)
    if form.is_valid():   
        t_code=form.cleaned_data['Code']
        t_amount=form.cleaned_data['amount']  

        part=Part.objects.filter(Q(Code__contains=t_code)).values()
        print(part)
        for p in part:         
            f_amount=p['Amount']
            r_amount= f_amount - t_amount
            if r_amount >= 0:
                part.update(Amount=r_amount)
                form.save()  
            else:
                return HttpResponseRedirect('/error')

        #form.save()  

        return HttpResponseRedirect('/factoritemview')
        
    context['form'] = form
    return render(request, "main/create_factor_item.html", context)

 

#/////////////////////////////////////////////////

def update_factor_item(request, id):
    context = {}
    
    obj = FactorItem.objects.filter(Q(customer_id=id)).first()
    obj_amount=obj.amount
    form = create_factor_itemForm(request.POST or None, instance = obj)
    if form.is_valid():   
        tmp_code=form.cleaned_data['Code']
        tmp_amount=form.cleaned_data['amount']  
        
        part=Part.objects.filter(Q(Code__contains=tmp_code)).values()
        #print(part)       
        
        for p in part:         
            form_amount=p['Amount']  
            if tmp_amount > obj_amount:                
                updated_amount= form_amount - (tmp_amount-obj_amount)
                part.update(Amount=updated_amount)
                form.save()  
            if tmp_amount < obj_amount:                
                updated_amount= form_amount + (obj_amount-tmp_amount)
                part.update(Amount=updated_amount)
                form.save()  
            if tmp_amount == obj_amount: 
                return HttpResponseRedirect('/factoritemview') 

            #else:
                #return HttpResponseRedirect('/error')

        return HttpResponseRedirect('/factoritemview')
        
    context['form'] = form
    return render(request, "main/update_factor_item.html", context)
 

 
""" #/////////////////////////////////////////////////
class FactorItemUpdateView(generic.UpdateView):
    model=FactorItem
    fields = ['customer_id', 'part_id', 'Code', 'single_price', 'amount', 'total_price', 'date_factor']
    success_url:reverse_lazy('factoritemview')  # name in urls
    def get_success_url(self):
      return reverse('factoritemview')
 """
#/////////////////////////////////////////////////
class FactorItemDeleteView(generic.DeleteView):
    model=FactorItem
    success_url:reverse_lazy('factoritemview')  # name in urls
    def get_success_url(self):
      return reverse('factoritemview')
 

###########################################
# Customer
###########################################

def customersView(request):
    searchForm=SearchForm(request.GET)
    if searchForm.is_valid():
        SearchText=searchForm.cleaned_data['SearchText']
        parts=Customer.objects.filter(Q(Name__contains=SearchText ) | Q(Family__contains=SearchText ) | Q(Code__contains=SearchText ) | Q(Company__contains=SearchText )| Q(Address__contains=SearchText ) ) 
    else:
        parts=Customer.objects.all()

    paginator = Paginator(parts,4)
    page=request.GET.get('page',1)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    return render(request, "main/customersView.html", {
        'result':result,
        "searchForm":searchForm,
        })

#/////////////////////////////////////////////////
class CustomerCreateView(generic.CreateView):
    model=Customer
    fields = ['Name', 'Family', 'Company', 'Address', 'Phone','Code']
    success_url:reverse_lazy('customersview')  # name in urls
    def get_success_url(self):
      return reverse('customersview')

#/////////////////////////////////////////////////
class CustomerUpdateView(generic.UpdateView):
    model=Customer
    fields = ['Name', 'Family', 'Company', 'Address', 'Phone','Code']
    success_url:reverse_lazy('customersview')  # name in urls
    def get_success_url(self):
      return reverse('customersview')

#/////////////////////////////////////////////////
class CustomerDeleteView(generic.DeleteView):
    model=Customer
    success_url:reverse_lazy('customersview')  # name in urls
    def get_success_url(self):
      return reverse('customersview')



###########################################
# Colleague  
###########################################

def colleaguesView(request):
    searchForm=SearchForm(request.GET)
    if searchForm.is_valid():
        SearchText=searchForm.cleaned_data['SearchText']
        parts=Colleague.objects.filter(Q(Name__contains=SearchText ) | Q(Family__contains=SearchText ) | Q(Code__contains=SearchText ) | Q(Company__contains=SearchText )| Q(Address__contains=SearchText ) ) 
    else:
        parts=Colleague.objects.all()

    paginator = Paginator(parts,4)
    page=request.GET.get('page',1)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    return render(request, "main/colleaguesView.html", {
        'result':result,
        "searchForm":searchForm,
        })

#/////////////////////////////////////////////////
class ColleagueCreateView(generic.CreateView):
    model=Colleague
    fields = ['Name', 'Family', 'Company', 'Address', 'Phone','Code']
    success_url:reverse_lazy('colleaguesview')  # name in urls
    def get_success_url(self):
      return reverse('colleaguesview')

#/////////////////////////////////////////////////
class ColleagueUpdateView(generic.UpdateView):
    model=Colleague
    fields = ['Name', 'Family', 'Company', 'Address', 'Phone','Code']
    success_url:reverse_lazy('colleaguesview')  # name in urls
    def get_success_url(self):
      return reverse('colleaguesview')


#/////////////////////////////////////////////////
class ColleagueDeleteView(generic.DeleteView):
    model=Colleague
    success_url:reverse_lazy('colleaguesview')  # name in urls
    def get_success_url(self):
      return reverse('colleaguesview')


###########################################
# ColleagueFactorItem
###########################################

def colleaguefactoritemview(request):
    searchForm=SearchForm(request.GET)
    if searchForm.is_valid():
        SearchText=searchForm.cleaned_data['SearchText']
        parts=ColleagueFactorItem.objects.filter(Q(part_id__Name__contains=SearchText)|Q(part_id__VehicleName__contains=SearchText)|Q(part_id__Code__contains=SearchText)|Q(part_id__MadeIn__contains=SearchText)|Q(part_id__Place__contains=SearchText)) 
    else:
        parts=ColleagueFactorItem.objects.all()

    paginator = Paginator(parts,4)
    page=request.GET.get('page',1)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    return render(request, "main/colleaguefactoritemview.html", {
        'result':result,
        "searchForm":searchForm,
        })


#/////////////////////////////////////////////////
def create_colleague_factor_item(request):
    context = {}
    form = create_colleague_factor_itemForm(request.POST, request.FILES or None)
    if form.is_valid():   
        t_code=form.cleaned_data['Code']
        t_amount=form.cleaned_data['amount']  

        part=Part.objects.filter(Q(Code__contains=t_code)).values()
        print(part)
        for p in part:         
            f_amount=p['Amount']
            r_amount= f_amount + t_amount

        part.update(Amount=r_amount)
        form.save()  
        return HttpResponseRedirect('/colleaguefactoritemview')
        
    context['form'] = form
    return render(request, "main/create_colleague_factor_item.html", context)


#/////////////////////////////////////////////////
def update_colleague_factor_item(request, id):
    context = {}
    
    obj = ColleagueFactorItem.objects.filter(Q(colleague_id=id)).first()
    obj_amount=obj.amount
    form = create_colleague_factor_itemForm(request.POST or None, instance = obj)
    if form.is_valid():   
        tmp_code=form.cleaned_data['Code']
        tmp_amount=form.cleaned_data['amount'] 
       
        part=Part.objects.filter(Q(Code__contains=tmp_code)).values()
        for p in part:         
            form_amount=p['Amount']  
            if tmp_amount > obj_amount:                
                updated_amount= form_amount + (tmp_amount-obj_amount)
                print('updated_amount 1= ', updated_amount)   

                part.update(Amount=updated_amount)
                form.save()  
            if tmp_amount < obj_amount:                
                updated_amount= form_amount - (obj_amount-tmp_amount)
                part.update(Amount=updated_amount)
                form.save()  
            if tmp_amount == obj_amount: 
                return HttpResponseRedirect('/colleaguefactoritemview') 

            #else:
                #return HttpResponseRedirect('/error')

        return HttpResponseRedirect('/colleaguefactoritemview')
        
    context['form'] = form
    return render(request, "main/update_colleague_factor_item.html", context)
 

#/////////////////////////////////////////////////
class ColleagueFactorItemDeleteView(generic.DeleteView):
    model=ColleagueFactorItem
    success_url:reverse_lazy('colleaguefactoritemview')  # name in urls
    def get_success_url(self):
      return reverse('colleaguefactoritemview')
 
