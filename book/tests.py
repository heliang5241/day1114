from django.test import TestCase
from django.shortcuts import HttpResponse,redirect,render
# Create your tests here.
def test_dict(request):
    pass
    dict1 = {}
    dict1['中国人民大学出版社'] = 24
    dict1['北京大学出版社'] = 27
    dict1['北京邮电大学'] = 29
    dict1['同济大学出版社'] = 3
    dict1['机械工业出版社'] = 26
    dict1['清华大学出版社'] = 28
    return render(request,'book/test_dict.html',{'dict1':dict1})
    return HttpResponse("测试字典")
