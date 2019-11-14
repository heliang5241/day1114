from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def publisher_list(request):
    return HttpResponse('出版社列表')