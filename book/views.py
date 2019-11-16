from django.shortcuts import render,HttpResponse,redirect
from book import models
from publisher import models as pub_models
import re
import redis
# Create your views here.
# 书籍列表
def book_list(request):
    book_list = models.Book.objects.all()
    return render(request,'book/book_list.html',{'book_list':book_list})

# 增加书籍
def add_book(request):
    reg = "Duplicate entry '(.*?)' for key 'title'"
    error_msg = ''
    publisher_list = pub_models.Publisher.objects.all()
    if request.method == 'POST':
        book_name = request.POST.get('book_name',None)
        publisher_id = request.POST.get('publisher_id',None)
        print(book_name,publisher_id)
        if book_name and not book_name.isspace():
            try:
                models.Book.objects.create(title=book_name,publisher_id=publisher_id)
                return redirect('/book_list/')
            except Exception as e:
                error_msg = e.args[1]
                if 'Duplicate entry' in error_msg:
                    ss = re.findall(reg,error_msg)
                    if ss:
                        error_msg = ss[0] + ' 数据库中已存在'
        else:
            error_msg = '书籍信息为空'
    return render(request,'book/add_book.html',{'publisher_list':publisher_list,'error_msg':error_msg})

# 删除书籍
def del_book(request):
    book_id = request.GET.get('id')
    book_obj = models.Book.objects.get(id=book_id)
    book_obj.delete()
    return redirect('/book_list/')

# 编辑书籍
def edit_book(request):
    reg = "Duplicate entry '(.*?)' for key 'title'"
    conn = redis.Redis(host="127.0.63.97", port=6379)
    # error_msg = ''
    if request.method == 'POST':
        book_id = request.POST.get('book_id',None)
        book_title = request.POST.get('book_title',None)
        if book_id != '':
            conn.set('book_id',book_id)
            conn.set('book_title',book_title)
            conn.set('old_book_title',book_title)
        else:
            book_id = conn.get('book_id')
        if book_title and not book_title.isspace():
            publisher_id = request.POST.get('publisher_id')
            book_obj = models.Book.objects.get(id=book_id)
            book_obj.title = book_title
            book_obj.publisher_id = publisher_id
            try:
                book_obj.save()
                print(book_title,publisher_id)
                return redirect('/book_list/')
            except Exception as e:
                error_msg = e.args[1]
                if 'Duplicate entry' in error_msg:
                    ss = re.findall(reg,error_msg)
                    if ss:
                        error_msg = ss[0] + ' 数据库中已存在，再次提交'
        else:
            error_msg = '书名为空，再次提交'
        print(error_msg)
        return render(request, 'book/edit_book.html',{'error_msg': error_msg})
    book_id = request.GET.get('id')
    book_obj = models.Book.objects.get(id=book_id)
    publisher_obj = pub_models.Publisher.objects.all()
    publisher_name = pub_models.Publisher.objects.all().values()
    for i in publisher_name:
        name = i['name']
        id = i['id']
        print(name,id)
        conn.set(name,id)
    return render(request, 'book/edit_book.html',{'book_obj': book_obj, 'publisher_obj': publisher_obj})
