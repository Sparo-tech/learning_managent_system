from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, User, Teacher,Class_level,Course
 

class StudentForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        self.stream = kwargs.pop('stream')
        super(StudentForm,self).__init__(*args,**kwargs)
        
        
        
        if Class_level.objects.all().exists():
            self.fields['class_level'].queryset = Class_level.objects.filter(stream=self.stream).order_by('name')
            
    email = forms.EmailField(label='Email', required=True)
    
    first_name = forms.CharField(
        label='First Name', max_length=250, required=True)
    
    last_name = forms.CharField(
        label='Last Name', max_length=250, required=True)
    
    
    class_level = forms.ModelChoiceField(queryset=None )
    
    
    roll_no =forms.IntegerField(label='Roll No.', required=True, min_value=1, max_value=500)
    
    student_id = forms.CharField(label='Student ID', max_length=50, required=True, min_length=4)
    
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        student = Student.objects.create(
            user=user,
           class_level= self.cleaned_data['class_level'],
            roll_no = self.cleaned_data['roll_no'],
            student_id = self.cleaned_data['student_id'],   
            )
        student.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        class_level = cleaned_data.get('class_level')
        roll_no = self.cleaned_data.get('roll_no')
        student_id = self.cleaned_data.get('student_id')
        email = self.cleaned_data.get('email')
        
        # Class and Roll No. Unique Constraint Validation
        if Student.objects.filter(class_level = class_level).filter(roll_no=roll_no).exists():
           
            raise forms.ValidationError('Student with Roll No. already exists.')
        
        # Student id validation
        if Student.objects.filter(student_id=student_id).exists():
           
            raise forms.ValidationError('Student with Student ID already exists.')
        
        # Email Validations
        if User.objects.filter(email=email).exists():
           
            raise forms.ValidationError('User with Email already exists.')


class TeacherForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        self.stream = kwargs.pop('stream')
      
        super(TeacherForm,self).__init__(*args,**kwargs)
    
    
    

    email = forms.EmailField(label='Email', required=True)
    
    first_name = forms.CharField(
        label='First Name', max_length=250, required=True)
    
    last_name = forms.CharField(
        label='Last Name', max_length=250, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        teacher = Teacher.objects.create(
            user=user,
            stream = self.stream   
            )
        teacher.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')

        # Email Validations
        if User.objects.filter(email=email).exists():
            print("Email exists")
            raise forms.ValidationError('User with Email already exists.')
                