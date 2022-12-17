from email.policy import default
from typing import Concatenate
from django.db import models
from django.utils import timezone 
from django.utils.translation import gettext_lazy as _ 


class Part (models.Model):
  
    class Meta:
        verbose_name=_('Part') 
        verbose_name_plural= _("Parts") 

    Name=models.CharField(max_length=100, verbose_name= _("name") )
    VehicleName=models.CharField(max_length=100,default="-", verbose_name= _("model") )
    Code=models.CharField(max_length=100,  verbose_name= _("part code") )
    MadeIn=models.CharField(max_length=100, default="unknown",verbose_name= _("country") )
    Amount=models.PositiveBigIntegerField(verbose_name= _("amount") )
    Picture=models.ImageField(upload_to="partImages/", default="c.jpg", verbose_name= _("image") )
    Place=models.CharField(max_length=100, default="A1", verbose_name=_("store"))
    
    def __str__(self):
        return " name  : {} - model: {} - part code: {} - country:{}  - amount: {}  - store:{}".format(self.Name,self.VehicleName,self.Code,self.MadeIn, self.Amount, self.Place)



class FactorItem(models.Model):
    class Meta:
        verbose_name=_("FactorItem")
        verbose_name_plural=_("FactorItems")

    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name=_("customer info"))
    part_id = models.ForeignKey('Part', on_delete=models.CASCADE, verbose_name=_("name"))
    Code=models.CharField(max_length=100, default="unknown", verbose_name=_("part code"))
    single_price = models.PositiveBigIntegerField(default=0 , verbose_name=_("single price"))
    amount = models.PositiveIntegerField(default=0 , verbose_name=_("amount") )
    total_price = models.PositiveBigIntegerField(default=0 , verbose_name=_("total price"))
    date_factor = models.DateField(default=timezone.now, verbose_name=_("date")) 

    def __str__(self):
        return "  customers info = {}  -  name = {}  - part code  : {}-  single price : {}- amount: {} -  total price :{}- date :{} ".format(self.customer_id.Company, self.part_id.Code,self.Code, self.single_price,self.amount,self.total_price, self.date_factor)


class Customer (models.Model):
    class Meta:
        verbose_name=_("Customer")
        verbose_name_plural=_("Customers")

    Name=models.CharField(max_length=100, verbose_name=_("name"))
    Family=models.CharField(max_length=100, verbose_name=_("family"))
    Company=models.CharField(max_length=100, default="-", verbose_name=_("company"))
    Address=models.CharField(max_length=500, default="-",verbose_name=_("address"))
    Phone=models.CharField(max_length=100, default="-",verbose_name=_("phone"))
    Code=models.CharField(max_length=100, verbose_name=_("customer code"))
      
    def __str__(self):
        return "  name: {}   -  family: {}-  company: {} -  address: {}   -  phone: {}- customer code: {}".format(self.Name, self.Family, self.Company,self.Address, self.Phone, self.Code)


class Colleague (models.Model):
    class Meta:
        verbose_name=_("Colleague")
        verbose_name_plural=_("Colleagues")

    Name=models.CharField(max_length=100, verbose_name=_("name"))
    Family=models.CharField(max_length=100, verbose_name=_("family"))
    Company=models.CharField(max_length=100, default="-", verbose_name=_("company"))
    Address=models.CharField(max_length=500, default="-",verbose_name=_("address"))
    Phone=models.CharField(max_length=100, default="-",verbose_name=_("phone"))
    Code=models.CharField(max_length=100, verbose_name=_("colleague code"))
      
    def __str__(self):
        return "  name: {}   -  family: {}-  company: {} -  address: {}   -  phone: {}- colleague code: {}".format(self.Name, self.Family, self.Company,self.Address, self.Phone, self.Code)


class ColleagueFactorItem(models.Model):
    class Meta:
        verbose_name=_("ColleagueFactorItem")
        verbose_name_plural=_("ColleagueFactorItems")

    colleague_id = models.ForeignKey('Colleague', on_delete=models.CASCADE, verbose_name=_("colleague info") )
    part_id = models.ForeignKey('Part', on_delete=models.CASCADE, verbose_name=_("part info") )
    Code=models.CharField(max_length=100, default="unknown", verbose_name=_("part code"))
    single_price = models.PositiveBigIntegerField(default=0 , verbose_name=_("single price"))
    amount = models.PositiveIntegerField(default=0 , verbose_name=_("amount") )
    total_price = models.PositiveBigIntegerField(default=0 , verbose_name=_("total price") )
    date_factor = models.DateField(default=timezone.now, verbose_name=_("date") ) 

    def __str__(self):
        return "   company info= {}  -part info  = {}  -  part code: {}- single price : {}-  amount: {} - total price:{}- date:{} ".format(self.colleague_id.Company, self.part_id.Code,self.Code, self.single_price,self.amount,self.total_price, self.date_factor)
