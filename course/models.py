from django.db import models
from django.contrib.auth.models import User


class CourseModel(models.Model):
	name = models.CharField(max_length= 30, null=False)
	slug = models.CharField(max_length= 350, null=False, default='char')
	descripation = models.CharField(max_length=300, null=True)
	price = models.IntegerField(null=False)
	discount = models.IntegerField(null=False , default=0)
	active = models.BooleanField(default=False)
	thumbnail = models.ImageField(upload_to='file/thumbnail')
	date = models.DateTimeField(auto_now_add=True)
	resource = models.FileField(upload_to='file/resource')
	length = models.IntegerField(null=False)

	def __str__(self):
		return self.name


class CourseProperty(models.Model):
	discription = models.CharField(max_length=300 , null=False)
	course = models.ForeignKey(CourseModel , null=False , 
		on_delete=models.CASCADE)

	class Meta:
		abstract = True


class TagModel(CourseProperty):
	pass
	
class PrerequisiteModel(CourseProperty):
	pass

class LearningModel(CourseProperty):
	pass 


class VideoModel(models.Model):
	title  = models.CharField(max_length=1000, null =False)
	course = models.ForeignKey(CourseModel , null=False, on_delete=models.CASCADE)
	serial_number = models.IntegerField(null = False)
	video_id = models.CharField(max_length= 30,  null=False)
	is_preview = models.BooleanField(default=False)

	def __str__(self):
		return self.title



class UserCourseModel(models.Model):
	user = models.ForeignKey(User , null=False, on_delete=models.CASCADE)
	course = models.ForeignKey(CourseModel , null=False, on_delete=models.CASCADE )
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{ self.user.username } - { self.course.name }'

class PaymentModel(models.Model):
	order_id = models.CharField(max_length=50 , null=False)
	payment_id = models.CharField(max_length=50)
	user = models.ForeignKey(User , on_delete=models.CASCADE)
	user_course = models.ForeignKey(UserCourseModel , null=True , blank =True ,on_delete=models.CASCADE)
	course = models.ForeignKey( CourseModel , on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=False)

	# def __str__(self):
	# 	return self.user