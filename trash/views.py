from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import Q
import os
import json
import requests
from .models import *

COMMON_ERROR_MESSAGE = "An error has occurred."
NOT_FOUND_TRASH_BIN = "The trash bin is not existing."
ADD_ITEM_SUCCESSFULLY_MESSAGE = "Item has been added successfully."
SUCCESS_CSS_TAGS = "alert alert-success"
ERROR_CSS_TAGS = "alert alert-danger"
ERROR_SCAN = "Item could not be scanned, please try again."
NOT_FOUND_BAR_CODE = "NOTFOUND"


def index(request):
    return render(request, "trash/index.html")


class AddItem(View):  # Add Item page
    def get(self, request):  # request to open the add item page
        bins = TrashBin.objects.all()  # get all the current trash bins

        if request.method == 'GET' and 'scnf' in request.GET:
            context = {
                "scanner": request.GET["scnf"],
                "bins": bins,
            }
        else:
            context = {
                "bins": bins,
            }

        return render(request, "trash/additem.html", context)

    def post(self, request):  # request to create an item
        new_item = TrashItem.objects.create(name=request.POST["name"].strip(),
                                            description=request.POST["description"].strip(),
                                            bin_id=request.POST["bin"], sc_code=request.POST["sc_code"])
        new_item.save()

        messages.add_message(request, messages.SUCCESS, ADD_ITEM_SUCCESSFULLY_MESSAGE, extra_tags=SUCCESS_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))


class TrashBins(View):  # Trash Bin page
    def get(self, request):
        return render(request, "trash/bins.html")

    def post(self, request):
        pass


def show_binitems(request, bin_name):
    try:
        bin = TrashBin.objects.get(name=bin_name.lower())
    except TrashBin.DoesNotExist:
        messages.add_message(request, messages.ERROR, NOT_FOUND_TRASH_BIN, extra_tags=ERROR_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))
    else:
        items = TrashItem.objects.filter(bin=bin)
        return render(request, "trash/binitems.html", {"bin": bin, "items": items})


def search(request):  # search item by title or bar code number
    if request.GET["criteria"] == NOT_FOUND_BAR_CODE:
        # message for not found bar code
        messages.add_message(request, messages.ERROR, ERROR_SCAN, ERROR_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))
    elif (request.GET["criteria"] != "") & (request.GET["criteria"] != NOT_FOUND_BAR_CODE):
        # searching item
        criteria = request.GET["criteria"].lower().strip()
        if criteria[:4] == "scnr":
            result = TrashItem.objects.filter(Q(name__contains=criteria[4:]) | Q(sc_code__contains=criteria[4:])).order_by(
                "bin__name")
        else:
            result = TrashItem.objects.filter(Q(name__contains=criteria) | Q(sc_code__contains=criteria)).order_by("bin__name")
        # if the scanned number was not found go directly to the add page and show a message there
        if (criteria[:4] == "scnr") & (not result.count()):
            criteria = criteria[4:]
            return HttpResponseRedirect("/additem/?scnf="+criteria)

        elif (criteria[:4] == "scnr") & (result.count()):
            criteria = criteria[4:]

    else:
        # search all
        result = TrashItem.objects.order_by('-created_date')[:20]

    context = {
        "items": result,
        "criteria": request.GET["criteria"].lower().strip()
    }

    return render(request, "trash/searchresult.html", context)


def openmap(request):  # open map page
    # get the coordinates list from opendata
    r = requests.get("http://opendata.lounaistieto.fi/aineistoja/Roskikset_geojson.geojson")
    if r.status_code != 404 and r.status_code != 403:
        data = r.json()
    else:
        # in case it is failed, use the local file
        my_dir = os.path.dirname(__file__)
        path = os.path.join(my_dir, 'static/trash/json/Roskikset_geojson.geojson')
        with open(path) as f:
            data = json.load(f)

    return render(request, "trash/maps.html", {"data": json.dumps(data)})


class AboutUs(View):
    def get(self, request):
        return render(request, "trash/aboutus.html")

    def post(self, request):
        pass
