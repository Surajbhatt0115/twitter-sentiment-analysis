from django.shortcuts import render,HttpResponse
from subprocess import run,PIPE
import sys
# Create your views here.

def index(request):

    return render(request,'home.html')


def output(request):
    inpt = request.GET.get('hash','suraj')
    out1 = run([sys.executable,'C://Users//SURAJ BHATT//OneDrive//Desktop//django//tutorial-yt//main.py',inpt],shell=False,stdout=PIPE)
   
    return render(request,'result.html')