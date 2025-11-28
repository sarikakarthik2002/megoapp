"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *
from frontendpart.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('signup/',register,name='register'),
    path('login/',Login,name='Login'),
    path('logout/',Logout,name="logout"),
    path('course/',course,name='course'),
    path('concept/',courseconcept,name='courseconcept'),
    path('card/',card,name="card"),
    path('admincards/',admincoursemenu,name='coursemenu'),
    path('admindelete/<int:id>/',admincoursedelete,name='coursedelete'),
    path('adminupdate/<int:id>/',admincourseupdate,name='courseupdate'),
    path('profile/',profile,name='profile'),
    path('delete/',Delete,name='Delete'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', TemplateView.as_view(template_name='frontend/password_change_done.html'), name='password_change_done'),
    path('add-to-cart/<int:id>/', addtocart, name='addtocart'),
    path('cart/',cart, name='cart'),
    path('remove-from-cart/<int:id>/',remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='Checkout'),
    path('checkout/<int:id>/', checkout, name='Checkout_with_id'),
    path('enroll/',enroll, name='Enroll'),
    path('enroll/<int:id>/',enroll, name='Enroll_with_id'),
    path('enroll-courses/', enroll_courses, name='enroll_courses'),
    path('conceptmenu/',admincourseconcept,name='admincourseconcept'),
    path('deleteconcept/<int:id>/',deleteadmincourseconcept,name='deleteadmincourseconcept'),
    # path('usersdata/', UsersData.as_view(), name='usersdata'),
    path('usersdata/', UserSearchView.as_view(), name='usersdata'),
    path('usercreate/', usercreate, name='usercreate'),
    path('userupdate/<int:id>/',userupdate, name='userupdate'),
    path('userdelete/<int:id>/',userdelete, name='userdelete'),
]

