from django.db import models

# Create your models here.


class JobPosition(models.Model):
  
  job_title =  models.CharField(max_length=300)
  
  
  def __str__(self):
    
    return f"{self.job_title}"
  
  