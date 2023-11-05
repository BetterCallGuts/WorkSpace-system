from django.contrib import admin
from .models        import Peaple, Recp, Ticket, Token
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.html import mark_safe






class WithAlertAdminPage(admin.sites.AdminSite):


    def main(self):
      pple = Peaple.objects.all()
      tickets =  Ticket.objects.all()
      total = 0
      for i in pple:
        if i.is_clear():
          # print("he is clear")
          pass
        else:
          # print("h")
          total += 1
      
      return tickets, total
    @never_cache
    def index(self, request, extra_context=None):

        # print(mark_safe("yoo"))
        # print('__')
        # print(mark_safe("<p> yooo</p>"))
        tickets, total = self.main()
        if total == 0:
          
          messages.add_message(request, messages.SUCCESS,mark_safe( f'You have no debtor !!, check out your finished {len(tickets)} tickets <a href="/api/ticket/"> here </a>'))
          return super().index(request, extra_context)

        # 
        messages.add_message(request, messages.WARNING, mark_safe( f'There is {total} people with debt <a href="/api/peaple/?have_debt__exact=1" > check them </a> out, And {len(tickets)} Tikets Click <a href="/api/ticket/">here to see them</a>'))
        return super().index(request, extra_context)
          # print(i.is_clear())

          

final_boss = WithAlertAdminPage()








# def printhello(modeladmin, req, selected):

  # # print("Hello world")
  # for i in selected:
  #   print(i.name)  
  
# admin.site.index_template = "my_index.html"
# class CustomAdminSite(admin.):
#     @never_cache
#     def index(self, request, extra_context=None):
#         messages.add_message(request, messages.INFO, 'This is a message.')
#         return super().index(request, extra_context)
  


# admin_site = CustomAdminSite(name='myadmin')

class InLineTicket(admin.StackedInline):
  model = Ticket
  
  


class PeapleAdminStyle(admin.ModelAdmin):
  inlines      = (InLineTicket,)
  list_display = ("name", "tickets", "he_debt",  "have_debt" )
  search_fields= ("name",)
  list_filter  = ("have_debt",)
  list_display_links = ("tickets",)
  list_editable= ("name", )
  # actions = ("they_have_debt", )
  # def save_model(self, request, obj, form, change):
        
  #       messages.add_message(request, messages.INFO, 'Car has been sold')
  #       super(PeapleAdminStyle, self).save_model(request, obj, form, change)
  
class TicketAdminStyle(admin.ModelAdmin):
  # inlines            = (InLinePeaple, )
  list_display       = ( "name_of_ticket", "the_person", "ticket_price", "he_paid" , "still_have", "have_debt","time_added")
  search_fields      = ( "name_of_ticket", "the_person__name", "ticket_price", )
  list_filter        = ( "have_debt",)
  list_display_links = ("time_added",)
  list_editable      = ("name_of_ticket", "ticket_price", "he_paid")



class RecpAdminStyle(admin.ModelAdmin):
  # inlines            = (InLineRecp,)
  list_display       = ("name", "cost_or_price", "how_much_sold","avilable", "more")
  fields             = ("image_tag", "name", "image", "cost_or_price","how_much_sold", "avilable" )
  search_fields      = ("cost_or_price", "name", "how_much_sold") 
  list_display_links = ("more", ) 
  readonly_fields    = ('image_tag',)
  list_filter        = ("avilable",)
  list_editable      = ("name", "cost_or_price", "how_much_sold")
  

  # actions =[printhello] #i commented the function


# def rinadmin():
#   x = Packages.objects.first()
#   try:
#     if x.Peaple:
#       final_boss.register(Peaple, PeapleAdminStyle)
    
#   except:
#     pass
#   try:
      
#       if not x.Peaple:
#         final_boss.unregister(Peaple)
#   except:
#       pass
#   try:
    
#     if x.Recption:
#       final_boss.register(Recp,   RecpAdminStyle  )
#   except:
#     pass
#   try:
    
#     if not x.Recption:
#       final_boss.unregister(Recp)
#   except:
#     pass
#   try:
    
#     if x.Ticket:
#       final_boss.register(Ticket, TicketAdminStyle)
#   except: pass
#   try:
#     if not x.Ticket:
      
#       final_boss.unregister(Ticket)
#   except:pass
#   try:
    
#     if x.Token:
#       final_boss.register(Token)
#   except:
#     pass
#   try:  
      
#     if not x.Token:
#       final_boss.unregister(Token)
#   except:
#     pass

# rinadmin()


# final_boss.register(Packages)


final_boss.register(Peaple, PeapleAdminStyle)
final_boss.register(Recp,  RecpAdminStyle)
final_boss.register(Ticket, TicketAdminStyle)