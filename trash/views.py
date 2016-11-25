from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils import translation
import json
from .models import *

COMMON_ERROR_MESSAGE = "An error has occured."
ADD_ITEM_SUCCESSFULLY_MESSAGE = "Item has been added successfully."
SUCCESS_CSS_TAGS = "alert alert-success"
ERROR_CSS_TAGS = "alert alert-danger"
ERROR_SCAN = "Item could not be scanned, please try again."
NOT_FOUND_BAR_CODE = "NOTFOUND"


def index(request):
    return render(request, "trash/index.html")


class AddItem(View):
    def get(self, request):
        bins = TrashBin.objects.all()
        # materials = TrashMaterial.objects.all()

        context = {
            "bins": bins,
            # "materials": materials
        }

        return render(request, "trash/additem.html", context)

    def post(self, request):
        new_item = TrashItem.objects.create(name=request.POST["name"].strip(),
                                            description=request.POST["description"].strip(),
                                            bin_id=request.POST["bin"], sc_code=request.POST["sc_code"])
        new_item.save()

        messages.add_message(request, messages.SUCCESS, ADD_ITEM_SUCCESSFULLY_MESSAGE, extra_tags=SUCCESS_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))


class TrashBins(View):
    def get(self, request):
        return render(request, "trash/bins.html")

    def post(self, request):
        pass


def show_binitems(request, bin_name):
    try:
        bin = TrashBin.objects.get(name=bin_name.lower())
    except TrashBin.DoesNotExist:
        messages.add_message(request, messages.ERROR, COMMON_ERROR_MESSAGE, extra_tags=ERROR_CSS_TAGS)
    else:
        items = TrashItem.objects.filter(bin=bin)
        return render(request, "trash/binitems.html", {"items": items})


def search(request):
    if request.GET["criteria"] == NOT_FOUND_BAR_CODE:
        messages.add_message(request, messages.ERROR, ERROR_SCAN, ERROR_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))
    elif (request.GET["criteria"] != "") & (request.GET["criteria"] != NOT_FOUND_BAR_CODE):
        criteria = request.GET["criteria"].lower().strip()
        result = TrashItem.objects.filter(name__contains=criteria).order_by("bin__name")
    else:
        result = TrashItem.objects.order_by('-created_date')[:20]

    context = {
        "items": result,
        "criteria": request.GET["criteria"].lower().strip()
    }

    return render(request, "trash/searchresult.html", context)

