from django.contrib import admin
from Thoth.admin    import final_boss
from .models        import (
  JobPosition,
  CourseType,
  Level,
  Days,
  CourseGroup,
  CashOut,
  PaymentMethod
  )

days  = Days.objects.all()
a = 0

for i in days:
  a += 1


if a == 7:
  pass
else:
  days  = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
    
          ]
  for i in days:
    b = Days.objects.create(day=i)
    b.save()




class JobPosAdminStyle(admin.ModelAdmin):
  
  list_display  = ("job_title",)
  search_fields= ("job_title",)

class CourseTypeAdminStyle(admin.ModelAdmin):
  list_display = ("Name", "description")
  search_fields=  ("Name", "description")

class CashOutAdminStyle(admin.ModelAdmin):
  list_display = ("Amount", "description", "time_added")


# class MyModelAdmin(admin.ModelAdmin):

    # A template for a very customized change view:
    # change_list_template = 'admin/myapp/extras/sometemplate_change_form.html'

    # def get_total(self):
    #     #functions to calculate whatever you want...
    #     total = YourModel.objects.all().aggregate(tot=Sum('total'))['tot']
    #     return total

    # def changelist_view(self, request, extra_context=None):
    #     my_context = {
    #         'total': self.get_total(),
    #     }
    #     return super(MyModelAdmin, self).changelist_view(request,
    #         extra_context=my_context)

final_boss.register(JobPosition, JobPosAdminStyle)
final_boss.register(CourseType, CourseTypeAdminStyle)
final_boss.register(Level)
final_boss.register(PaymentMethod)
final_boss.register(CourseGroup)
final_boss.register(CashOut, CashOutAdminStyle)




