from django.contrib import admin
from .models        import Peaple, Recp, Ticket, Token, Packages

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
  fields             = ("image_tag", "name" )
  search_fields      = ("cost_or_price", "name", "how_much_sold") 
  list_display_links = ("more", ) 
  readonly_fields = ('image_tag',)
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

rinadmin()


admin.site.register(Packages)

