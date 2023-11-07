from django.db import models
from phone_field import PhoneField
from django import forms
import datetime
from django.utils.timezone import now
# Create your models here.
from django.contrib import admin
import uuid
import os
from django.utils.html import mark_safe
from config.models import JobPosition

app_label = "Thoth"

# print("****"*10)
HOST = os.environ.get("HOST", "http://192.168.1.62:8000/")
# print(HOST)
# print("****"*10)
class Recp(models.Model):
  
  name          = models.CharField(max_length=255 )
  image         = models.ImageField()
  cost_or_price = models.IntegerField(help_text="Price")
  how_much_sold = models.IntegerField( default=0) 
  avilable      = models.BooleanField(default=True)
  more          = models.CharField(default="More", max_length=255, editable=False)
  def __str__(self):
    
    
    return f"{self.name}"
  def image_tag(self):
    return mark_safe(f'<img style="width:200px;hieght:200px" src="{HOST}/media/{ self.image}" />' )
  image_tag.short_description = 'Image'
  image_tag.allow_tags = True
  class Meta:
        app_label = app_label
        # abstract = True
  




class Ticket(models.Model):
  
  the_person      = models.ForeignKey("Peaple", on_delete=models.CASCADE)
  name_of_ticket  = models.CharField(max_length=255)
  ticket_price    = models.FloatField()
  he_paid         = models.FloatField(default=0, help_text="How much did he paid from ticket")
  have_debt       = models.BooleanField(default=True)
  time_added      = models.DateTimeField(  default=now, editable=False)
  
  def __str__(self):
    return f"{self.name_of_ticket}|{self.the_person.name}"
  class Meta:
        app_label = app_label
        # abstract = True
  def save(self):
    super().save()
    # print("we here")
    # print(self.ticket_price)
    # print(self.he_paid)
    if (self.ticket_price - self.he_paid) == 0:
      # print("it happend")
      self.have_debt = False
      super().save()
      
    else:
      self.have_debt = True
      super().save()
  
  
  def still_have(self):
    
    return self.ticket_price - self.he_paid
  
  
class Peaple(models.Model):
  name = models.CharField(max_length=255)
  have_debt = models.BooleanField(default=False)
  
  def tickets(self):
    person_ticket = Ticket.objects.filter(the_person__name=self.name)
    person_ticket = [x.name_of_ticket for x in person_ticket]
    if len(person_ticket) == 0:
      return "He doesnt have any ticket yet"
    
    return person_ticket
  class Meta:
        app_label = app_label
        # abstract = True
  def is_clear(self):
    person_ticket = Ticket.objects.filter(the_person__name=self.name)
    person_ticket = [x for x in person_ticket]
    if len(person_ticket) == 0:
      return True
    
    succ = []
    for i in person_ticket:
      if i.he_paid == i.ticket_price:
        succ.append(True)
        continue
      succ.append(False)
    
    if False in succ:
      return False
    return True
    
  def he_debt(self):
    person_ticket = Ticket.objects.filter(the_person__name=self.name)
    person_ticket = [x for x in person_ticket]
    result = 0
    for i in person_ticket:
      result += i.still_have()
    return result

  def __str__(self):
    return f"{self.name}"
  
  def they_have_debt(self):
    pass
  
  def save(self):
    super().save()
    person_ticket = Ticket.objects.filter(the_person__name=self.name)
    person_ticket = [x for x in person_ticket]
    result = 0
    for i in person_ticket:
      result += i.still_have()
    if result == 0:
      # print("wtf is this")
      self.have_debt = False

    else:
      self.have_debt = True
      # print("wtf is this Twice")

    super().save()

class Token(models.Model):
  token = models.UUIDField(default=uuid.uuid1, editable=False)

  def __str__(self):
    # print(self.check())
    
    
    return f"{self.token}"

# class PeapleAdminStyle(admin.ModelAdmin):
#   list_display = ("name", "tickets", "he_debt",  "have_debt" )
#   search_fields= ("name",)
#   list_filter  = ("have_debt",)
#   list_display_links = ("tickets",)
#   list_editable= ("name", )
#   # actions = ("they_have_debt", )
  
# class TicketAdminStyle(admin.ModelAdmin):
#   list_display  = ( "name_of_ticket", "the_person", "ticket_price", "he_paid" , "still_have", "have_debt","time_added")
#   search_fields = ( "name_of_ticket", "the_person__name", "ticket_price", )
#   list_filter   = ( "have_debt",)
#   list_display_links = ("time_added",)
#   list_editable = ("name_of_ticket", "ticket_price", "he_paid")

# class RecpAdminStyle(admin.ModelAdmin):
#   list_display       = ("name", "cost_or_price", "how_much_sold","avilable", "more")
#   search_fields      = ("cost_or_price", "name", "how_much_sold") 
#   list_display_links = ("more", ) 
#   list_filter        = ("avilable",)
#   list_editable      = ("name", "cost_or_price", "how_much_sold")


