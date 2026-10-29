from django.contrib import admin
from .models import Student, Teacher, SchoolClass, Subject

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(SchoolClass)
admin.site.register(Subject)