from django.contrib.auth.models import User, auth
from django.template.loader import get_template
from django.shortcuts import render, redirect
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.contrib import messages
from login.forms import *
from io import BytesIO
from .models import *
import datetime


# Create your views here.


# ----------------------------- HOME PAGE ---------------------------------------


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Not Valid Credential")
            return redirect('/')

    return render(request, 'login/login.html')


# ----------------------------- REGISTRATION PAGE-----------------------------------


def register(request):
    return render(request, 'login/register.html')


# --------------------------------- Logout -----------------------------------

def logout(request):

    auth.logout(request)
    return redirect('/')


# ----------------------------- DASHBOARD PAGE ---------------------------------------


def dashboard(request):

    # Expenditure Date

    expenditure = Expenditure.objects.all()
    comp_date = datetime.date.today()
    start_date = datetime.date.today().replace(day=1)
    currnt = 0
    for x in expenditure:
        if x.Date >= start_date:
            currnt += int(x.Amount)

    # Passing Total Teacher

    totl_teacher = Teacher.objects.all().count()

    #  Checking Student Fees

    start_date = datetime.date.today().year

    fees_Recieve = Student_fee.objects.filter(date__year=start_date)
    fees_Due = Students.objects.all()
    total_amount = 0
    Due_Amount = 0
    Due_Crrnt_fee = 0
    for x in fees_Recieve:
        total_amount += x.amount

    #  Checking Student Due

    for y in fees_Due:

        Due_Crrnt_fee += y.fee_per_month

    Due_Amount = Due_Crrnt_fee - total_amount

    # ----------------------------Year Chart for Student--------------------------

    crn_years = datetime.datetime.today().year
    mon = []
    mon_amount = 0
    mon_count = 0
    month_list = set([])
    data_year = fees_Recieve.filter(date__year=crn_years).order_by('date')
    if data_year:
        for month in data_year:
            new_mon = month.date.strftime('%B')
            if new_mon not in month_list or mon_count == 0:

                mon_amount = data_year.filter(
                    date__month=month.date.month)
                amt = 0
                for amnt in mon_amount:
                    amt += amnt.amount
                new_dic = {

                    month.date.strftime('%B'):   amt
                }
                mon.append(new_dic)
                month_list.add(new_mon)
                mon_count += 1
            else:
                pass

    # ----------------------- Year Wise Expenditure Data for Graphs ----------------------

    expend_year_data = Expenditure.objects.filter(
        Date__year=crn_years).order_by('Date')
    data_dic_expend = {}
    expend_month = set()

    if expend_year_data:
        for ex_data in expend_year_data:
            month_name = ex_data.Date.strftime("%B")

            if expend_month == None or month_name not in expend_month:
                expend_month.add(month_name)
                monthly_amount = 0
                data_total_month = Expenditure.objects.filter(
                    Date__month=ex_data.Date.month)

                for total_exp_month in data_total_month:

                    monthly_amount += int(total_exp_month.Amount)

                data_dic_expend[month_name] = monthly_amount

    # ------------------------ Teacher Payment Details Chart -----------------------------

    tech_year_data = Teacher_payment.objects.filter(
        date__year=crn_years).order_by('date')
    data_dic_tech = {}
    tech_month = set()

    if tech_year_data:
        for tec_data in tech_year_data:
            month_tech_name = tec_data.date.strftime("%B")

            if tech_month == None or month_tech_name not in tech_month:
                tech_month.add(month_tech_name)
                monthly_amount = 0
                tech_total_month = Teacher_payment.objects.filter(
                    date__month=tec_data.date.month)

                for total_tech_month in tech_total_month:

                    monthly_amount += int(total_tech_month.amount)

                data_dic_tech[month_tech_name] = monthly_amount

    # ----------------------- Sending List to Templates -----------------------------------

    lst = {'currnt': currnt,
           'totl_teacher': totl_teacher, 'total_amount': total_amount, 'Due_Amount': Due_Amount, 'mon': mon, 'crn_years': crn_years, 'data_dic_expend': data_dic_expend, 'data_dic_tech': data_dic_tech}

    return render(request, 'login/dashboard.html', lst)


# ----------------------------- STUDENT PAGE ---------------------------------------


