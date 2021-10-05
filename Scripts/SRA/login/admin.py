from django.contrib import admin
from .models import *

# Register your models here.


class StudentsAdmin(admin.ModelAdmin):

    list_display = ('first_name',
                    'last_name', 'mobile', 'email', 'standard', 'divison', 'fee_per_month', 'date_created',)

    list_filter = ('date_created',)
    search_fields = ('first_name', 'mobile')


class TeacherAdmin(admin.ModelAdmin):

    list_display = ('fname',
                    'lname', 'sub', 'qual', 'join_date', 'active')

    list_filter = ('sub',)
    search_fields = ('fname',)


class ExpenditureAdmin(admin.ModelAdmin):

    list_display = ('Expenditure_Name',
                    'Payment_type', 'Amount', 'Date')

    list_filter = ('Payment_type',)
    search_fields = ('Date',)


class Teacher_paymentAdmin(admin.ModelAdmin):

    list_display = ('Teacher',
                    'payment_type', 'amount', 'date')

    list_filter = ('payment_type',)
    search_fields = ('Teacher',)


class Student_feeAdmin(admin.ModelAdmin):

    list_display = ('Student',
                    'payment_type', 'amount', 'date')

    list_filter = ('payment_type',)
    search_fields = ('Student',)


admin.site.register(Students, StudentsAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)
admin.site.register(Teacher_payment, Teacher_paymentAdmin)
admin.site.register(Student_fee, Student_feeAdmin)

admin.site.site_title = "Shivansh SunRise Acedmy"
admin.site.site_header = "Shivansh SunRise Acedmy"
admin.site.index_title = "Shivansh SunRise Acedmy"
