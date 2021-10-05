from django.db import models

# Create your models here.


class Students(models.Model):

    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    standard = models.CharField(max_length=10, null=True)
    divison = models.CharField(max_length=10, null=True)
    fee_per_month = models.IntegerField()

    def __str__(self):

        return self.first_name + " " + self.last_name


class Teacher(models.Model):

    activ = (
        ("Active", "Active"),
        ("Not Active", "Not Active")
    )

    fname = models.CharField(max_length=25, null=True)
    lname = models.CharField(max_length=25, null=True)
    sub = models.CharField(max_length=20, null=True)
    qual = models.CharField(max_length=50, null=True)
    join_date = models.DateField()
    Add = models.CharField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    active = models.CharField(max_length=10, null=True, choices=activ)

    def __str__(self):

        return self.fname


class Expenditure(models.Model):

    ex_type = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("dd", "dd")
    )

    Expenditure_Name = models.CharField(max_length=25, null=True)
    Payment_type = models.CharField(max_length=25, null=True, choices=ex_type)
    Amount = models.CharField(max_length=50, null=True)
    Date = models.DateField()

    def __str__(self):

        return self.Expenditure_Name


class Student_fee(models.Model):

    ex_type = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("dd", "dd")
    )

    Student = models.ForeignKey(Students, null=True, on_delete=models.SET_NULL)
    payment_type = models.CharField(max_length=10, null=True, choices=ex_type)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):

        return self.Student.first_name


class Teacher_payment(models.Model):

    ex_type = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("dd", "dd")
    )

    Teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    payment_type = models.CharField(max_length=10, null=True, choices=ex_type)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):

        return self.Teacher.fname