def student(request):

    Student_module = StudentsForms()

    if request.method == "POST":
        Student_module = StudentsForms(request.POST)
        if Student_module.is_valid():
            Student_module.save()
            Student_name = request.POST.get('first_name')
            messages.success(
                request, " Student  {}  Saved to Database Successfully ✔".format(Student_name))
            return redirect('student')

    student = Students.objects.all()
    stu_count = Students.objects.all().count()
    fee_under_seven = Students.objects.filter(fee_per_month__lte=10000).count()
    gte = Students.objects.filter(fee_per_month__gt=10000).count()

    lst = {'Student_module': Student_module,
           'student': student, 'stu_count': stu_count, 'fee_under_seven': fee_under_seven, 'gte': gte}
    return render(request, 'login/student.html', lst)


# ----------------------------- STUDENT UPDATE ---------------------------------------


def student_update(request, pk):

    students = Students.objects.get(id=pk)
    student = StudentsForms(instance=students)

    if request.method == "POST":
        student = StudentsForms(request.POST, instance=students)
        if student.is_valid():
            student.save()
            Student_name = request.POST.get('first_name')
            messages.success(
                request, " Student  {}  Updated Successfully ✔".format(Student_name))
            return redirect('/student')

    lst = {'student': student}

    return render(request, 'login/student_update.html', lst)

# ----------------------------- STUDENT DELETE --------------------------------------


def student_delete(request, pk):

    student = Students.objects.get(id=pk)

    if request.method == "POST":
        if student:
            student.delete()
            messages.success(
                request, "Yehhh !!!  Data Deleted Successfully ✔")
            return redirect('/student')
    dic = {'student': student}
    return render(request, 'login/stud_delete.html', dic)

# ------------------------------- Student Fees ------------------------------------


def student_fees(request):

    student = Student_fee.objects.all()
    students = Student_feeForms()
    start_date = datetime.date.today().replace(day=1)

    year = datetime.datetime.today().year

    if request.method == "POST":
        students = Student_feeForms(request.POST)
        if students.is_valid():

            students.save()

            # For Successfull Message
            Student_data = request.POST.get('Student')
            Student_name = Students.objects.get(id=Student_data)
            amount_pay = request.POST.get('amount')
            messages.success(
                request, " Student {} Paid ₹ {} to Us , Data Saved Successfully ✔".format(Student_name.first_name, amount_pay))
            return redirect('/student_fees')

    crnt_mon_fee = 0
    for x in student:
        if x.date >= start_date:
            crnt_mon_fee += x.amount
    studentss = Students.objects.all()
    crnt_mon_total = 0
    for x in studentss:
        crnt_mon_total += x.fee_per_month

    crnt_year_recieved = 0
    for rec in student:
        crnt_year_recieved += rec.amount

    dic = {'student': student, 'students': students,
           'crnt_mon_fee': crnt_mon_fee, 'crnt_mon_total': crnt_mon_total, 'start_date': start_date, 'crnt_year_recieved': crnt_year_recieved}

    return render(request, 'login/student_fees.html', dic)


# ------------------------------- Student Fees Update ------------------------------------

def studentfee_update(request, pk):

    student = Student_fee.objects.get(id=pk)
    students = Student_feeForms(instance=student)
    print(students)
    if request.method == "POST":
        students = Student_feeForms(request.POST, instance=student)
        if students.is_valid():
            students.save()
            Student_data = request.POST.get('Student')
            Student_name = Students.objects.get(id=Student_data)
            messages.success(
                request, "Fee Recipt of {}  Updated Successfully ✔".format(Student_name.first_name))
            return redirect('/student_fees')

    dic = {'students': students}
    return render(request, 'login/studentfee_update.html', dic)

# --------------------------------- STUDENT FEE DELETE ----------------------------


def studentfee_delete(request, pk):

    student = Student_fee.objects.get(id=pk)

    if request.method == "POST":
        if student:
            student.delete()
            messages.success(
                request, "Yehhh!!! Data Deleted Successfully ✔")
            return redirect('/student_fees')

    dic = {'student': student}

    return render(request, 'login/studentfee_delete.html', dic)

# ----------------------------- TEACHER PAGE ---------------------------------------


def teacher(request):

    teacher_module = TeacherForm()

    if request.method == "POST":
        teacher_module = TeacherForm(request.POST)
        if teacher_module.is_valid():
            teacher_module.save()
            messages.success(
                request, "Yehhh !!! Prof. {} Added to the Database 😊".format(
                    request.POST.get('fname')))
            return redirect('/teacher')
        else:
            pass

    teacher = Teacher.objects.all()
    active = Teacher.objects.filter(active="Active").count()
    inactive = Teacher.objects.filter(active="Not Active").count()
    total = teacher.count()

    lst = {'teacher': teacher, 'active': active,
           'inactive': inactive, 'total': total, 'teacher_module': teacher_module}

    return render(request, 'login/teacher.html', lst)

