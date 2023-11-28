from django.db   import           models
from django      import           forms
import                            datetime
from django.utils.timezone import now
from django.contrib import        admin
import                            uuid
import                            os
from django.utils.html import     mark_safe
from config.models import         JobPosition, PaymentMethod
from django.urls import reverse

# GLobal Vars
app_label = "Thoth"
HOST = os.environ.get("HOST", "http://127.0.0.1:8000/")

# Models
# ________________________
class Token(models.Model):
  # 
  token = models.UUIDField(default=uuid.uuid1, editable=False)
  # 
  def __str__(self):
    return f"{self.token}"

class Coffee(models.Model):
  # 
  ch_clients = (
    ("0", "Client"),
    ("1", "Stuff"),
  )
  name          = models.CharField(max_length=255 )
  image         = models.ImageField(blank=True)
  cost_or_price = models.IntegerField(help_text="Price")
  how_much_sold = models.IntegerField( default=0) 
  avilable      = models.BooleanField(default=True)
  To_who        = models.CharField(max_length=1, choices=ch_clients, verbose_name="The consumer?", default="0")
  more          = models.CharField(default="More", max_length=255, editable=False)
  # 
  def __str__(self):
    return f"{self.name}"
  # 
  def image_tag(self):
    return mark_safe(f'<img style="width:200px;hieght:200px" src="{HOST}/media/{ self.image}" />' )
  image_tag.short_description = 'Image'
  image_tag.allow_tags = True
  # 
  class Meta:
        app_label = app_label





class Course(models.Model):
  # 
  coursetype  = models.ForeignKey("config.CourseType", on_delete=models.CASCADE)
  start_date  = models.DateField(default=datetime.datetime.now)
  levels      = models.ManyToManyField("config.Level", related_name="levels", blank=True)
  Instructor  = models.ForeignKey("Instructors", on_delete=models.CASCADE, null=True, blank=True)
  end_date    = models.DateField(default=datetime.datetime.now)
  cost_forone = models.FloatField(blank=True, default=0, verbose_name="Course cost per person")
  Day_per_week= models.ManyToManyField("config.Days", related_name="Days", blank=True)
  Voucher     = models.FloatField( blank=True, default=0, verbose_name="Depreciation")
  per_for_inst= models.FloatField(

    default=0,
    verbose_name="percentage for instructor",
    )
  groups      = models.ManyToManyField("config.CourseGroup", related_name="Group", blank=True)
  # 
  
  def save(self):
    super().save()
    if self.Voucher == None:
      self.Voucher = 0
    if self.cost_forone == None:
      self.cost_forone = 0
    super().save()
  
  def __str__(self):
    return f"{self.coursetype}|start:{self.start_date}|end:{self.end_date}"
  # 
  class Meta:
      app_label = app_label
  # 
  def course_levels(self):
    levels_many_to_many = self.levels.all()
    return ", ".join([x.Level for x in levels_many_to_many])
  # 
  def income(self):
    pple  = float(self.clients_in_course())
    pple_in_course = ClintCourses.objects.filter(the_course=self)
    result =  ((pple) * self.cost_forone) - self.Voucher
    dont_repeat = []
    for i in pple_in_course:
      if i not in dont_repeat:
        result -= i.the_client.voucher
        dont_repeat.append(i)

    return result
  # 
  def Percenage(self):
    return f"{self.per_for_inst}%"
  # 
  def more(self):
    return "more"
  # 
  def clients_in_course(self):
    pple = ClintCourses.objects.filter(the_course=self)
    return f"{len(pple) }"


  def Day_per_week_(self):
    days = self.Day_per_week.all()
    se = []
    for i in days:
      se.append(i.day)
    if len(se) == 0:
      return "You havent config the days"
    
    return ", ".join(se)


