from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('student/', views.student, name='student'),
    path('student_fees/', views.student_fees, name='student_fees'),
    path('teacher/', views.teacher, name='teacher'),
    path('expend/', views.expend, name='expend'),
    path('expend_update/<str:pk>/', views.expend_update, name='expend_update'),
    path('delete_update/<str:pk>/', views.delete_update, name='delete_update'),
    path('teacher_update/<str:pk>/', views.teacher_update, name='teacher_update'),
    path('teacher_delet/<str:pk>/', views.teacher_delet, name='teacher_delet'),
    path('teacher_pay/', views.teacher_pay, name='teacher_pay'),
    path('teacher_pay_update/<str:pk>/',
         views.teacher_pay_update, name='teacher_pay_update'),
    path('teacher_pay_delete/<str:pk>/',
         views.teacher_pay_delete, name='teacher_pay_delete'),

    path('student_update/<str:pk>/', views.student_update, name='student_update'),
    path('student_delete/<str:pk>/', views.student_delete, name='student_delete'),

    path('studentfee_update/<str:pk>/',
         views.studentfee_update, name='studentfee_update'),
    path('studentfee_delete/<str:pk>/',
         views.studentfee_delete, name='studentfee_delete'),

    path('dataprint/<str:pk>/', views.dataprint, name='dataprint'),
    path('dataprintstudent/<str:pk>/',
         views.dataprintstudent, name='dataprintstudent'),
    path('dataprintteach/<str:pk>/',
         views.dataprintteach, name='dataprintteach'),
    path('report/', views.report, name='report'),
    path('student_report/', views.student_report, name='student_report'),
    path('teachers_report/', views.teachers_report, name='teachers_report'),
    path('expenditure_report/', views.expenditure_report,
         name='expenditure_report'),
    re_path(r'^std_rpt/(?P<frm>[\w-]+)/(?P<to>[\w-]+)/(?P<id>[\w-]+)',
            views.std_rpt, name='std_rpt'),

    re_path(r'^std_rpt_date/(?P<frm>[\w-]+)/(?P<to>[\w-]+)',
            views.std_rpt, name='std_rpt_date'),

    re_path(r'^teach_rpt/(?P<frm>[\w-]+)/(?P<to>[\w-]+)/(?P<id>[\w-]+)',
            views.teach_rpt, name='teach_rpt'),

    re_path(r'^teach_rpt_date/(?P<frm>[\w-]+)/(?P<to>[\w-]+)',
            views.teach_rpt, name='teach_rpt_date'),

    re_path(r'^expend_date/(?P<frm>[\w-]+)/(?P<to>[\w-]+)',
            views.expend_date, name='expend_date'),

]
