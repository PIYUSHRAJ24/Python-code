from django.contrib import admin
from django.utils.html import format_html
from course.models import CourseModel ,TagModel , PrerequisiteModel , LearningModel

from course.models import UserCourseModel
from course.models import PaymentModel
from course.models import VideoModel



class TagAdmin(admin.TabularInline):
	model = TagModel

class VideoAdmin(admin.TabularInline):
	model = VideoModel


class PrerequisiteAdmin(admin.TabularInline):
	model = PrerequisiteModel

class LearninAdmin(admin.TabularInline):
	model = LearningModel

class CourseAdmin(admin.ModelAdmin):
	inlines = [ TagAdmin , PrerequisiteAdmin , LearninAdmin,VideoAdmin]

class CourseAdmin(admin.ModelAdmin):
	model = CourseModel
	list_display = ['name', 'get_price', 'get_discount', 'active']
	list_filter = ['name', 'active']

	def get_price (self,course):
		return f'₹ {course.price}'

	def get_discount(admin, course):
		return f'{course.discount}%'

	get_discount.short_description = 'discount'

	get_price.short_description = "price"

admin.site.register(CourseModel , CourseAdmin)

admin.site.register(VideoModel)

admin.site.register(UserCourseModel)

@admin.register(PaymentModel)
class Pyament(admin.ModelAdmin):
	model = PaymentModel
	list_display = [ 'order_id', "get_user"  ,'course', 'status']
	list_filter = ['user' , 'status']

	def get_user(self, payment):
		return format_html(f"<a target='_blank' href='/admin/auth/user/'>{payment.user}</a>")
	get_user.short_description = 'user'
