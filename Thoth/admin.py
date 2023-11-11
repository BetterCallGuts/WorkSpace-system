from django.contrib import admin
from .models        import ( Recp,
 Token, Course, 
Client, Cafe, Employee, vacation,
Absent, Deduction,Reward,
 Instructors

)
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.html import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.conf import settings
from django.conf.urls.static import static
from config.models import CourseType

class FilterClinetsByCourseType(admin.SimpleListFilter):
  title = ('Course type')
  parameter_name = 'course_type'
  def lookups(self, request, model_admin):
    i = CourseType.objects.all()
    x = ( (s.Name, f"{s.Name}")  for s in i )
    
    return x
  
  def queryset(self, request, queryset):
    list_that_will_be_returned = []
    if self.value():
      # true
        for i in queryset:
          for c in i.courses.all():
            if c.coursetype.Name == self.value():
              list_that_will_be_returned.append(i.id)
              break
        return queryset.filter(id__in=list_that_will_be_returned)
    

class FilterClinetsByIntructors(admin.SimpleListFilter):
  title = ('instructor')
  parameter_name = 'instructor'

  def lookups(self, request, model_admin):
    i = Instructors.objects.all()
    x = ( (s.name, f"{s.name}")  for s in i )
    
    return x


  def queryset(self, request, queryset):
    list_that_will_be_returned = []


    if self.value():
      # true
        for i in queryset:
          for c in i.courses.all():
            # print(c.Instructor.)
            if c.Instructor.name  == self.value():
              list_that_will_be_returned.append(i.id)
              break
            
        return queryset.filter(id__in=list_that_will_be_returned)
    
# class CoursesInLine(admin.StackedInline):
#   model = Client.courses.through
  # fields = ("Client__courses__coursetype", )
  # fields = (Client.courses.field.name,)
class VacationInLine(admin.StackedInline):
  model = vacation
  # fields = ("Client__courses__coursetype", )
  # fields = (Client.courses.field.name,)

class DeductionInLine(admin.StackedInline):
  model = Deduction

class AbsentInLine(admin.StackedInline):
  model = Absent
  
class RewardInLine(admin.StackedInline):
  model = Reward
  
# class LevelsInLine(admin.StackedInline):
#   model = Level
# class StillHaveToPay(admin.SimpleListFilter):
#   title = ('Have debt?')
#   parameter_name = 'decade'

#   def lookups(self, request, model_admin):
    
#     return (
#         (True, ('Yes')),
#         (False, ('No')),
#     )
#   def queryset(self, request, queryset):
#     list_that_will_be_returned = []
#     if self.value():
#       # true
#         for i in queryset:
#           if i.still_have_to_pay == "He is Clear":
#             pass
#           else:
#             list_that_will_be_returned.append(i)
#         return list_that_will_be_returned
#     if not self.value() :
#       # false
#         for i in queryset:
#           if i.still_have_to_pay == "He is Clear":
#             list_that_will_be_returned.append(i)
#           else:
#             pass
#         return list_that_will_be_returned

class ClientAdmin(admin.ModelAdmin):
  fields       = ("name", "phone_number",
      "birth_day", "courses",
      "total", "paid", "still_have_to_pay"
      )
  readonly_fields = ("total", "still_have_to_pay" )
  search_fields = ( "name", "phone_number" )
  list_display = (
    "more",
    "name", "phone_number", 
    "birth_day",
    "total",
    "paid",
    "still_have_to_pay",
    "courses_in"
    )
  list_editable = (
    "name",
    "phone_number",
    "paid",
    # "courses_in"
    )
  list_display_links = ("more",)
  list_filter        = ('have_debt', 
        FilterClinetsByCourseType,
        FilterClinetsByIntructors


        )
  # list_editable = 

