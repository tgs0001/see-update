from django.urls import path
from . import views

urlpatterns = [
    
    path('home/',views.home, name='home'),
    path('show_employees/',views.employees_info),
    path('home/select-evaluatee/',views.select_evaluatee, name='select-evaluatee'),
    path('home/select-evaluatee/evaluate/<int:emp_id>/',views.evaluate, name='evaluate'),
    #path('home/select-evaluatee/evaluate',views.evaluate, name='testEvaluate'),

   
    path('home/show_employees/mark',views.mark_employees),
    path('registration/',views.registerPage, name='registration'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('home/profile/',views.showProfileData, name='profile'),
    #path('home/profile/get_employee_data',views.get_employee_data, name='profile'),

    #path('get_employee_data/', views.get_employee_data, name='get_employee_data'),

    path('home/profile/',views.get_employee_data, name='profile'),
    path('home/query/',views.showReport, name='query'),
    #path('home/award/',views.giveAward, name='award'),
    path('home/write-award-description/<int:emp_id>/',views.writeAwardDescription, name='writeAwardDescription'),
    path('home/award/',views.pie_chart, name='award'),
     

]
