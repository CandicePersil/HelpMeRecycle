"""Hmr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
import trash.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^trash/', include('trash.urls', namespace='trash')),
    url(r'^$', trash.views.index, name='index'),
    url(r'^additem/$', trash.views.AddItem.as_view(), name='additem'),
    url(r'^bin/$', trash.views.TrashBins.as_view(), name='trashbins'),
    url(r'^bin/(\w+)/$', trash.views.show_binitems, name='show_binitems'),
    url(r'^search/$', trash.views.search, name='search'),
]
