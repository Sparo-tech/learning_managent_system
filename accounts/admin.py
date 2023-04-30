from django.contrib import admin
from .models import Assignment,Course,Resource,Stream,Student,Lecture_session,User,Teacher,Class_level

# Register your models here.

admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(Stream)
admin.site.register(Student)
admin.site.register(Lecture_session)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Class_level)