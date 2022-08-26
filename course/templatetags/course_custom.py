from atexit import register
from django import template
import math
from course.models import UserCourseModel,CourseModel


register = template.Library()

@register.simple_tag
def cal_sell_price(price , discount):
    if discount is None or discount is 0:
        return price
    sellprice = price

    sellprice = price -(price*discount*0.01 )
    return math.floor(sellprice)


@register.filter(name='rupee')
def rupee (price):
    return f'₹ {price}/-'

@register.simple_tag
def is_enroll(request , course):
    user= None
    if not request.user.is_authenticated:
        return False

    user = request.user
    try:
        user_course = UserCourseModel.objects.get(course= course, user=user)
        return True
    except:
        return False






