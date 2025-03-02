from django.shortcuts import render, redirect
from .models import AboutPage, ContactPage, Student, Notice, Teacher

def home(request):
    public_notices = Notice.objects.filter(isPublic=True)
    data = {"public_notices": public_notices}
    return render(request, 'home.html', data)

def about(request):
    about_text = AboutPage.objects.all()
    data = {"aboutDetails": about_text}
    return render(request, 'about.html', data)

def contact(request):
    contact_text = ContactPage.objects.all()
    data = {"contactDetails": contact_text}
    return render(request, 'contact.html', data)

def adminPanel(request):
    if 'admin_user' in request.session:
        all_students = Student.objects.all()
        all_teachers = Teacher.objects.all()
        data = {'students': all_students, 'teachers': all_teachers}
        return render(request, 'admin/admin_panel.html', data)
    return redirect('admin_login')

def adminLogin(request):
    if request.method == 'POST':
        admin_email = request.POST['email']
        admin_pwd = request.POST['pwd']

        if admin_email == "admin@gmail.com" and admin_pwd == "admin@123":
            request.session['admin_user'] = admin_email
            return redirect('admin_panel')
        return redirect('admin_login')

    return render(request, 'admin/admin_login.html')

def adminLogout(request):
    del request.session['admin_user']
    return redirect('admin_login')

def adminAbout(request):
    about_details = AboutPage.objects.all()
    data = {"aboutDetails": about_details}
    return render(request, 'admin/admin_about.html', data)

def updateAbout(request, id):
    if request.method == 'POST':
        about_text = request.POST['text']
        about_obj = AboutPage.objects.get(id=id)
        about_obj.about = about_text
        about_obj.save()
    return redirect('admin_about')

def adminContact(request):
    contact_details = ContactPage.objects.all()
    data = {"contactDetails": contact_details} 
    return render(request, 'admin/admin_contact.html', data)

def updateContact(request, id):
    if request.method == 'POST':
        contact_obj = ContactPage.objects.get(id=id)
        contact_obj.address = request.POST['address']
        contact_obj.email = request.POST['email']
        contact_obj.contact_num = request.POST['contact']
        contact_obj.save()
    return redirect('admin_contact')

def addStudent(request):
    if request.method == 'POST':
        student_data = {
            'full_name': request.POST['full_name'],
            'father_name': request.POST['f_name'],
            'mother_name': request.POST['m_name'],
            'gender': request.POST['gender'],
            'address': request.POST['address'],
            'city': request.POST['city'],
            'email': request.POST['stu_email'],
            'contact_num': request.POST['contact_number'],
            'date_of_birth': request.POST['dob'],
            'course': request.POST['course'],
            'stu_id': request.POST['stu_id'],
            'user_name': request.POST['stu_user_name'],
            'password': request.POST['stu_pwd']
        }
        Student.objects.create(**student_data)
    return render(request, 'admin/new_student.html')

def manageStudent(request):
    all_students = Student.objects.all()
    data = {"students": all_students}
    return render(request, 'admin/manage_students.html', data)

def updateStudent(request, id):
    student_obj = Student.objects.get(id=id)
    if request.method == 'POST':
        for field in ['full_name', 'father_name', 'mother_name', 'gender', 'address', 'city', 'email', 'contact_num', 'date_of_birth', 'course', 'stu_id', 'user_name', 'password']:
            setattr(student_obj, field, request.POST.get(field, getattr(student_obj, field)))
        student_obj.save()
    return redirect('manage_students')

def deleteStudent(request, id):
    if 'admin_user' in request.session:
        Student.objects.filter(id=id).delete()
    return redirect('manage_students')

def addNotice(request):
    if request.method == 'POST':
        notice_data = {
            'title': request.POST['notice_title'],
            'content': request.POST['notice_content'],
            'isPublic': request.POST['notice_status']
        }
        Notice.objects.create(**notice_data)
    return render(request, "admin/admin_notice.html")

def manageNotices(request):
    all_notices = Notice.objects.all()
    data = {'notices': all_notices}
    return render(request, 'admin/manage_notices.html', data)

def deleteNotice(request, id):
    if 'admin_user' in request.session:
        Notice.objects.filter(id=id).delete()
    return redirect('manage_notices')

def updateNotice(request, id):
    if request.method == 'POST':
        notice_obj = Notice.objects.get(id=id)
        notice_obj.title = request.POST['title']
        notice_obj.content = request.POST['content']
        notice_obj.isPublic = request.POST['status']
        notice_obj.save()
    return redirect('manage_notices')

