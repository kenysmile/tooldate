from lib2to3.pytree import convert
from logging import exception
from socket import timeout
from django.shortcuts import render, redirect
from urllib3 import HTTPResponse
from .forms import TooldateForm
from .models import ToolDate, ToolDateDetails
from datetime import date, datetime, timedelta

def home(request):
    return render(request, 'tool/home.html', {})

def tool_date_details(request, pk):
    tool_date_details = ToolDateDetails.objects.filter(tool_date=pk)
    return render(request, 'tool/tool_date_details.html', {'tool_date_details': tool_date_details})

def simple_function(request):
    print('ok')
    return HTTPResponse("return this string")
def create_tool_date(request):
    if request.method == 'GET':
        form = TooldateForm()
        return render(request, 'tool/home.html', {'form': form})
    else:
        set_hours_work = 8
        form = TooldateForm(request.POST)
        lst_extra_hours = request.POST['lst_extra_hours']
        start_date = request.POST['startdate']
        if request.POST['sethourswork']:
            set_hours_work = request.POST['sethourswork']
        tool_date = ToolDate.objects.create(lst_extra_hours=lst_extra_hours, start_date=start_date)
        convert_start_date = datetime.strptime(tool_date.start_date, '%Y/%m/%d')
        start_date = convert_start_date
        time_out = 0
        for extra_hours in str(tool_date.lst_extra_hours).split('-'):
            extra_hours = str(extra_hours).replace(",",".")
            if float(extra_hours) < float(set_hours_work):
                end_date = start_date
                time_out_choice = float(extra_hours) + time_out
                if time_out_choice >= float(set_hours_work):
                    days = float(time_out_choice)//8
                    time_out_choice = (float(time_out_choice) % float(set_hours_work))
                    end_date = start_date  + timedelta(days=days)
                else:
                    time_out_choice = 0
            else:
                days = float(extra_hours)//8
                time_out_choice = (float(extra_hours) % float(set_hours_work)) + time_out
                end_date = start_date  + timedelta(days=days)
            weekday = start_date.weekday()
            if weekday == 4:

                end_date += timedelta(days=2)
            tool_date_details = ToolDateDetails.objects.create(tool_date=tool_date, name=tool_date.pk, 
                                                   start_date=start_date, end_date=end_date,
                                                   extra_hours=extra_hours, time_out=time_out_choice,
                                                   weekday=weekday    
                                                            )
            time_out = time_out_choice
            start_date = end_date   
              
        return redirect('tool_date_details', pk=tool_date.pk)
