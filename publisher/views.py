from django.shortcuts import render,HttpResponse,redirect
from publisher import models
# Create your views here.
import redis
import re

def root(request):
    return render(request,'all.html')
# 出版社列表
def publisher_list(request):
    publisher_obj = models.Publisher.objects.all()
    return render(request,'publisher/publisher_list.html',{'publisher_obj':publisher_obj})
    # return HttpResponse('出版社列表')

# 增加出版社
def add_publisher(request):
    error_msg = ''
    if request.method == 'POST':
        publisher_name = request.POST.get('publisher_name')
        if publisher_name and not publisher_name.isspace():
            try:
                models.Publisher.objects.create(name=publisher_name)
                return redirect('/publisher_list/')
            except Exception as e:
                error_msg = e.args[1]
        else:
            error_msg = '出版社名称为空'
    return render(request,'publisher/add_publisher.html',{'error_msg':error_msg})

# 删除出版社
def del_publisher(request):
    publisher_id = request.GET.get('id')
    publisher_obj = models.Publisher.objects.get(id=publisher_id)
    publisher_obj.delete()
    return redirect('/publisher_list/')

# 编辑出版社
def edit_publisher(request):
    reg = r"Duplicate entry '(.*?)' for key 'name'"
    conn = redis.Redis(host="10.40.63.97", port=6379)
    if request.method == 'POST':
        new_publisher_id = request.POST.get('publisher_id',None)
        new_publisher_name = request.POST.get('publisher_name',None)
        if new_publisher_id == '':
            new_publisher_id = conn.get('new_publisher_id')
            print("出版社id为空,从redis中获取id:{0}".format(str(new_publisher_id,'utf-8')))
        else:
            print("向redis中存入出版社id")
            conn.set('new_publisher_id', new_publisher_id)
        publisher_obj = models.Publisher.objects.get(id=new_publisher_id)
        publisher_obj.name = new_publisher_name
        if new_publisher_name and not new_publisher_name.isspace():
            try:
                publisher_obj.save()
                return redirect('/publisher_list/')
            except Exception as e:
                error_msg = e.args[1]
                if "Duplicate entry" and "for key 'name'" in error_msg:
                    ss = re.findall(reg,error_msg)
                    if ss:
                        error_msg = ss[0] + " 数据库中已存在"
        else:
            error_msg = '出版社名称为空'
        if len(error_msg) > 0:
            old_publisher_name = conn.get('old_publisher_name')
            return render(request,'publisher/edit_publisher.html',{'error_msg':error_msg,'old_publisher_name':old_publisher_name})
    publisher_id = request.GET.get('id')
    publisher_obj = models.Publisher.objects.get(id=publisher_id)
    conn.set('old_publisher_name', publisher_obj.name)
    return render(request,'publisher/edit_publisher.html',{'publisher_obj':publisher_obj})
