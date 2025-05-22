from django.shortcuts import render
from django.http import HttpResponse

def dataRender3(request):
    return HttpResponse("Render Point 3 From Test file")

def htmlPage2(request):
    # return render(request, 'index.html')
    return render(request, 'home2.html')