from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

from django.db import transaction

from .utils import pagination

class HomeView(View):
   
   templates_name = 'index.html'
   
   invoices = Invoice.objects.select_related('customer', 'save_by').all()
   
   context = {
      'invoices': invoices
   }
   
   def get(self, request, *args, **kwargs):
      
      items = pagination(request, self.invoices)
      
      
      self.context['invoices']= items 
      
      return render(request, self.templates_name, self.context)
   
   def post(self, request, *args, **kwargs ):
      
       items = pagination(request, self.invoices)
      
      
       self.context['invoices']= items 
      
       return render(request, self.templates_name, self.context)
      
class AddCustomerView(View):
     
   template_name ='add_customer.html'
   
   def get(self, request, *args, **kwargs):
      return render(request, self.template_name)
   
   @transaction.atomic()
   
   def post(self, request, *args, **kwargs):
      data ={
         'name': request.POST.get('name'),
         'email': request.POST.get('email'),
         'phone': request.POST.get('phone'),
         'address': request.POST.get('address'),
         'sex': request.POST.get('sex'),
         'age': request.POST.get('age'),
         'city': request.POST.get('city'),
         'zip_code': request.POST.get('zip'),
         'save_by': request.user,
      }
      try:
         created = Customer.objects.create(**data)
         
         if created:
            
            messages.success(request,"Customer registered succefully. ")
            
         else:
            
            messages.error(request, "sorry, please try egain")
            
      except Exception as e:
         
         messages.error(request, f"sorry our system is detecteting the followings issues {e}.")
         
      return render(request, self.template_name)
   
class AddInvoiceView(View):
   
   template_name='add_invoice.html'
   
   customers = Customer.objects.select_related('save_by').all()
   
   context ={
      'customers': customers
   }
   
   def get(self, request, *args, **kwargs):
      return render(request, self.template_name, self.context)
   
   def post(self, request, *args, **kwargs):
      
      items = []
      
      try:
         
         customer = request.POST.get('customer')
         type = request.POST.get('invoice_type')
         articles = request.POST.getlist('article')
         
         qties = request.POST.getlist('qty')
         
         units = request.POST.getlist('unit')
         
         total_a = request.POST.getlist('total-a')
         total = request.POST.get('total')
         
         comment = request.POST.get('comment')
         
         invoice_object = {
            'customer_id': customer,
            'save_by': request.user,
            'total': total,
            'invoice_type': type,
            'comments': comment
         }
         
         invoice =Invoice.objects.create(**invoice_object)
         
         for index, article in enumerate(articles):
            data = Article(
               invoice_id = invoice.id,
               name = article,
               quantity= qties[index],
               unit_price = units[index],
               total = total_a[index],
            )
            items.append(data)
         
         created = Article.objects.bulk_create(items)
         
         if created:
            messages.success(request,"Data saved successfully.")
         else:
            messages.error(request,"soory please try again the sent data is incorrect")
         
      except Exception as e:
         messages.error(request, f"sorry the following error has occured {e}.")
         
      
      return render(request, self.template_name, self.context)