
from django.urls import path
from course import views

urlpatterns = [
	
	# path('',views.Showindex,name="home"),

	path('',views.Showindex.as_view(),name="home"),

	# path('course/',views.Showcourse,name="course"),

	path('course/',views.Showcourse.as_view(),name="course"),

	# path('my_course/',views.MyCourse,name="my_scourse"),

	path('my_course/',views.MyCourse.as_view(),name="my_course"),

	path('check_out/<str:slug>',views.Checkout, name = "check_out"),

	path('show_more/<str:slug>',views.ShowMore, name='show_more'),

	# path('register/',views.Register,name='register'),

	path('register/',views.Register.as_view(),name='register'),

	# path('login/',views.Login, name='login')
	 path('login/',views.LoginView.as_view(), name='login'),

	 path('logout/',views.Signout, name= 'logout'),

	 path("verify_payment",views.Verify_payment,name='verify_payment'),

]