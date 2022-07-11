from socket import timeout
from tracemalloc import start
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TooldateForm
from .models import ToolDate, ToolDateDetails
# from datetime import timedelta  
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
        if form.is_valid():
            lst_extra_hours = request.POST['lst_extra_hours']
            start_date = request.POST['start_date']
            tool_date = ToolDate.objects.create(lst_extra_hours=lst_extra_hours, start_date=start_date)
            convert_start_date = datetime.strptime(tool_date.start_date, '%Y-%m-%d')
            start_date = convert_start_date
            time_out = 0

            for extra_hours in str(tool_date.lst_extra_hours).split('-'):
                if float(extra_hours) < 8:
                    end_date = start_date
                    time_out_choice = float(extra_hours) + time_out
                    if time_out_choice >= 8:
                        days = float(time_out_choice)//8
                        # print(extra_hours)
                        time_out_choice = (float(time_out_choice) % 8)
                        # print(time_out_choice)
                        # time_out_choice = time_out_choice  - 8
                        end_date = start_date  + timedelta(days=days)
                else:
                    days = float(extra_hours)//8
                    # time_out_choice = float(extra_hours) - 8 + time_out
                    time_out_choice = (float(extra_hours) % 8) + time_out

                    end_date = start_date  + timedelta(days=days)

                tool_date_details = ToolDateDetails.objects.create(tool_date=tool_date, name=tool_date.pk, 
                                                       start_date=start_date, end_date=end_date,
                                                       extra_hours=extra_hours, time_out=time_out_choice    
                                                            )
                time_out = time_out_choice
                start_date = end_date     
            return redirect('tool_date_details', pk=tool_date.pk)
            


