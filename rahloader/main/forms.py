from django import forms
from .models import FactorItem, ColleagueFactorItem
 

class SellFactorForm(forms.Form):
    SearchText=forms.CharField(max_length=100, label= "Customer information ",required=False)
    #SearchDate=forms.DateField(label="Date of selling",required=False)


class BuyFactorForm(forms.Form):
    SearchText=forms.CharField(max_length=100, label="Colleague information",required=False)
    #SearchDate=forms.DateField(label="Date of buying",required=False)


class SearchForm(forms.Form):
    SearchText=forms.CharField(max_length=100, label="your item",required=False)


class create_factor_itemForm(forms.ModelForm):
    class Meta:
        model=FactorItem
        fields= [ 'customer_id', 'part_id',  'Code', 'single_price', 'amount', 'total_price' ]
         

class update_factor_itemForm(forms.ModelForm):
    class Meta:
        model=FactorItem
        fields= [ 'customer_id', 'part_id',  'Code', 'single_price', 'amount', 'total_price' ]
         
class create_colleague_factor_itemForm(forms.ModelForm):
    class Meta:
        model=ColleagueFactorItem
        fields= [ 'colleague_id', 'part_id',  'Code', 'single_price', 'amount', 'total_price' ]
         

class update_colleague_factor_itemForm(forms.ModelForm):
    class Meta:
        model=ColleagueFactorItem
        fields= [ 'colleague_id', 'part_id',  'Code', 'single_price', 'amount', 'total_price' ]
         