# ----------------------------- Teacher Update ------------------------------------


def teacher_update(request, pk):

    get_teacher = Teacher.objects.get(id=pk)
    teachers = TeacherForm(instance=get_teacher)

    if request.method == 'POST':
        teachers = TeacherForm(request.POST, instance=get_teacher)
        if teachers.is_valid():
            teachers.save()
            messages.success(
                request, "Yehhh !!! Prof. {} Data Updated Successfully ✔".format(
                    request.POST.get('fname')))
            return redirect('/teacher')

    lst = {'teachers': teachers}

    return render(request, 'login/teacher_update.html', lst)


# ---------------------------- Teacher Delete -----------------------------------------


def teacher_delet(request, pk):

    teacher = Teacher.objects.get(id=pk)
    if request.method == "POST":
        teacher.delete()
        messages.success(
            request, "Yehhh !!!  Data Deleted Successfully ✔")
        return redirect('/teacher')

    lst = {'teacher': teacher}

    return render(request, 'login/teacher_delete.html', lst)


# ------------------------------- Teacher Payment Add -----------------------------------


def teacher_pay(request):

    start_date = datetime.date.today().replace(day=1)
    teach_pay = Teacher_payment.objects.all()

    teacher_feild = Teacher_paymentForms()

    if request.method == "POST":
        teacher_feild = Teacher_paymentForms(request.POST)
        if teacher_feild.is_valid():

            teacher_feild.save()
            Teacher_data = request.POST.get('Teacher')
            Teacher_name = Teacher.objects.get(id=Teacher_data)
            amount_pay = request.POST.get('amount')
            messages.success(
                request, "You Paid ₹ {} to Prof. {} , Data Saved Successfully ✔".format(amount_pay, Teacher_name.fname))
            return redirect('/teacher_pay')

    teacher_cash = Teacher_payment.objects.filter(payment_type='Cash')
    cash_total = 0
    for cash in teacher_cash:
        if cash.date >= start_date:
            cash_total += cash.amount

    teacher_cheque = Teacher_payment.objects.filter(payment_type='Cheque')
    cheque_total = 0
    for cheque in teacher_cheque:
        if cheque.date >= start_date:
            cheque_total += cheque.amount

    lst = {'teach_pay': teach_pay,
           'teacher_feild': teacher_feild, 'cash_total': cash_total, 'cheque_total': cheque_total}

    return render(request, 'login/add_tech_payment.html', lst)

# -------------------------------- Teacher Payment Update - ----------------------


def teacher_pay_update(request, pk):

    teacher_pay = Teacher_payment.objects.get(id=pk)
    teachers = Teacher_paymentForms(instance=teacher_pay)

    if request.method == "POST":
        teachers = Teacher_paymentForms(request.POST, instance=teacher_pay)
        if teachers.is_valid():
            teachers.save()
            Teacher_data = request.POST.get('Teacher')
            Teacher_name = Teacher.objects.get(id=Teacher_data)
            messages.success(
                request, " Prof. {}  Updated Successfully ✔".format(Teacher_name.fname))
            return redirect('/teacher_pay')

    lst = {'teachers': teachers}
    return render(request, 'login/teacher_pay_update.html', lst)


# -------------------------------- Teacher Payment Delete ----------------------


def teacher_pay_delete(request, pk):

    teachers_pay = Teacher_payment.objects.get(id=pk)

    if request.method == "POST":
        teachers_pay.delete()
        messages.success(request, "Yehhh !!!  Data Deleted Successfully ✔")
        return redirect('/teacher_pay')

    lst = {'teachers_pay': teachers_pay}
    return render(request, 'login/teacher_pay_delete.html', lst)


# ----------------------------- EXPENSITURE PAGE ---------------------------------------


def expend(request):

    expends = ExpenditureForm()

    if request.method == "POST":
        expends = ExpenditureForm(request.POST)
        if expends.is_valid():
            expends.save()
            messages.success(request, "Data Save Successfully 😊")
            return redirect('expend')
        else:
            pass

    expenditure = Expenditure.objects.all()
    comp_date = datetime.date.today()
    start_date = datetime.date.today().replace(day=1)
    next_to_next_month = comp_date.month-2
    currnt = 0
    pre_mon = 0
    total_expend = 0
    for x in expenditure:
        if x.Date >= start_date:
            currnt += int(x.Amount)
        else:
            if x.Date.month > next_to_next_month:

                pre_mon += int(x.Amount)
            else:
                total_expend += int(x.Amount)

    lst = {'expenditure': expenditure, 'start_date': start_date,
           'currnt': currnt, 'pre_mon': pre_mon, 'expends': expends, 'total_expend': total_expend}
    return render(request, 'login/expend.html', lst)


