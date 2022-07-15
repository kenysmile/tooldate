from lib2to3.pytree import convert
from logging import exception
from socket import timeout
from tracemalloc import start
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

def create_tool_date(request):
    if request.method == 'GET':
        form = TooldateForm()
        return render(request, 'tool/home.html', {'form': form})
    else:
        form = TooldateForm(request.POST)
        lst_extra_hours = request.POST['lst_extra_hours']
        start_date = request.POST['startdate']
        set_hours_work = request.POST['sethourswork']

        tool_date = ToolDate.objects.create(lst_extra_hours=lst_extra_hours, start_date=str(start_date).replace('/','-'))
        convert_start_date = datetime.strptime(tool_date.start_date, '%Y-%m-%d')
        start_date = convert_start_date
        time_out = 0
        extra_hours_save = 0
        for extra_hours in str(tool_date.lst_extra_hours).split('\r\n'):
            extra_hours = str(extra_hours).replace(",",".")
            weekday = start_date.weekday()
            if float(extra_hours) < float(set_hours_work):
                end_date = start_date
                time_out_choice = float(extra_hours) + time_out
                if time_out_choice >= float(set_hours_work):
                    days = float(time_out_choice)//float(set_hours_work)
                    time_out_choice = (float(time_out_choice) % float(set_hours_work))
                    if weekday == 4:
                        end_date += timedelta(days=2) + timedelta(days=days)
                    else:
                        end_date += timedelta(days=days)
                else:
                    time_out_choice = -(float(set_hours_work) - time_out - float(extra_hours))
                    if weekday == 4:
                        end_date += timedelta(days=3)
                    else:
                        if float(extra_hours) + float(extra_hours_save) >= float(set_hours_work):
                            extra_hours_save = float(set_hours_work) + float(time_out_choice)
                            end_date += timedelta(days=1)
                        else:
                            extra_hours_save = float(set_hours_work) + float(time_out_choice)

            else:
                days = float(extra_hours)//float(set_hours_work)
                time_out_choice = (float(extra_hours) % float(set_hours_work)) + time_out
                if weekday == 4:
                    end_date += timedelta(days=2) + timedelta(days=days)

                else:
                    end_date = start_date  + timedelta(days=days)
                    if end_date.weekday() in [5, 6]:
                        end_date += timedelta(days=2)
                        
            if request.POST['dateoff']:
                date_off = request.POST['dateoff']
                if end_date == datetime.strptime(str(date_off).replace('/','-'), '%Y-%m-%d'):
                    weekday = end_date.weekday()
                    if weekday ==4:
                        end_date += timedelta(days=3)    
                    else:    
                        end_date += timedelta(days=1)    
            tool_date_details = ToolDateDetails.objects.create(tool_date=tool_date, name=tool_date.pk, 
                                                   start_date=start_date, end_date=end_date,
                                                   extra_hours=extra_hours, time_out=time_out_choice,
                                                   weekday=weekday
                                                            )
            extra_hours_save = float(extra_hours_save) 
            time_out = time_out_choice
            start_date = end_date   
        return redirect('tool_date_details', pk=tool_date.pk)


