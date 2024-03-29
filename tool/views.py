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
        lst_dateoff = []
        days_0 = 0
        days_1 = 0
        if request.POST['dateoff']:
            for date_off in str(request.POST['dateoff']).split('\r\n'):
                lst_dateoff.append(str(date_off).replace('/','-'))
        for extra_hours in str(tool_date.lst_extra_hours).split('\r\n'):
            end_date = start_date
            extra_hours = str(extra_hours).replace(",",".")
            weekday = start_date.weekday()
            if float(extra_hours) < float(set_hours_work):
                end_date = start_date
                time_out_choice = float(extra_hours) + time_out
                if float(time_out_choice) >= float(set_hours_work):
                    if float(time_out_choice) > float(set_hours_work):
                        days = float(time_out_choice)//float(set_hours_work)
                        time_out_choice = (float(time_out_choice) % float(set_hours_work))
                        if weekday == 4:
                            end_date += timedelta(days=2) + timedelta(days=days)
                        else:
                            end_date += timedelta(days=days)
                    else:
                        days_1 = 1
                        time_out_choice = 0
                else:
                    end_date = end_date
            else:
                if float(extra_hours) == float(set_hours_work):
                    if (float(extra_hours) + time_out) > float(set_hours_work):
                        days = (float(extra_hours) + time_out)// float(set_hours_work)
                        end_date += timedelta(days)
                    time_out_choice = (float(extra_hours) + time_out) - float(set_hours_work)
                    days =(float(extra_hours)//float(set_hours_work)) + day_time_out_choice
                    print(days)
                    if time_out > 0:
                        if weekday == 4:
                            end_date += timedelta(days=2)
                        else:
                            if end_date.weekday() in [5, 6]:
                                end_date += timedelta(days=2)
                            else:
                                days_0 = 1
                                end_date += timedelta(days=days)
                                if end_date.weekday() in [5, 6]:
                                    end_date += timedelta(days=2)
                    elif time_out == 0:
                        days_1 = 1

                else:
                    day_time_out_choice = 0
                    time_out_choice = (float(extra_hours) % float(set_hours_work)) + time_out
                    if time_out_choice > float(set_hours_work):
                        day_time_out_choice =(float(time_out_choice) // float(set_hours_work))
                        time_out_choice = float(time_out_choice) % float(set_hours_work)
                    elif (time_out_choice // float(set_hours_work)) == 1:
                        day_time_out_choice =(float(time_out_choice) // float(set_hours_work) - 1)
                        time_out_choice = 0
                    days =(float(extra_hours)//float(set_hours_work)) + day_time_out_choice
                    if weekday == 4:
                        end_date += timedelta(days=2) + timedelta(days=days)
                    else:
                        if end_date.weekday() in [5, 6]:
                            end_date += timedelta(days=2) + timedelta(days=days)
                        else:
                            days_0 = 1
                            end_date += timedelta(days=days)
                            if end_date.weekday() in [5, 6]:
                                end_date += timedelta(days=2)
            if request.POST['dateoff']:
                for date_off in str(request.POST['dateoff']).split('\r\n'):
                    a = datetime.strptime(str(date_off).replace('/','-'), '%Y-%m-%d')
                    if a > start_date and a < end_date:
                        end_date += timedelta(days=1)
                        if end_date.weekday() in [5, 6]:
                            end_date += timedelta(days=3)

                    if end_date == datetime.strptime(str(date_off).replace('/','-'), '%Y-%m-%d'):
                        weekday = end_date.weekday()
                        if weekday == 4:
                            end_date += timedelta(days=3)    
                        else:    
                            end_date += timedelta(days=1)   
                    if start_date == datetime.strptime(str(date_off).replace('/','-'), '%Y-%m-%d'):
                        if weekday == 4:
                            start_date += timedelta(days=3)    
                        else:    
                            start_date += timedelta(days=1)   
            tool_date_details = ToolDateDetails.objects.create(tool_date=tool_date, name=tool_date.pk, 
                                                   start_date=start_date, end_date=end_date,
                                                   extra_hours=extra_hours, time_out=time_out_choice,
                                                   weekday=weekday, extra_hours_save=0
                                                            )
            time_out = time_out_choice
            start_date = end_date
            if time_out == 0:
                if days_0 == 1:
                    if float(extra_hours) > float(set_hours_work):
                        start_date = start_date + timedelta(days=1)
                else: 
                    start_date = start_date
                if days_1 == 1:
                    start_date = start_date + timedelta(days=1)
                if start_date.weekday() in [5, 6]:
                    start_date += timedelta(days=2)
                    end_date += timedelta(days=2)
        return redirect('tool_date_details', pk=tool_date.pk)
