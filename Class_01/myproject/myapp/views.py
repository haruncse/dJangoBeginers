from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse(" Hello Dept CSE ")
    # return render(request, 'index.html')


def dataRender2(request):
    return HttpResponse("Render Point 2")
    # return render(request, 'index.html')
def htmlPage(request):
    return render(request, 'index.html')