def addTeacher(request):
    if request.method == 'POST':
        teacher_data = {
            'full_name': request.POST['full_name'],
            'gender': request.POST['gender'],
            'email': request.POST['email'],
            'contact_num': request.POST['contact_number'],
            'qualification': request.POST['qualification']
        }
        Teacher.objects.create(**teacher_data)
    return render(request, 'admin/add_teacher.html')

def manageTeachers(request):
    all_teachers = Teacher.objects.all()
    data = {"teachers": all_teachers}
    return render(request, 'admin/manage_teachers.html', data)

def deleteTeacher(request, id):
    Teacher.objects.filter(id=id).delete()
    return redirect('manage_teachers')

def studentLogin(request):
    if 'student_user' not in request.session:
        if request.method == "POST":
            user_name = request.POST['userName']
            student_pwd = request.POST['stuPwd']
            if Student.objects.filter(user_name=user_name, password=student_pwd).exists():
                request.session['student_user'] = user_name
                return redirect('student_dashboard')
        return render(request, 'student/student_login.html')
    return redirect('student_dashboard')

def studentDashboard(request):
    if 'student_user' in request.session:
        student = Student.objects.get(user_name=request.session['student_user'])
        data = {"student": student}
        return render(request, 'student/student_dashboard.html', data)
    return redirect('student_login')

def studentLogout(request):
    del request.session['student_user']
    return redirect('student_login')

def updateFaculty(request, id):
    if request.method == 'POST':
        teacher_obj = Teacher.objects.get(id=id)
        for field in ['full_name', 'email', 'contact_num', 'gender', 'qualification']:
            setattr(teacher_obj, field, request.POST[field])
        teacher_obj.save()
    return redirect('manage_teachers')

def viewNotices(request):
    if 'student_user' in request.session:
        student_notices = Notice.objects.filter(isPublic=False)
        data = {"notices": student_notices}
        return render(request, 'student/view_notices.html', data)
    return redirect('student_login')

def studentSettings(request):
    if 'student_user' in request.session:
        student_obj = Student.objects.get(user_name=request.session['student_user'])
        data = {'student': student_obj}
        if request.method == 'POST':
            current_pwd = request.POST['current_pwd']
            new_pwd = request.POST['new_pwd']
            student_obj.password = new_pwd
            student_obj.save()
            return redirect('student_dashboard')
        return render(request, "student/student_settings.html", data)
    return redirect('student_login')

from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('admin_panel/dashboard', adminPanel, name="admin_panel"),
    path('admin_panel/login/', adminLogin, name="admin_login"),
    path('admin_panel/logout/', adminLogout, name="admin_logout"),
    path('student/login/', studentLogin, name="student_login"),
    path('admin_panel/add_student/', addStudent, name="add_student"),
    path('admin_panel/about/', adminAbout, name="admin_about"),
    path('admin_panel/update_about/<str:id>/', updateAbout, name="update_about"),
    path('admin_panel/contact/', adminContact, name="admin_contact"),
    path('admin_panel/update_contact/<str:id>/', updateContact, name="update_contact"),
    path('admin_panel/manage_students/', manageStudent, name="manage_students"),
    path('admin_panel/update_student/<str:id>/', updateStudent, name="update_student"),
    path('admin_panel/delete_student/<str:id>/', deleteStudent, name="delete_student"),
    path('admin_panel/add_notice/', addNotice, name="add_notice"),
    path('admin_panel/manage_notices/', manageNotices, name="manage_notices"),
    path('admin_panel/delete_notice/<str:id>/', deleteNotice, name="delete_notice"),
    path('admin_panel/update_notice/<str:id>/', updateNotice, name="update_notice"),
    path('admin_panel/add_teacher/', addTeacher, name="add_teacher"),
    path('admin_panel/manage_teacher/', manageTeachers, name="manage_teachers"),
    path('admin_panel/delete_teacher/<str:id>/', deleteTeacher, name="delete_teacher"),
    path('student/dashboard/', studentDashboard, name="student_dashboard"),
    path('student/logout/', studentLogout, name="student_logout"),
    path('student/update_teacher/<str:id>/', updateFaculty, name="update_teacher"),
    path('student/view_notices/', viewNotices, name="view_notices"),
    path('student/student_settings/', studentSettings, name="student_settings")
]
