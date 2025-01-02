from django.db import models

class contactus(models.Model):
    Full_name=models.CharField(max_length=30)
    Email=models.EmailField()
    Phone_number=models.CharField(max_length=10)
    Message=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.Full_name}"
    


class Admission(models.Model):
    COURSE_CHOICES = [
        ('programming', 'Programming'),
        ('web_development', 'Web Development'),
        ('data_science', 'Data Science'),
        ('machine_learning', 'Machine Learning'),
        ('cloud_computing', 'Cloud Computing'),
        ('cyber_security', 'Cyber Security'),
        ('game_development', 'Game Development'),
        ('civil_cad', 'Civil CAD'),
        ('mechanical_cad', 'Mechanical CAD'),
        ('digital_marketing', 'Digital Marketing'),
        ('graphic_design', 'Graphic Design'),
        ('other', 'Other Programs'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    address = models.CharField(max_length=255, verbose_name="Address")
    qualification = models.CharField(max_length=150, verbose_name="Qualification")
    passed_out = models.BooleanField(default=False, verbose_name="Passed Out")
    passed_out_year = models.IntegerField(null=True, blank=True, verbose_name="Passed Out Year")
    college_name = models.CharField(max_length=150, verbose_name="College Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    course = models.CharField(max_length=50, choices=COURSE_CHOICES, verbose_name="Selected Course")
    message = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Submission Date")

    def __str__(self):
        return f"{self.full_name} - {self.course}"

class Course(models.Model):
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return self.name