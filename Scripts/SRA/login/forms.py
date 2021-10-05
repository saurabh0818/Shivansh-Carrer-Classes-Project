from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class ExpenditureForm(forms.ModelForm):

    class Meta:
        model = Expenditure
        fields = '__all__'
        widgets = {
            'Date':   DateInput(),
        }


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'fname': forms.TextInput(attrs={"placeholder": "Enter First Name", "aria-label": "First Name"}),
            'lname': forms.TextInput(attrs={"placeholder": "Enter Last Name", "aria-label": "First Name"}),
            'sub': forms.TextInput(attrs={"placeholder": "Enter Subject of Techer", "aria-label": "First Name"}),
            'qual': forms.TextInput(attrs={"placeholder": "Enter Qualification of Teacher", "aria-label": "First Name"}),
            'join_date': DateInput(),
            'Add': forms.TextInput(attrs={"placeholder": "Enter Address of Teacher", "aria-label": "First Name"}),




        }
        labels = {
            'fname': "First Name ",
            'lname':  "Last Name ",
            'sub': 'Subject ',
            'qual':   "Qualification ",
            'join_date': "Join Date ",
            'Add':   "Address ",
            'active':   "Active "
        }


class Teacher_paymentForms(forms.ModelForm):

    class Meta:
        model = Teacher_payment
        fields = '__all__'

        widgets = {
            'amount': forms.TextInput(attrs={"placeholder": "Enter Amount", "aria-label": "Amount"}),
            'date': DateInput(),


        }


class StudentsForms(forms.ModelForm):

    class Meta:
        model = Students
        fields = '__all__'

        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "Enter First Name", "aria-label": "First Name"}),
            'last_name': forms.TextInput(attrs={"placeholder": "Enter Last Name", "aria-label": "Last Name"}),
            'mobile': forms.TextInput(attrs={"placeholder": "Enter Mobile Number", "aria-label": "Mobile"}),
            'email': forms.TextInput(attrs={"placeholder": "Enter Email Address", "aria-label": "Email Address"}),
            'date_created': DateInput(),
            'standard': forms.TextInput(attrs={"placeholder": "Enter Standard", "aria-label": "Standard"}),
            'divison': forms.TextInput(attrs={"placeholder": "Enter Division", "aria-label": "Division"}),
            'fee_per_month': forms.TextInput(attrs={"placeholder": "Enter Fees", "aria-label": "Fees"}),


        }

        labels = {
            "fee_per_month": "Total Fees",

        }


class Student_feeForms(forms.ModelForm):

    class Meta:
        model = Student_fee
        # fields = '__all__'
        fields = ['Student', 'payment_type', 'amount', 'date']

        widgets = {
            # 'Student.first_name': forms.ModelChoiceField(label="", queryset=Student_fee.objects.all(), empty_label="Placeholder"),
            # 'Student.last_name': forms.TextInput(attrs={"placeholder": "Enter Last Name", "aria-label": "Last Name"}),
            # 'Student.first_name': floppyforms.widgets.Input(datalist=_get_all_proj_names()),
            'amount': forms.TextInput(attrs={"placeholder": "Enter Amount", "aria-label": "Amount"}),
            'date': DateInput(),
        }


class Students_feeForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Students_feeForms, self).__init__(*args, **kwargs)
        self.fields['Student'].required = False

    class Meta:
        model = Student_fee
        fields = ['Student', ]


class teachers_payForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(teachers_payForms, self).__init__(*args, **kwargs)
        self.fields['Teacher'].required = False

    class Meta:
        model = Teacher_payment
        fields = ['Teacher', ]