class Client(models.Model):
  # 
  name           = models.CharField(max_length=255)
  phone_number   = models.CharField(max_length=255)
  birth_day      = models.DateField(default=datetime.datetime.now, blank=True, null=True)
  paid           = models.IntegerField(default=0, blank=True, verbose_name="Paid")
  have_debt      = models.BooleanField(default=True, )
  payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
  voucher        = models.FloatField(default=0, blank=True, verbose_name="Voucher")
  time_added     = models.DateField(default=datetime.datetime.now,  verbose_name="Time added",)
  # 
  def month_with_year(self):
    
    
    
    return "-".join(str(self.time_added).split('-')[:-1])
  # 
  def total(self):
    cost  = ClintCourses.objects.filter(the_client=self)
    result= 0
    for i in cost:
      result += i.the_course.cost_forone
    if self.voucher == 0 or self.voucher == None:
      
      return result
    
    return  result - self.voucher
  # 
  def more(self):
    return "More"
  # 
  def courses_in(self):
    x = ClintCourses.objects.filter(the_client=self)
    courses_type = []
    for i in x:
      courses_type.append(i.the_course.coursetype.Name)
    if len(courses_type) == 0:
      return "He is not in course"
    return ", ".join(courses_type)
  # 
  def still_have_to_pay(self):
    still_didt_pay = float(self.total()) - float(self.paid)
    if still_didt_pay <= 0 :
      return "He is Clear"
    return still_didt_pay

  def __str__(self):
    return f"{self.name}"
  # 
  def save(self):
    if self.paid == None:
      self.paid  =0
    super().save()
    if self.still_have_to_pay() == "He is Clear":
      self.have_debt = False
    else:
      self.have_debt = True
    super().save()
  # 
  class Meta:
    app_label = app_label
  # 
  def save_model(self, request, obj, form, changed):
    if '_continue' in request.POST:
        if self.paid == None:
          self.paid  =0
        super().save()
        if self.still_have_to_pay() == "He is Clear":
          self.have_debt = False
        else:
          self.have_debt = True
        super().save()
    return super().change_view(request, obj, form, changed)
  # 
  def Attnder(self):
    my_ = ClintCourses.objects.filter(the_client=self)

    div = '''
    
    <div>
    
          '''
    
    for i in my_:

      try:
        
        days = i.Atten.split(',')
      except:
        days = None
      

        days_html = f"""
      <hr>
      <h2>
        {i.the_course.coursetype}
      </h2> 
      <a 
        href='{reverse("attend",args=(i.pk,))}' 
        target='popup'
        >
          Edit it
        </a>
        <br>
        You havn't set it up yet  
        <hr
        > <br>"""
      days_html = mark_safe(days_html)
      

      if days is not None:
        the_cours_name = i.the_course.coursetype
        days_html = f''' 
        
        <hr>
        <h2>
        {the_cours_name}
        </h2>
        <a 
        href='{reverse("attend",args=(i.pk,))}' 
        target='popup'
        >
          Edit it
        </a>
        '''
        for m in days:
          days_html += f"<p> {m}</p>"

        days_html += '<hr>'
        days_html = mark_safe(days_html)

      div += mark_safe(days_html)
    
  
    div += mark_safe("</div>")
    div += mark_safe( ''' 
          <script>
    links = document.querySelectorAll('a[target=popup]');
    
    for ( link of links) {
        link.addEventListener('click', ()=>{
            window.open(link.getAttribute("href"), 'popup',' width=600,height=600'); return false; 
        }) 
    }
          </script>''')
    return mark_safe(div) 

class ClientScore(models.Model):
  the_client   = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
  the_course   = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
  client_score = models.IntegerField()
  max_score = models.IntegerField()
  
class ClintCourses(models.Model):
  
  the_course = models.ForeignKey(Course, on_delete=models.CASCADE)
  the_client = models.ForeignKey(Client, on_delete=models.CASCADE)
  th_group   = models.ForeignKey('config.CourseGroup',verbose_name="Group", on_delete=models.SET_NULL, null=True, blank=True)
  the_level  = models.ForeignKey("config.Level", on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Level")
  Atten      = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.the_client.name}|{self.the_course.coursetype.Name}"


class Service(models.Model):
  # 

  # 
  class Meta:
    app_label = app_label


