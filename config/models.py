from django.db import models

# Create your models here.


class JobPosition(models.Model):
  
  job_title =  models.CharField(max_length=300)
  
  
  def __str__(self):
    
    return f"{self.job_title}"
  
class CourseType(models.Model):
  Name = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.Name}"
  


class Level(models.Model):
  Level = models.CharField(max_length=255)
  
  def __str__(self):
    
    return f"{self.Level}"
  

class Days(models.Model):
  
  day = models.CharField(max_length=255, verbose_name="Day Name")
  
  def __str__(self):
    return f"{self.day}"

class CourseGroup(models.Model):
  name = models.CharField(max_length=255)
  
  
  def __str__(self):
    
    return f"{self.name}"
