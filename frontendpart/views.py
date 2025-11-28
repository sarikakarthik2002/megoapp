from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from myapp.models import *
from myapp.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
    user=request.user
    randomCourses = courses.objects.order_by('?')[:3]
    if user.is_authenticated:
        cart_items = list(CartItems.objects.filter(userid=user).values_list('courseid', flat=True))
        enrolled_courses = EnrolledCourses.objects.filter(userid=request.user).select_related('courseid')
        enrolled_course_ids = enrolled_courses.values_list('courseid_id', flat=True)
    else:
        cart_items =[]
        enrolled_courses=[]
        enrolled_course_ids=[]
    context = {
        'cart_items': cart_items,
        'enrolled_courses': enrolled_course_ids,
        'user':user,
        'randomCourses':randomCourses
    }
    return render(request,"frontend/home.html",context)


def card(request):
    user = request.user
    courses_list = courses.objects.all()
    if user.is_authenticated:
        cart_items = list(CartItems.objects.filter(userid=user).values_list('courseid', flat=True))
        enrolled_courses = EnrolledCourses.objects.filter(userid=request.user).select_related('courseid')
        enrolled_course_ids = enrolled_courses.values_list('courseid_id', flat=True)
    else:
        cart_items =[]
        enrolled_courses=[]
        enrolled_course_ids=[]
    context = {
        'data': courses_list,
        'cart_items': cart_items,
        'enrolled_courses': enrolled_course_ids,
    }
    return render(request, 'frontend/cards.html', context)

@login_required(login_url='Login')
def profile(request):
    user = request.user
    data = CustomUser.objects.get(id=user.id)
    if request.method == 'POST':
        form = myupdateform(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user.first_name = form.cleaned_data['first_name'] 
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone_number = form.cleaned_data['phone_number']
            user.username = form.cleaned_data['username']
            user.save()
            return redirect('profile')
    return render(request, 'frontend/profile.html',{'data':data})


@login_required(login_url='Login')
def Delete(request):
    data=request.user
    userdata=CustomUser.objects.get(username=data)
    userdata.delete()
    return redirect('home')

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'frontend/changepassword.html'
    success_url = reverse_lazy('password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

@login_required(login_url='Login')
def cart(request):
    user = request.user
    cart_items = CartItems.objects.filter(userid=user).select_related('courseid')
    total_price = sum(item.courseid.courseprice for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }    
    return render(request, 'frontend/cart.html', context)


@login_required(login_url='Login')
def addtocart(request,id):
    user=request.user
    course = get_object_or_404(courses, id=id)
    cart_item, created = CartItems.objects.get_or_create(userid=user,courseid=course)
    return redirect('card')
    
@login_required(login_url='Login')
def remove_from_cart(request,id):
    cart_item = get_object_or_404(CartItems, id=id, userid=request.user)
    course_name = cart_item.courseid.coursename
    cart_item.delete()
    # messages.success(request, f"{course_name} has been removed from your cart.")
    return redirect('cart') 

@login_required(login_url='Login')
def checkout(request,id=None):
    user=request.user
    items=None
    total_price=None
    if id==None:
        items = CartItems.objects.filter(userid=user)
        total_price = sum(item.courseid.courseprice for item in items)
        if not items:
            return redirect('cart')
    else:
        items = courses.objects.filter(id=id)
        total_price = items[0].courseprice
    context = {
            'cart_items': items,
            'id':id,
            'total_price': total_price,
        }  
    return render(request, 'frontend/checkout.html', context)


@login_required(login_url='Login')
def enroll(request,id=None):
    user = request.user
    items=None
    if request.method == 'POST':
        if id==None:
            items = CartItems.objects.filter(userid=user).select_related('courseid')
            for item in items:
                    if not EnrolledCourses.objects.filter(userid=user, courseid=item.courseid).exists():
                        EnrolledCourses.objects.create(userid=user, courseid=item.courseid)
            items.delete()
            return redirect('enroll_courses')
        else:
            items=courses.objects.get(id=id)
            cartitem=CartItems.objects.filter(userid=user,courseid=items)
            if not EnrolledCourses.objects.filter(userid=user, courseid=items).exists():
                EnrolledCourses.objects.create(userid=user, courseid=items)
            cartitem.delete()
            return redirect('enroll_courses')
    
    # return render(request, 'frontend/enroll.html')


@login_required(login_url='Login')
def enroll_courses(request):
    enrolled_courses = EnrolledCourses.objects.filter(userid=request.user).select_related('courseid')
    context = {
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'frontend/enrollcourses.html', context)






