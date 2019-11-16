from django.shortcuts import render,HttpResponse,redirect
from book import models as book_models
from author import models
# Create your views here.
# 作者列表
def author_list(request):
    author_list = models.Author.objects.all()
    book_list = book_models.Book.objects.all()
    return render(request,'author/author_list.html',{'author_list':author_list,'book_list':book_list})

# 增加作者
def add_author(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        book_id = request.POST.getlist('book_id')
        author_obj = models.Author.objects.create(name=author_name)
        author_obj.book.set(book_id)
        author_obj.save()
        return redirect('/author_list/')
    book_list = book_models.Book.objects.all()
    return render(request,'author/add_author.html',{'book_list':book_list})

# 删除作者
def del_author(request):
    id = request.GET.get('id')
    author_obj = models.Author.objects.get(id=id)
    author_obj.delete()
    return redirect('/author_list/')

# 编辑作者
def edit_author(request):
    if request.method == 'POST':
        author_id = request.POST.get('author_id')
        author_name = request.POST.get('author_name')
        book_id = request.POST.getlist('book_id')
        author_obj = models.Author.objects.get(id=author_id)
        author_obj.name = author_name
        author_obj.book.set(book_id)
        author_obj.save()
        return redirect('/author_list/')
    id = request.GET.get('id')
    author_obj = models.Author.objects.get(id=id)
    book_obj = book_models.Book.objects.all()
    return render(request,'author/edit_author.html',{'author_obj':author_obj,'book_obj':book_obj})
