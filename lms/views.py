from urllib.request import Request
from django.http import HttpResponseRedirect
from .models import Members, Leave
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMultiAlternatives
from leave_management_system.settings import EMAIL_HOST_USER
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.template import RequestContext


def landing_page(request):
    return render(request, 'dashboard/landingpage.html')

def members_list(request):
    members = Members.objects.all()
    value = any(member.year in [2020, 2021] for member in members if member.username == request.user.username)
    return render(request, 'dashboard/members_list.html', {'members': members, "value": value})


def leave_request(request):
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        reason = request.POST.get('reason')
        mem = Members.objects.filter(username=request.user.username)
        email = mem.values_list('mentoremail', flat=True).first()
        maillist = email.split(", ")

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Check if end date comes before start date
            if end_date < start_date:
                messages.error(request, "End date cannot be before the start date.")
                return render(request, 'dashboard/leave_request.html')

            # Check if start date is before the current day
            if start_date < timezone.now().date():
                messages.error(request, "Start date cannot be a date before the current day.")
                return render(request, 'dashboard/leave_request.html')

            valid = (end_date - start_date).days <= 20
            if valid:
                msg = EmailMultiAlternatives(
                    'Leave request', f'Start Date: {start_date}\nEnd Date: {end_date}\nReason: {reason}', EMAIL_HOST_USER, maillist)
                if msg.send():
                    messages.success(request, 'Leave request submitted successfully.')
                    for member in mem:
                        Leave.objects.create(start_date=start_date, end_date=end_date, reason=reason, user_id=member.user_id)
                else:
                    messages.error(request, 'Failed to send leave request email.')
            else:
                messages.error(request, "Please mention a valid time period within 20 days.")
        except Exception as e:
            messages.error(request, f"Leave request unsuccessful: {e}")

    return render(request, 'dashboard/leave_request.html')


def user(request, id):
    user = get_object_or_404(Members, id=id)
    members = Members.objects.all()
    leave = Leave.objects.all()
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST.get('start-date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST.get('end-date'), '%Y-%m-%d').date()
        user_id = user.user_id
        n_days = sum((min(end, end_date) - max(start, start_date)).days for start, end in ((req.start_date, req.end_date) for req in leave if req.user_id == user_id))
        n_dayst = (end_date - start_date).days
        days_present = n_dayst - n_days
        context = {'members': members, 'id': id, 'leave': leave, 'dict': {'n_days': n_days, 'n_dayst': n_dayst, 'days_present': days_present}}
        return render(request, 'dashboard/user.html', context)
    context = {'members': members, 'id': id, 'leave': leave}
    return render(request, 'dashboard/user.html', context)


def approve(request):
    requests = Leave.objects.all()
    members = Members.objects.all()
    for member in members:
        if request.user.username == member.username:
            mentees = member.mentee
    mentee_list = mentees.split(", ")
    dict = {}
    for mem in members:
        for mentee_name in mentee_list:
            if mem.first_name == mentee_name:
                for req in requests:
                    if mem.user_id == req.user_id:
                        dict[mentee_name] = req.user_id

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        reqe = get_object_or_404(requests, id=request_id)
        user_id = reqe.user_id
        user_mail = get_object_or_404(members, user_id=user_id).email
        maillist = [user_mail]

        if 'approved' in request.POST:
            reqe.status = "approved"
            reqe.save(update_fields=['status'])
            msg_content = f'Your leave request from {reqe.start_date} to {reqe.end_date} has been approved.'
        elif 'rejected' in request.POST:
            reqe.status = "rejected"
            reqe.save(update_fields=['status'])
            msg_content = f'Your leave request from {reqe.start_date} to {reqe.end_date} has been rejected.'

        msg = EmailMultiAlternatives('Leave request status', msg_content, EMAIL_HOST_USER, maillist)
        if msg.send():
            messages.success(request, 'Leave request status email sent successfully.')
        else:
            messages.error(request, 'Failed to send leave request status email.')

        # Pass the message content to the template
        context = {'members': members, 'requests': requests, 'dict': dict, 'msg_content': msg_content}
        return render(request, 'dashboard/approve.html', context)

    return render(request, 'dashboard/approve.html', {'members': members, 'requests': requests, 'dict': dict})
