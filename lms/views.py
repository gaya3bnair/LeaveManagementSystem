from urllib.request import Request
from django.http import HttpResponseRedirect
from .models import Members, Leave
from django.shortcuts import render
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMultiAlternatives
from leave_management_system.settings import EMAIL_HOST_USER
from django.contrib import messages
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime
def landing_page(request):
    return render(request, 'dashboard/landingpage.html')
def members_list(request):
    members = Members.objects.all()
    value = False
    val = False


    for det in members:
        uname = det.username
        if uname == request.user.username:
            if det.year == 2020 or det.year == 2021:
                print(det.year)
                value = True
    return render(request, 'dashboard/members_list.html', {'members': members, "value": value, "val": val})





def leave_request(request):
    return render(request, 'dashboard/leave_request.html')

def user(request, id):
    user = get_object_or_404(Members, id=id)
    members = Members.objects.all()
    leave= Leave.objects.all()
    context = {'members': members, 'id': id, 'leave': leave}
    return render(request, 'dashboard/user.html', context)


def approve(request):
    requests = Leave.objects.all()
    members = Members.objects.all()
    for member in members:
        if request.user.username == member.username:
            mentees = member.mentee
    mentee_list = mentees.split(", ")
    print(mentee_list)
    dict = {}
    for mem in members:
        for mentee_name in mentee_list:
            if mem.first_name == mentee_name:
                for req in requests:
                    if mem.user_id == req.user_id:
                        dict[mentee_name] = req.user_id
    print(dict)

  
 
    

    return render(request, 'dashboard/approve.html', {'members': members, 'requests': requests, 'dict': dict})