class EmpAdmin(admin.ModelAdmin):
  inlines  = (
    VacationInLine,
    AbsentInLine,  
    DeductionInLine,
    RewardInLine
    )
  fields = ("image_tag", 
            "img", "name", 
            "Person_identf", 
            "EDU_state", "address", 
            "cur_sallary", "state_of_marrieg"
            ,"Date_of_join" , "phone_number",
            "phone_number_eme",
            "job_postition"
            )
  list_display = (
    "more",
    "name",
    "EDU_state",
    "cur_sallary",
    "state_of_marrieg",
    "Date_of_join",
    "phone_number",
    "job_postition",
    
    )
  list_editable = (
    
        "name", 
        "EDU_state", "cur_sallary",
        "state_of_marrieg", "phone_number",
        "job_postition","Date_of_join",
        
        )
  # list_editable = ("more",)
  list_display_links = ("more",)
  list_filter = ("state_of_marrieg", )
  search_fields = ("name", "cur_sallary")
  readonly_fields    = ('image_tag',)

class InstructorsAdminStyle(admin.ModelAdmin):
  
  list_display = ("name", "phone_number","specialities")
  list_filter  = ("specialty", )



class CourseAdminStyle(admin.ModelAdmin):
  list_display = ("coursetype", "Instructor","start_date", "end_date", "course_levels")
  # inlines      = (CoursesInLine, )

class WithAlertAdminPage(admin.sites.AdminSite):


    # def main(self):
    #   pple = Peaple.objects.all()
    #   tickets =  Ticket.objects.all()
    #   total = 0
    #   for i in pple:
    #     if i.is_clear():
    #       # print("he is clear")
    #       pass
    #     else:
    #       # print("h")
    #       total += 1
      
    #   return tickets, total

      # def get_urls(self):
        
      #   urlpatterns = self.super().get_urls()
      #   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

      #   return urlpatterns

    @never_cache
    def index(self, request, extra_context=None):

        students =  Client.objects.all()
        ppl_with_debt = []

        for i in students:
          if i.still_have_to_pay() == "He is Clear":
            continue
          ppl_with_debt.append(i)
        
        if len(ppl_with_debt) ==0:
          pass
        else:
          messages.add_message(request,
                messages.WARNING  ,
                mark_safe(f"You have {len(ppl_with_debt)} clients with debt <a href='Thoth/client/?have_debt__exact=1'>click here</a> to see them")
                )

        # if total == 0:
          
        #   messages.add_message(request, messages.SUCCESS,mark_safe( f'You have no debtor !!, check out your finished {len(tickets)} tickets <a href="/api/ticket/"> here </a>'))
        #   return super().index(request, extra_context)

        # # 
        # messages.add_message(request, messages.WARNING, mark_safe( f'There is {total} people with debt <a href="/api/peaple/?have_debt__exact=1" > check them </a> out, And {len(tickets)} Tikets Click <a href="/api/ticket/">here to see them</a>'))
        # x = Employee.objects.all()
        # for i in x:
        #   # print(i.img.url)
        #   pass
        return super(WithAlertAdminPage, self).index(request, extra_context,)
          # print(i.is_clear())


final_boss = WithAlertAdminPage()
# final_boss.urls
final_boss.register(User, UserAdmin)
final_boss.register(Group, GroupAdmin)
final_boss.register(Client,ClientAdmin)
final_boss.register(Course, CourseAdminStyle)
# final_boss.register(CourseType)
final_boss.register(Employee, EmpAdmin)
# final_boss.register(Level)
final_boss.register(Instructors, InstructorsAdminStyle)
# final_boss.site_title = "Thoth"
# final_boss.site_header = "Thoth"
# final_boss.index_title = "Dash Board"







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

# class InLineTicket(admin.StackedInline):
#   model = Ticket
  
  


class PeapleAdminStyle(admin.ModelAdmin):
  # inlines      = (InLineTicket,)
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


# final_boss.register(Peaple, PeapleAdminStyle)
# final_boss.register(Recp,  RecpAdminStyle)
# final_boss.register(Ticket, TicketAdminStyle)
final_boss.register(Recp, RecpAdminStyle)