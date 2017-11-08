from django.db import models
import uuid

INCIDENT_TYPES = (
	(1, "Under Construction Patch"),
	(2, "Pothole Found"),
	(3, "Accident Site"),
	(4, "Others"),
)

state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

class Operator(models.Model):
	name = models.CharField(max_length=255)
	penalty = models.FloatField(default=0)

	def __str__(self):
		return self.name

class Traveller(models.Model):
	name = models.CharField(max_length=255)
	trust = models.FloatField(default=0.50)
	last_latitude = models.DecimalField(default=19.0760,decimal_places=6,max_digits=10)
	last_longitude = models.DecimalField(default=72.8777,decimal_places=6,max_digits=10)
	credits = models.FloatField(default=0)
	def __str__(self):
		return self.name

TRIGGERS = (
	(1,"Decelaration"),
	(2,"Lane Switching"),
	(3,"Confirmation"),
)

ROAD_CONDITION = (
	(1, "Very Poor"),
	(2, "Poor"),
	(3, "Average"),
	(4, "Good"),
	(5, "Very Good"),
)

#Need to combine some reportings into an information with a relevant trust score algorithm
class Report(models.Model):
	reporting_time = models.DateTimeField()
	reporter = models.ForeignKey('Traveller',related_name='report')
	latitude = models.DecimalField(default=0.0,decimal_places=6,max_digits=10)
	longitude = models.DecimalField(default=0.0,decimal_places=6,max_digits=10)
	incident = models.IntegerField(choices=INCIDENT_TYPES,default=4) #Inferred from TRIGGERS
	road = models.ForeignKey('Road',related_name='report')
	trigger = models.IntegerField(choices=TRIGGERS,default=1)
	severity = models.IntegerField(choices=ROAD_CONDITION,default=3)
	information = models.ForeignKey('Information',related_name='reports') #This would be deduced.
	processed = models.IntegerField(default=0) #Whether affect of report has been considered?
	credits = models.IntegerField(default=0) #Value given for this report?
	def __str__(self):
		return self.reporter.name+"-"+str(self.reporting_time)

class Information(models.Model):
	latitude = models.DecimalField(default=0.0,decimal_places=4,max_digits=10)
	longitude = models.DecimalField(default=0.0,decimal_places=4,max_digits=10)
	incident = models.IntegerField(choices=INCIDENT_TYPES,default=4)
	trust = models.FloatField(default=0.0)
	road = models.ForeignKey('Road',related_name='information')
	last_report_time = models.DateTimeField()
	first_report_time = models.DateTimeField()
	avg_severity = models.FloatField(default=0)
	report_count = models.IntegerField(default=1)
	status = models.IntegerField(default=0)
	def __str__(self):
		return self.road.name+"-"+str(self.trust)

class Road(models.Model):
	name = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(choices=state_choices,max_length=255)
	penalty = models.IntegerField(default=0) # Penalty to the operator for this road.
	operator = models.ForeignKey('Operator',related_name='road')
	def __str__(self):
		return self.name+", "+self.city+", "+self.state+" : "+self.operator.name


ADDRESS_CHOICES = (
	("Office","Office"),
	("Residence","Residence")
)
class AlumniCartd(models.Model):
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(choices=state_choices,max_length=255)
	dob = models.DateField()
	first_degree_name = models.CharField(max_length=255)
	first_degree_branch = models.CharField(max_length=255)
	first_degree_year = models.IntegerField()
	present_dept = models.CharField()
	present_office = models.TextField()
	present_residence = models.TextField()
	telephone = models.
	mobile = models.
	email = models.EmailField()
	address_for_correspondence = models.IntegerField(choices=ADDRESS_CHOICES)
	payment = 
	graduation = models.ImageField()
	sign = models.ImageField()
	photo = models.ImageField()