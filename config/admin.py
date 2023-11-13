from django.contrib import admin
from Thoth.admin    import final_boss
from .models        import (
  JobPosition,
  CourseType,
  Level,
  Days,
  CourseGroup
  
  )



class JobPosAdminStyle(admin.ModelAdmin):
  
  list_display  = ("job_title",)
  search_fields= ("job_title",)

class CourseTypeAdminStyle(admin.ModelAdmin):
  list_display = ("Name", "description")
  search_fields=  ("Name", "description")




# 
final_boss.register(JobPosition, JobPosAdminStyle)
final_boss.register(CourseType, CourseTypeAdminStyle)
final_boss.register(Level)
final_boss.register(CourseGroup)



