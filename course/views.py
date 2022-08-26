import razorpay
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from course.models import CourseModel
from course.models import PaymentModel , UserCourseModel
from course.models import VideoModel,PrerequisiteModel,LearningModel,TagModel
from time import time
from django.shortcuts import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import login
from forms.form import RegistrationFrom
from forms.login_form import LoginForm
from django.views.decorators.csrf import csrf_exempt
from OnlineCourse.settings import *
from django.contrib.auth.decorators import login_required 
from django.views.generic import ListView , TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

class Showindex(TemplateView):
	template_name = 'common/home.html'
	
# def Showindex(request):
# 	return render(request, "common/home.html")

@method_decorator(login_required(login_url='login') , name= 'dispatch')
class MyCourse(ListView):
	template_name = 'course/my_course.html'
	
	context_object_name = 'uc'

	def get_queryset(self):
		return UserCourseModel.objects.filter( user=self.request.user)
# @login_required(login_url="login")
# def MyCourse(request):
# 	user =request.user
# 	user_course = UserCourseModel.objects.filter(user=user)

# 	return render( request, 'course/my_course.html',{"uc":user_course})


class Showcourse(ListView):
	template_name = 'course/course.html'
	queryset = CourseModel.objects.all()

	

# def Showcourse(request):
# 	course = CourseModel.objects.all()
# 	return render(request, "course/course.html",{"course":course})


def ShowMore(request, slug ):
	# print(slug)
	course = CourseModel.objects.get(slug = slug)
	
	pre = PrerequisiteModel.objects.filter(course = course)
	tag = TagModel.objects.filter(course = course)
	learning = LearningModel.objects.filter(course = course)
	video = VideoModel.objects.filter(course = course)

	serial_number = request.GET.get('lecture')

	if serial_number is None:
		serial_number = 1

	video_get =VideoModel.objects.get( course = course , serial_number =serial_number)
	
	if video_get.is_preview is False:

		if request.user.is_authenticated is False:
			return redirect('register')
		else:
			user = request.user
			try:
				usercourse = UserCourseModel.objects.get( course= course , user=user)
			except:
				return redirect ('check_out' , slug=course.slug)


	data = {
		'course':course,
		'video' :video,
		'tag' : tag,
		'pre' : pre,
		'learn':learning,
		'video_get': video_get
	}

	return render(request , "course/show_more.html", data)



@login_required(login_url = 'login')
def Checkout(request,slug):
	course = CourseModel.objects.get(slug= slug)
	# user =None
	# if not request.user.is_authenticated:
	# 	return redirect('login')
	user = request.user
	
	action = request.GET.get('action')
	order = None
	payment = None
	error = None

	if action == "create_payment":

		try:
			user_course = UserCourseModel.objects.get(course= course, user=user)
			error = "you are alredy Subscribed this course"
		except:
			pass

		if error is None:
			amount= int((course.price -(course.price * course.discount * 0.01 ))*100)
			currency= "INR"
			receipt= f"order_rcptid-{int(time())}"
			notes = {
			"email": user.email,
			'name' :f"{user.first_name} {user.last_name}"
			}
	  
			order = client.order.create({"receipt":receipt,
			'amount':amount, 
			'currency':currency,
			'notes':notes})
	
			payment = PaymentModel()
			payment.user = user
			payment.course = course
			payment.order_id = order.get("id")
			payment.save()

	
	context ={
	 		'course' :course,
	  		'order' : order,
			'payment' : payment,
			'user' : user,
			'error': error
			}
	return render( request ,'course/check_out.html',context)

@csrf_exempt
def Verify_payment(request):
	if request.method == "POST":
		data = request.POST
		print(data)
		context={}
		try:
			client.utility.verify_payment_signature(data)
			razorpay_order_id = data['razorpay_order_id']
			razorpay_payment_id = data['razorpay_payment_id']

			payment = PaymentModel.objects.get(order_id = razorpay_order_id)
			payment.payment_id = razorpay_payment_id
			payment.status = True

			usercourse = UserCourseModel(user = payment.user , course = payment.course)
			usercourse.save()

			payment.user_course = usercourse
			payment.save()

			return render(request , "course/my_course.html")			
		except:
			return HttpResponse("invalid user")

# function base views
# def Register(request):
# 	form = RegistrationFrom( request.POST)
# 	if form.is_valid():
# 		user = form.save()
# 		return redirect('login')

# 	else:
# 		return render(request, 'course/register.html',{'form' :form})

class Register(FormView):
	template_name = 'course/register.html'
	form_class = RegistrationFrom
	success_url = 'login'

	def form_valid(self,form):
		form.save()

		return super().form_valid(form)


# class Login(View):
# 	def get(self ,request):
# 		form = LoginForm()
# 		return render (request, "course/login.html",{"form":form} )

# 	def post(self ,request):
# 		form = LoginForm(request = request , data = request.POST)
# 		print(form)
# 		if form.is_valid():
# 			return redirect ('course')
# 		else:
# 			return render (request, "course/login.html",{"form":form})

class LoginView(FormView):
	template_name = 'course/login.html'
	form_class = LoginForm
	success_url = "/"

	def form_valid(self,form):
		login(self.request , form.cleaned_data)

		next_page=self.request.GET.get("next")
		if next_page is not None:
			return redirect(next_page)

		return super().form_valid(form)

def Signout(request):
	logout(request)
	return redirect('home')