def expend_update(request, pk):

    expend = Expenditure.objects.get(id=pk)
    expends = ExpenditureForm(instance=expend)

    if request.method == "POST":
        expends = ExpenditureForm(request.POST, instance=expend)
        if expends.is_valid():
            expends.save()
            messages.success(request, "Yehhh !!! Data Updated Successfully 😊")
            return redirect('expend')
        else:
            messages.error(request, "Opps!!! Somthing Went Wrong 😕")
            return redirect('expend')

    return render(request, 'login/update.html', {'expends': expends})


def delete_update(request, pk):

    expend = Expenditure.objects.get(id=pk)

    if request.method == "POST":
        if expend:

            expend.delete()
            messages.success(request, "Yehhh!!! Data has been Deleted ✔")
            return redirect('/expend')
        else:

            messages.error(request, "Oppps!!! Cant Delete Data 😕")
            return redirect('/expend')

    lst = {'expend': expend}

    return render(request, "login/delete.html", lst)


# ------------------------- Reports ------------------------------

def report(request):

    return render(request, 'login/reports_page.html')

# ----------------------- All Student Reports -----------------------------


def student_report(request):

    students = Students_feeForms()
    id = 0
    frm = None
    to = None
    if request.POST.get('from') != "" and request.POST.get('to') != "" and request.POST.get('Student') == "":
        try:

            frm = request.POST.get('from')
            to = request.POST.get('to')
            data_by_date = Student_fee.objects.filter(
                date__gte=frm, date__lte=to)

        except:
            data_by_date = ""

    elif request.POST.get('from') != "" and request.POST.get('to') != "" and request.POST.get('Student') != "":
        try:
            frm = request.POST.get('from')
            to = request.POST.get('to')
            id = request.POST.get('Student')

            data_by_date = Student_fee.objects.filter(
                date__gte=frm, date__lte=to, Student=id)

        except:

            data_by_date = None

    else:
        data_by_date = None

    if id != 0:
        lst = {'data_by_date': data_by_date,
               'students': students, 'id': id, "frm": frm, "to": to}

    elif frm is not None and to is not None:
        lst = {'data_by_date': data_by_date,
               'students': students, "frm": frm, "to": to}

    else:
        lst = {'data_by_date': data_by_date, 'students': students}

    return render(request, "login/student_report.html", lst)


# ----------------------- All Teachers Report -----------------------------------


def teachers_report(request):

    teachers = teachers_payForms()
    id = 0
    frm = None
    to = None
    if request.POST.get('from') != "" and request.POST.get('to') != "" and request.POST.get('Teacher') == "":
        try:

            frm = request.POST.get('from')
            to = request.POST.get('to')
            data_by_date = Teacher_payment.objects.filter(
                date__gte=frm, date__lte=to)

        except:
            data_by_date = ""

    elif request.POST.get('from') != "" and request.POST.get('to') != "" and request.POST.get('Teacher') != "":
        try:
            frm = request.POST.get('from')
            to = request.POST.get('to')
            id = request.POST.get('Teacher')

            data_by_date = Teacher_payment.objects.filter(
                date__gte=frm, date__lte=to, Teacher=id)

        except:

            data_by_date = None

    else:
        data_by_date = None

    if id != 0:
        lst = {'data_by_date': data_by_date,
               'teachers': teachers, 'id': id, "frm": frm, "to": to}

    elif frm is not None and to is not None:
        lst = {'data_by_date': data_by_date,
               'teachers': teachers, "frm": frm, "to": to}

    else:
        lst = {'data_by_date': data_by_date, 'teachers': teachers}

    return render(request, "login/teachers_report.html", lst)


# -----------------------  Html 2 Pdf Function of Single Expenditure -----------------------------


