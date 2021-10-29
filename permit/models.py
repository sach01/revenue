from django.db import models
import datetime
#from django.db.models import F, Sum
from django.db.models.fields import DecimalField
from django.utils.functional import cached_property
from django.db.models import Sum, F, FloatField, Case, When, Count
from django.db.models.functions import TruncMonth
from django.core.validators import RegexValidator
from datetime import date, timedelta, timezone


class SubCounty(models.Model):
    name = models.CharField(max_length=20) #sub_county name
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s'% (self.name)

class Ward(models.Model):
    name = models.CharField(max_length=20) #ward name
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE) #under which sub_county
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s'% (self.name)

class Zone(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE) #under which ward
    name = models.CharField(max_length=20) #zone name eg.kaisut, stage 45
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s'% (self.name)

class Category(models.Model):
    name = models.CharField(max_length=20) #business category name eg.hardware, retail shop
    period = models.PositiveIntegerField()
    price = models.IntegerField()
    #ward = models.ForeignKey(Ward, on_delete=models.CASCADE) #under which ward
    #zone = models.ForeignKey(Ward, on_delete=models.CASCADE) #under which ward
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s'% (self.name)


class Business(models.Model):
    owner = models.CharField(max_length=20)
    shop_no = models.CharField(max_length=20)
    code = models.CharField(max_length=20) #generate unique code for specific business
    id_number = models.CharField(max_length=20)
    #ward = models.ForeignKey(Ward, on_delete=models.CASCADE, default='') #under which ward
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #which category
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE) #which category
    #building = models.CharField(max_length=20)
    created_on = models.DateTimeField(default='')
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s'% (self.owner)

class Payment(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    start = models.DateTimeField(max_length=20) #start date(check_in)
    last_paid = models.DateTimeField(max_length=20) #last date paid
    next_month = models.DateTimeField() #month paid for
    price = models.IntegerField()
    paid_count = models.IntegerField()
    remaining = models.DecimalField(max_digits=17, decimal_places=2, default=0.0)
    pending = models.IntegerField(max_length=20)

    #expired = models.BooleanField(default=False)

    def last_paid(self):
        self.last_paid = Payment.objects.all().order_by('business__shop_no').last()
        if not self.last_paid:
            return self.start
        

    def save(self, *args, **kwargs):
        next_month = Payment.objects.all().order_by('business__shop_no').last()
        if not next_month:
            return self.last_paid 
        self.next_month = self.last_paid.month + 1
        #price = self.business.category.price
        #payment_done = Payment.objects.filter(Business=self).aggregate(Sum('price'))['price__sum'] or DecimalField('0')
        # Remaining Amount of each customer

        #self.remaining = price - payment_done
        super(Payment, self).save(*args, **kwargs)

    @cached_property
    def paid_count(self):
       paid_count = Payment.objects.order_by('date_period')
       paid_count.values('business__shop_no').annotate(Count('id'))
       self.paid_count = paid_count
       return self.paid_count
       
    @cached_property 
    def price(self):
        self.price = self.business.category.price
        return self.price

    @cached_property 
    def start(self):
        start = self.business.created_on
        return start

    @cached_property 
    def pending(self):
        start1 = self.start
        start = start1.replace(day=1)
        end1 = datetime.datetime.now()
        #end1 = self.start
		#fend = datetime.strptime(str(end1), '%d %b %y')
        end = end1.replace(day=1)
        self.pending = (end.year - start.year)*12 + (end.month - start.month)
        return self.pending


    def __str__(self):
        return '%s'% (self.business)

    #@cached_property
def increment_invoice_number():
    last_invoice = Payment.objects.all().order_by('id').last()
    if not last_invoice:
        return 'Rev0001'
    invoice_no = last_invoice.invoice_no
    new_invoice_no = str(int(invoice_no[4:]) + 1)
    new_invoice_no = invoice_no[0:-(len(new_invoice_no))] + new_invoice_no
    return new_invoice_no  

class Invoice(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE) 
    invoice_no = models.CharField(max_length=500, null=True, blank=True, 
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$',
        message='Invoice must be Alphanumeric',code='invalid_invoice number'),], 
        default=increment_invoice_number) #generate unique code for specific invoice
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s'% (self.name)
