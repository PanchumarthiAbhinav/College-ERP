from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import Dept, Class, Student, Attendance, Course, Teacher, Assign, AttendanceTotal, time_slots, \
    DAYS_OF_WEEK, AssignTime, AttendanceClass, StudentCourse, Marks, MarksClass
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()

# Create your views here.

# ... (rest of the views.py code remains unchanged) ...

@login_required()
def average_marks_percentage(request, subject_id):
    if not request.user.is_teacher:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        subject = Course.objects.get(id=subject_id)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

    marks = Marks.objects.filter(course=subject).aggregate(Avg('marks1'))
    average_marks = marks['marks1__avg']

    if average_marks is None:
        return JsonResponse({'message': 'No marks available for this subject'}, status=200)

    average_percentage = (average_marks / subject.max_marks) * 100
    message = 'above average' if average_percentage >= 50 else 'below average'

    return JsonResponse({'average_percentage': average_percentage, 'message': message}, status=200)
