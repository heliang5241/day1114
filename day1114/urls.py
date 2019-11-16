"""day1114 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from publisher import views as publisher
from book import views as book
from book import tests as test
from author import views as author
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 出版社
    url(r'^$', publisher.root),
    url(r'^publisher_list/', publisher.publisher_list),
    url(r'^add_publisher/', publisher.add_publisher),
    url(r'^del_publisher/', publisher.del_publisher),
    url(r'^edit_publisher/', publisher.edit_publisher),
    # 书籍
    url(r'^book_list/', book.book_list),
    url(r'^add_book/', book.add_book),
    url(r'^del_book/', book.del_book),
    url(r'^edit_book/', book.edit_book),
    url(r'^test_dict/', test.test_dict),
    # 作者
    url(r'^author_list/', author.author_list),
    url(r'^add_author/', author.add_author),
    url(r'^del_author/', author.del_author),
    url(r'^edit_author/', author.edit_author),
]
