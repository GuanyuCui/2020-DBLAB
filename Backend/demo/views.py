from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from .models import Demo
# Create your views here.

def default(request):
    return HttpResponse('hello,world')

def demo(request,paperID):
    paper = Demo.objects.raw('SELECT * FROM Demo WHERE paperID=%s',[paperID])[0]
    context = {
        'paperID':paperID,
        'paper':paper
    }
    print(paper.paperid,paper.content)
    return render(request,'demo/layout.html',context=context)

def interact(request):
    inputS = request.POST['text']
    return HttpResponse('<h1>received string:</h1><br><h2>{}</h2>'.format(inputS))