from django.db import models
import datetime
from django.utils.timezone import now
# Create your models here.
from django.contrib import admin
import uuid
import os
print("****"*10)
HOST = os.environ.get("HOST", "http://localhost:8000/")
print(HOST)
print("****"*10)
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
    from django.utils.html import mark_safe
    return mark_safe(f'<img style="width:200px;hieght:200px" src="{HOST}/media/{ self.image}" />' )
  image_tag.short_description = 'Image'
  image_tag.allow_tags = True
  




class Ticket(models.Model):
  
  the_person      = models.ForeignKey("Peaple", on_delete=models.CASCADE)
  name_of_ticket  = models.CharField(max_length=255)
  ticket_price    = models.FloatField()
  he_paid         = models.FloatField(default=0, help_text="How much did he paid from ticket")
  have_debt       = models.BooleanField(default=True)
  time_added      = models.DateTimeField(  default=now, editable=False)
  
  def __str__(self):
    return f"{self.name_of_ticket}|{self.the_person.name}"
  
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

class PeapleAdminStyle(admin.ModelAdmin):
  list_display = ("name", "tickets", "he_debt",  "have_debt" )
  search_fields= ("name",)
  list_filter  = ("have_debt",)
  list_display_links = ("tickets",)
  list_editable= ("name", )
  # actions = ("they_have_debt", )
  
class TicketAdminStyle(admin.ModelAdmin):
  list_display  = ( "name_of_ticket", "the_person", "ticket_price", "he_paid" , "still_have", "have_debt","time_added")
  search_fields = ( "name_of_ticket", "the_person__name", "ticket_price", )
  list_filter   = ( "have_debt",)
  list_display_links = ("time_added",)
  list_editable = ("name_of_ticket", "ticket_price", "he_paid")

class RecpAdminStyle(admin.ModelAdmin):
  list_display       = ("name", "cost_or_price", "how_much_sold","avilable", "more")
  search_fields      = ("cost_or_price", "name", "how_much_sold") 
  list_display_links = ("more", ) 
  list_filter        = ("avilable",)
  list_editable      = ("name", "cost_or_price", "how_much_sold")


def rinadmin():
  x = Packages.objects.first()
  try:
    if x.Peaple:
      admin.site.register(Peaple, PeapleAdminStyle)
    
  except:
    pass
  try:
      
      if not x.Peaple:
        admin.site.unregister(Peaple)
  except:
      pass
  try:
    
    if x.Recption:
      admin.site.register(Recp,   RecpAdminStyle  )
  except:
    pass
  try:
    
    if not x.Recption:
      admin.site.unregister(Recp)
  except:
    pass
  try:
    
    if x.Ticket:
      admin.site.register(Ticket, TicketAdminStyle)
  except: pass
  try:
    if not x.Ticket:
      
      admin.site.unregister(Ticket)
  except:pass
  try:
    
    if x.Token:
      admin.site.register(Token)
  except:
    pass
  try:  
      
    if not x.Token:
      admin.site.unregister(Token)
  except:
    pass


class Packages(models.Model):
  
  Recption = models.BooleanField(default=True)
  Peaple   = models.BooleanField(default=True)
  Ticket   = models.BooleanField(default=True)
  Token    = models.BooleanField(default=True)
  
  def __str__(slef):
    return f"Package manager Don't Touch!!"
  
  def save(self):
    super().save()
    rinadmin()

    super().save()