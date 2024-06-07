from django.shortcuts import render

def home(request):
    #nothing for now
    return render(request,'Emploi_du_temps/index.html',{})