# def rinadmin():
#   x = Packages.objects.first()
#   try:
#     if x.Peaple:
#       admin.site.register(Peaple, PeapleAdminStyle)
    
#   except:
#     pass
#   try:
      
#       if not x.Peaple:
#         admin.site.unregister(Peaple)
#   except:
#       pass
#   try:
    
#     if x.Recption:
#       admin.site.register(Recp,   RecpAdminStyle  )
#   except:
#     pass
#   try:
    
#     if not x.Recption:
#       admin.site.unregister(Recp)
#   except:
#     pass
#   try:
    
#     if x.Ticket:
#       admin.site.register(Ticket, TicketAdminStyle)
#   except: pass
#   try:
#     if not x.Ticket:
      
#       admin.site.unregister(Ticket)
#   except:pass
#   try:
    
#     if x.Token:
#       admin.site.register(Token)
#   except:
#     pass
#   try:  
      
#     if not x.Token:
#       admin.site.unregister(Token)
#   except:
#     pass


# class Packages(models.Model):
  
#   Recption = models.BooleanField(default=True)
#   Peaple   = models.BooleanField(default=True)
#   Ticket   = models.BooleanField(default=True)
#   Token    = models.BooleanField(default=True)
  
#   def __str__(slef):
#     return f"Package manager Don't Touch!!"
  
#   def save(self):
#     super().save()
#     rinadmin()

#     super().save()

class CourseType(models.Model):
  Name = models.CharField(max_length=255)
  description = models.TextField(default="")


  def __str__(self):
    return f"{self.Name}"
  class Meta:
        app_label = app_label
        # abstract = True




class Course(models.Model):
  coursetype = models.ForeignKey(CourseType, on_delete=models.CASCADE)
  start_date = models.DateField(default=datetime.datetime.now)
  end_date   = models.DateField(default=datetime.datetime.now)

  def __str__(self):
    return f"{self.coursetype}|start:{self.start_date}|end:{self.end_date}"
  class Meta:
      app_label = app_label
      # abstract = True

class Client(models.Model):
  
  name    = models.CharField(max_length=255)
  courses = models.ManyToManyField(Course,  blank=True)
  phone_number = models.CharField(max_length=255)
  birth_day    = models.DateField(default=datetime.datetime.now)

  def __str__(self):
    return f"{self.name}"
  class Meta:
        app_label = app_label
        # abstract = True



class Cafe(models.Model):
  class Meta:
        app_label = app_label
        # abstract = True

class Service(models.Model):
  

  class Meta:
          app_label = app_label
          # abstract = True


# Camera type tapo

class vacation(models.Model):
  choices = (
    ("Sick leave", "Sick leave"),
    ("weekends", "weekends"),
    
  )
  Emp           = models.ForeignKey("Employee", on_delete=models.CASCADE)
  vacation_type = models.CharField(choices=choices, max_length=300) 
  class Meta:
        app_label = app_label
        # abstract = True
  

class Employee(models.Model):
  choices = (
    ("Married" , "Married" ),
    ("Single"  , "Single")  ,
    ("Divorced", "Divorced"),
    ("Widower" , "Widower") ,
  )
  name             = models.CharField(max_length=255)
  Person_identf    = models.CharField(max_length=255, default=" ",verbose_name="ID", null=True, blank=True) 
  EDU_state        = models.CharField(max_length=300, default=" ", null=True, blank=True, verbose_name="	Educational Level") 
  address          = models.CharField(max_length=300, default=" ", null=True, blank=True) 
  img              = models.FileField(upload_to="EMP Pic")
  cur_sallary      = models.FloatField(verbose_name="Current Salary") 
  Date_of_join     = models.DateField(default=datetime.datetime.now)
  state_of_marrieg = models.CharField(choices=choices, verbose_name="Person state", max_length=300)
  phone_number     = models.CharField(max_length=20, verbose_name="Phone number", blank=True, null=True)
  phone_number_eme = models.CharField(max_length=20, verbose_name="Emergency phone number", blank=True, null=True)
  job_postition    = models.ForeignKey(JobPosition, null=True, on_delete=models.SET_NULL, blank=True)
  more             = models.CharField(editable=False, default="More",max_length=10)


  def image_tag(self):
    return mark_safe(f'<img style="width:200px;hieght:200px" src="{HOST[:-1]}{ self.img.url}" />' )
  image_tag.short_description = 'Image'
  image_tag.allow_tags = True


  def __str__(self):
    return f"{self.name}"
  class Meta:
        app_label = app_label
        # abstract = True
        
class EmpMarriegForm(forms.ModelForm):
  
  class Meta:
    models = (Employee ,)
    fields = ["state_of_marrieg", "state_of_marrieg"]
    labels = {"state_of_marrieg": "", "state_of_marrieg": "label for public"}