def dataprint(request, pk):

    data = Expenditure.objects.get(id=pk)
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date}
    templates = get_template('login/pdf.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")
    return render(request, 'login/pdf.html', send_data)


# ------------------------ Html 2 Pdf Data Print Student Fee --------------------


def dataprintstudent(request, pk):

    data = Student_fee.objects.get(id=pk)
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date}
    templates = get_template('login/studentfeepdf.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")
    return render(request, 'login/studentfeepdf.html', send_data)


# ------------------------ Html 2 Pdf Data Print Teacher Fee --------------------


def dataprintteach(request, pk):

    data = Teacher_payment.objects.get(id=pk)
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date}
    templates = get_template('login/teachpaypdf.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")
    return render(request, 'login/teachpaypdf.html', send_data)


# ----------------------- All Expenditure Report -----------------------------------


def expenditure_report(request):

    frm = None
    to = None
    if request.POST.get('from') != "" and request.POST.get('to') != "":
        try:

            frm = request.POST.get('from')
            to = request.POST.get('to')
            data_by_date = Expenditure.objects.filter(
                Date__gte=frm, Date__lte=to)

        except:
            data_by_date = ""

    else:
        data_by_date = None

    if frm is not None and to is not None:
        lst = {'data_by_date': data_by_date, "frm": frm, "to": to}

    else:
        lst = {'data_by_date': data_by_date}

    return render(request, "login/expenditure_report.html", lst)


# -----------------------  Html 2 Pdf Function of Single Expenditure -----------------------------


def dataprint(request, pk):

    data = Expenditure.objects.get(id=pk)
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date}
    templates = get_template('login/pdf.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")
    return render(request, 'login/pdf.html', send_data)


# -----------------------  Html 2 Pdf Function of Student by date and Name-----------------------------


def std_rpt(request, frm, to, id=""):

    try:

        if id != "" and id is not None:
            data = Student_fee.objects.filter(
                date__gte=frm, date__lte=to, Student=id)

        else:
            data = Student_fee.objects.filter(
                date__gte=frm, date__lte=to)

    except:

        print("Error in Export Student Fees")

    total = 0

    for x in data:
        total += x.amount

    # ----------- Time And Date -------------------
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    frmm = datetime.datetime.strptime(frm, '%Y-%m-%d')
    too = datetime.datetime.strptime(to, '%Y-%m-%d')
    fromm = frmm.strftime("%d-%B-%Y")
    tooo = too.strftime("%d-%B-%Y")

    # ------------- Dictionary for Templates ----------------
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date, 'fromm': fromm, 'tooo': tooo, 'total': total}
    templates = get_template('login/student_fees_report.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")
    return render(request, 'login/student_fees_report.html', send_data)


# -----------------------  Html 2 Pdf Function of Teachers by date and Name-----------------------------


def teach_rpt(request, frm, to, id=""):

    try:

        if id != "" and id is not None:
            data = Teacher_payment.objects.filter(
                date__gte=frm, date__lte=to, Teacher=id)

        else:
            data = Teacher_payment.objects.filter(
                date__gte=frm, date__lte=to)

    except:

        print("Error in Export Student Fees")

    total = 0

    for x in data:
        total += x.amount

    # ----------- Time And Date -------------------
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    frmm = datetime.datetime.strptime(frm, '%Y-%m-%d')
    too = datetime.datetime.strptime(to, '%Y-%m-%d')
    fromm = frmm.strftime("%d-%B-%Y")
    tooo = too.strftime("%d-%B-%Y")

    # ------------- Dictionary for Templates ----------------
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date, 'fromm': fromm, 'tooo': tooo, 'total': total}
    templates = get_template('login/teacher_pay_report.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")
    return render(request, 'login/teacher_pay_report.html', send_data)


# -----------------------  Html 2 Pdf Function of Expenditure by date and Name-----------------------------


def expend_date(request, frm, to):

    try:
        data = Expenditure.objects.filter(
            Date__gte=frm, Date__lte=to)

    except:
        data = None
        print("Error in Export Student Fees")

    total = 0

    for x in data:
        total += int(x.Amount)

    # ----------- Time And Date -------------------
    now = datetime.datetime.now()
    hr = now.strftime("%H")
    crrnt_date = now.strftime("%d-%B-%Y")
    current_time = now.strftime("%H:%M:%S")
    frmm = datetime.datetime.strptime(frm, '%Y-%m-%d')
    too = datetime.datetime.strptime(to, '%Y-%m-%d')
    fromm = frmm.strftime("%d-%B-%Y")
    tooo = too.strftime("%d-%B-%Y")

    # ------------- Dictionary for Templates ----------------
    send_data = {'data': data, 'current_time': current_time,
                 "hr": hr, "crrnt_date": crrnt_date, 'fromm': fromm, 'tooo': tooo, 'total': total}
    templates = get_template('login/expend_report.html')
    data_p = templates.render(send_data)
    respons = BytesIO()

    # converting html to pdf

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), respons)

    if not pdfPage.err:
        return HttpResponse(respons.getvalue(), content_type='application/pdf')
    else:
        print("Error")

    return render(request, 'login/expend_report.html', send_data)
