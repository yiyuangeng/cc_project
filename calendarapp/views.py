

from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from .utils import get_current_userid
from django.db.models import Q


from .models import *
from .utils import Calendar
from .forms import EventForm, EventMemberForm


def get_date(day):
    if day:
        time_list = day.split('-')
        year = int(time_list[0])
        month = int(time_list[1])
        day = 1
        return date(year, month, day)
    else:
        return datetime.today()

def get_last_month(a):
    first_day = a.replace(day=1)  #the first day of current month
    
    last_month = first_day + timedelta(days=-1) 
    month = 'month=' + str(last_month.year) + '-' + str(last_month.month)
    return month

def get_next_month(a):
    days_in_month = calendar.monthrange(a.year, a.month)[1]  #the last day of current month
    last_day= a.replace(day=days_in_month)
    next_month = last_day + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'signin'
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['last_month'] = get_last_month(d)
        context['next_month'] = get_next_month(d)
        return context
    


def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        desc = form.cleaned_data['desc']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            desc=desc,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'event.html', {'form': form})




def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'event_detail.html', context)


def add_eventmember(request, event_id):
    forms = EventMemberForm()
    if request.method == 'POST':
        forms = EventMemberForm(request.POST)
        if forms.is_valid():
            # try:
                # member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            user = forms.cleaned_data['user']
            user_id = request.POST['user']

            print(user)
            print(user_id)
            if EventMember.objects.filter(Q(user_id=user_id) & Q(event_id=event_id)):
                messages.success(request, 'Cannot add duplicate user')
                # return redirect('calendarapp:calendar')
            else:
                EventMember.objects.create(event=event,user=user)
                messages.success(request, 'Add user sucessfully')
            return redirect('calendarapp:calendar')
            
    context = {
        'form': forms
    }
    return render(request, 'add_member.html', context)


class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'desc', 'start_time', 'end_time']
    template_name = 'event.html'


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'member_delete.html'
    success_url = reverse_lazy('calendarapp:calendar')


class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'event_delete.html'
    success_url = reverse_lazy('calendarapp:calendar')


def searchEvent(request):
    if request.method == 'POST':
        title = request.POST['title']
        user_id=get_current_userid()
        try:
            event = Event.objects.get(user_id = user_id, title=title)
            eventmember = EventMember.objects.filter(event=event)
            context = {
                'event': event,
                'eventmember': eventmember
            }
            return render(request, 'search_event.html', context)
        except:
            messages.success(request, 'Nothing to match.')
            return redirect('calendarapp:calendar')
    return redirect('calendarapp:calendar')
