from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

def register(request):
    f=myregisterform()
    if request.method=="POST":
        f1=myregisterform(request.POST)
        if f1.is_valid():
            print(f1)
            f1.save()
            print(f1.cleaned_data)
            return HttpResponse("registraration sucess")
    return render(request,'admin/register.html',{'f':f})


def Login(request):
    f=myloginform()
    if request.method=="POST":
        f1=myloginform(request.POST)
        if f1.is_valid():
            username=f1.cleaned_data['username']
            password=f1.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse("login error")
    return render(request,'admin/login.html',{'f':f})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def course(request):
    f = coursesForm()
    if request.method == 'POST':
        form = coursesForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('coursemenu')
    return render(request, 'admin/course.html', {'f': f})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def courseconcept(request):
    f = courseconceptsform()
    if request.method == 'POST':
        form = courseconceptsform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admincourseconcept')
    return render(request, 'admin/courseconcept.html', {'f': f})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def admincourseconcept(request):
    data=courseconcepts.objects.all()
    return render(request,'admin/courseconeptmenu.html',{'data':data})


@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def deleteadmincourseconcept(request,id):
    data=courseconcepts.objects.get(id=id)
    data.delete()
    return redirect('admincourseconcept')


@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def admincoursemenu(request):
    data=courses.objects.all()
    return render(request,'admin/coursemenu.html',{'data':data})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def admincoursedelete(request,id):
    data=courses.objects.get(id=id)
    data.delete()
    return redirect('coursemenu')

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def admincourseupdate(request,id):
    data=courses.objects.get(id=id)
    f=coursesForm(instance=data)
    if request.method == 'POST':
        form = courseconceptsform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('coursemenu')
    return render(request,'admin/course.html',{'f':f})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def Logout(request):
    logout(request)
    return redirect('home')


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# class UsersData(ListView,StaffRequiredMixin,LoginRequiredMixin):
#     model = CustomUser
#     template_name = 'admin/userDetails.html'
#     paginate_by = 10
#     def get_queryset(self):
#         return CustomUser.objects.all().order_by('-date_joined')


class UserSearchView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('query', '')
        page_number = request.GET.get('page', 1)

        users = CustomUser.objects.all().order_by('-date_joined')
        if query:
            users = users.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(address__icontains=query)
            )

        paginator = Paginator(users, 10)
        page_obj = paginator.get_page(page_number)

        context = {
            'users': page_obj.object_list,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                template_name='admin/user_list_partial.html',
                context=context
            )
            return JsonResponse({
                'html': html,
                'current_page': page_obj.number,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            })

        return render(request, 'admin/userDetails.html', context)

# class UserSearchView(LoginRequiredMixin, StaffRequiredMixin, View):
#     def get(self, request):
#         query = request.GET.get('query', '')
#         users = CustomUser.objects.all()
        
#         if query:
#             users = users.filter(
#                 Q(username__icontains=query) |
#                 Q(email__icontains=query) |
#                 Q(first_name__icontains=query) |
#                 Q(last_name__icontains=query) |
#                 Q(phone_number__icontains=query) |
#                 Q(address__icontains=query)
#             ).order_by('-date_joined')
        
#         context = {
#             'users': users,
#         }
        
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             html = render_to_string(
#                 template_name='admin/user_list_partial.html',
#                 context=context
#             )
#             return JsonResponse({
#                 'html': html,
#                 'count': users.count()
#             })
            
#         return render(request, 'admin/userDetails.html', context)






@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff)
def usercreate(request):
    if request.method == 'POST':
        form = adminusercreateform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usersdata')
    else:
        form = adminusercreateform()
    return render(request, 'admin/adminuser.html', {'form': form})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def userupdate(request,id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = adminuserupdateform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('usersdata')
    else:
        form = adminuserupdateform(instance=user)
    return render(request, 'admin/adminuser.html', {'form': form, 'is_edit': True})

@login_required(login_url='Login')
@user_passes_test(lambda user: user.is_staff) 
def userdelete(request, id):
    user = get_object_or_404(CustomUser, id=id)
    # if request.method == 'POST':
    user.delete()
    # messages.success(request, f'User {user.username} has been deleted successfully.')
    return redirect('usersdata')
    # return render(request, 'coursesAdmin/userConfirmDelete.html',{'user': user})