# 
class Instructors(models.Model):
  # 
  name         = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=255, blank=True, null=True)
  specialty    = models.ManyToManyField("config.CourseType",related_name="speciality",blank=True)

  # 
  def __str__(self):
    return f"{self.name}"
  # 
  def specialities(self):
    data = self.specialty.all()
    s = []
    for i in data:
      s.append(i.Name)
    if len(s) == 0:
      return "Empty"
    return " ,".join(s)
  # 
  def salary(self):
    courses = Course.objects.filter(Instructor=self)
    result = 0
    for i in courses:
      n  = i.income() * (i.per_for_inst / 100)
      result += n
      
    return result
    
  def income(self):
    courses =  Course.objects.filter(Instructor=self)
    result = 0
    for cour in courses:
      result += cour.income()
    return result
  # 
  def more(self):
    return "more"
  
  
  class Meta:
    verbose_name = "Instructor"
  


# Employee section
# _____________________________________

class vacation(models.Model):
  # 
  choices = (
    ("Sick leave", "Sick leave"),
    ("weekends", "weekends")    ,
    
  )
  Emp           = models.ForeignKey("Employee", on_delete=models.CASCADE)
  vacation_type = models.CharField(choices=choices, max_length=300) 
  how_many_days = models.IntegerField(verbose_name="how many days",default=0 )
  # 
  class Meta:
        app_label = app_label
  # 
  def __str__(self):
    return f"{self.vacation_type}|{self.how_many_days}"
  
class Absent(models.Model):
  # 
  Emp           = models.ForeignKey("Employee", on_delete=models.CASCADE)
  how_many_days = models.IntegerField(verbose_name="how many days") 
  Reson         = models.TextField(verbose_name="reason", blank=True, default=" ")
  # 
  def __str__(self):
    return f"{self.how_many_days} day"
  # 
  class Meta:
    app_label = app_label
  

class Deduction(models.Model):
  # 
  Emp        = models.ForeignKey("Employee", on_delete=models.CASCADE)
  The_amount = models.IntegerField(verbose_name="Amount")
  the_reson  = models.TextField(null=True, blank=True, verbose_name="reason")
  # 
  class Meta:
    app_label = app_label
  # 
  def __str__(self):
    return f"{self.The_amount}"


class Reward(models.Model):
  # 
  Emp        = models.ForeignKey("Employee", on_delete=models.CASCADE)
  The_amount = models.IntegerField(verbose_name="Amount")
  the_reson  = models.TextField(null=True, blank=True, verbose_name="reason")
  img        = models.ImageField(verbose_name="Picture if there certificate[optional]", blank=True)
  # 
  class Meta:
    app_label = app_label
  # 
  def __str__(self):
    return f"{self.The_amount}"




class Employee(models.Model):
  # 
  choices = (
    ("Married" , "Married" ),
    ("Single"  , "Single")  ,
    ("Divorced", "Divorced"),
    ("Widower" , "Widower") ,
  )
  name             = models.CharField(max_length=255)
  Person_identf    = models.CharField(max_length=255, default=" ",verbose_name="ID", null=True, blank=True) 
  EDU_state        = models.CharField(max_length=300, default=" ", null=True, blank=True, verbose_name="Educational Level") 
  address          = models.CharField(max_length=300, default=" ", null=True, blank=True) 
  img              = models.ImageField(upload_to="EMP Pic", verbose_name=" ", blank=True)
  cur_sallary      = models.FloatField(verbose_name="Current Salary") 
  Date_of_join     = models.DateField(default=datetime.datetime.now)
  state_of_marrieg = models.CharField(choices=choices, verbose_name="Person state", max_length=300)
  phone_number     = models.CharField(max_length=20, verbose_name="Phone number", blank=True, null=True)
  phone_number_eme = models.CharField(max_length=20, verbose_name="Emergency phone number", blank=True, null=True)
  job_postition    = models.ForeignKey(JobPosition, null=True, on_delete=models.SET_NULL, blank=True)
  more             = models.CharField(editable=False, default="More",max_length=10)
  # 
  def image_tag(self):
    return mark_safe(f'<img style="width:200px;hieght:200px" src="{HOST[:-1]}{ self.img.url}" />' )
  # 
  def __str__(self):
    return f"{self.name}"
  # 
  class Meta:
    app_label = app_label
  
  image_tag.short_description = 'Image'
  image_tag.allow_tags = True



# 
