from django.contrib import admin
from Thoth.admin    import final_boss
from .models        import JobPosition



class JobPosAdminStyle(admin.ModelAdmin):
  
  list_display  = ("job_title",)
  search_fields= ("job_title",)
  

final_boss.register(JobPosition, JobPosAdminStyle)

# Register your models here.



