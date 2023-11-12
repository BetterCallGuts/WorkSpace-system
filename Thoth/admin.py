from django.contrib                import admin
from django.contrib                import messages
from django.views.decorators.cache import never_cache
from django.utils.html             import mark_safe
from django.contrib.auth.models    import User, Group
from django.contrib.auth.admin     import UserAdmin, GroupAdmin
from django.conf                   import settings
from django.conf.urls.static       import static
from config.models                 import CourseType
from .models                       import (
Coffee,   Token, 
Course,   Client,
Employee, vacation,
Absent,   Deduction, 
Reward,   Instructors,
)


# The Admin site 
# __________________
class WithAlertAdminPage(admin.sites.AdminSite):
    # Dash board html page
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
    if self.value():
        for i in queryset:
          for c in i.courses.all():
            if c.coursetype.Name == self.value():
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
    if self.value():
      # true
        for i in queryset:
          for c in i.courses.all():
            # print(c.Instructor.)
            if c.Instructor.name  == self.value():
              list_that_will_be_returned.append(i.id)
              break
        return queryset.filter(id__in=list_that_will_be_returned)





# Stacked INline
# _______________________________________
class VacationInLine(admin.StackedInline):
  model = vacation

class DeductionInLine(admin.StackedInline):
  model = Deduction

class AbsentInLine(admin.StackedInline):
  model = Absent
  
class RewardInLine(admin.StackedInline):
  model = Reward









# ModelAdmins Custom admin site
# ____________________________-


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
    )
  list_display_links = ("more",)
  list_filter        = ('have_debt', 
        FilterClinetsByCourseType,
        FilterClinetsByIntructors
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
    "name", "phone_number",
    "specialities"
    )
  list_filter  = ("specialty", )
# ________________________
class CourseAdminStyle(admin.ModelAdmin):
  list_display = ("coursetype", "Instructor","start_date", "end_date", "course_levels")
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
  list_display       = ("name", "cost_or_price", "how_much_sold","avilable", "more")
  fields             = ("image_tag", "name", "image", "cost_or_price","how_much_sold", "avilable" )
  search_fields      = ("cost_or_price", "name", "how_much_sold") 
  list_display_links = ("more", ) 
  readonly_fields    = ('image_tag',)
  list_filter        = ("avilable",)
  list_editable      = ("name", "cost_or_price", "how_much_sold")


# Register models

final_boss.register(User, UserAdmin)
final_boss.register(Group, GroupAdmin)
final_boss.register(Client,ClientAdmin)
final_boss.register(Course, CourseAdminStyle)
final_boss.register(Employee, EmpAdmin)
final_boss.register(Instructors, InstructorsAdminStyle)
final_boss.register(Coffee, CoffeeAdminStyle)