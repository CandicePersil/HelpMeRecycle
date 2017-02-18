from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.db.models import Q
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie
import os
import json
import requests
from .models import *

COMMON_ERROR_MESSAGE = "An error has occurred."
NOT_FOUND_TRASH_BIN = "The trash bin is not existing."
ADD_ITEM_SUCCESSFULLY_MESSAGE = "Item has been added successfully."
SUCCESS_CSS_TAGS = "alert alert-success"
ERROR_CSS_TAGS = "alert alert-danger"
INFO_CSS_TAGS = "alert alert-info"
ERROR_SCAN = "Item could not be scanned, please try again."
NOT_FOUND_BAR_CODE = "NOTFOUND"
PASSWORD_CONFIRMATION_NOT_MATCH_MESSAGE = "The password confirmation doesn't match."
USERNAME_EXISTED_MESSAGE = "This Email has been taken."
REGISTER_SUCCESSFULLY_MESSAGE = "Register successfully!"
LOGGED_OUT_MESSAGE = "Log out successfully!"
LOGGED_IN_MESSAGE = "Log in successfully!"
LOGGED_IN_NOT_SUCCESSFULLY_MESSAGE = "Email or password is incorrect."


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


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def show_binitems(request, bin_name):
    try:
        bin = TrashBin.objects.get(name=bin_name.lower())
    except TrashBin.DoesNotExist:
        messages.add_message(request, messages.ERROR, NOT_FOUND_TRASH_BIN, extra_tags=ERROR_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))
    else:
        items = TrashItem.objects.filter(bin=bin).order_by("-total_rating", "name")[:30]

        if request.user.is_authenticated():
            idlist = []
            for i in items:
                idlist.append(i.id)
            voted_items_by_user = ItemRating.objects.filter(Q(user=request.user) & Q(item__id__in=idlist) & Q(rate=1))

            for item in items:
                for vi in voted_items_by_user:
                    if vi.item.id == item.id:
                        item.voted = "yes"
                        break
                    else:
                        item.voted = "no"

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
            result = TrashItem.objects.filter(
                Q(name__contains=criteria[4:]) | Q(sc_code__contains=criteria[4:])).order_by(
                "-total_rating", "bin__name")
        else:
            result = TrashItem.objects.filter(Q(name__contains=criteria) | Q(sc_code__contains=criteria)).order_by(
                "-total_rating", "bin__name")
        # if the scanned number was not found go directly to the add page and show a message there
        if (criteria[:4] == "scnr") & (not result.count()):
            criteria = criteria[4:]
            return HttpResponseRedirect("/additem/?scnf=" + criteria)

        elif (criteria[:4] == "scnr") & (result.count()):
            criteria = criteria[4:]

    else:
        # search all
        result = TrashItem.objects.order_by("-total_rating", "-created_date")[:30]

    if request.user.is_authenticated():
        idlist = []
        for i in result:
            idlist.append(i.id)
        voted_items_by_user = ItemRating.objects.filter(Q(user=request.user) & Q(item__id__in=idlist) & Q(rate=1))

        for item in result:
            for vi in voted_items_by_user:
                if vi.item.id == item.id:
                    item.voted = "yes"
                    break
                else:
                    item.voted = "no"

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


class LogIn(View):
    def get(self, request):
        return render(request, "trash/login.html")

    def post(self, request):
        data = request.POST

        user = auth.authenticate(email=data["email"], username=data["email"], password=data["password"])
        if user is not None and user.is_active:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, LOGGED_IN_MESSAGE, SUCCESS_CSS_TAGS)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.ERROR, LOGGED_IN_NOT_SUCCESSFULLY_MESSAGE, ERROR_CSS_TAGS)
            return render(request, "trash/login.html")


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, LOGGED_OUT_MESSAGE, SUCCESS_CSS_TAGS)
    return HttpResponseRedirect(reverse("index"))


class Register(View):
    def get(self, request):
        return render(request, "trash/register.html")

    def post(self, request):
        data = request.POST

        # check password and confirm_password match or not
        if data["password"] != data["confirm_password"]:
            messages.add_message(request, messages.ERROR, PASSWORD_CONFIRMATION_NOT_MATCH_MESSAGE, ERROR_CSS_TAGS)
            return render(request, "trash/register.html")

        # check unique username
        u = User.objects.filter(email=data["email"])
        if len(u) > 0:
            messages.add_message(request, messages.ERROR, USERNAME_EXISTED_MESSAGE, ERROR_CSS_TAGS)
            return render(request, "trash/register.html")

        new_user = User.objects.create_user(data["email"], data["email"], data["password"])
        new_user.save()

        auth.login(request, new_user)

        messages.add_message(request, messages.SUCCESS, REGISTER_SUCCESSFULLY_MESSAGE, SUCCESS_CSS_TAGS)
        return HttpResponseRedirect(reverse("index"))


@ensure_csrf_cookie
def rate(request):
    if request.method == "POST":
        try:
            item = TrashItem.objects.get(pk=request.POST["item_id"])
        except TrashItem.DoesNotExist:
            trash_bin = TrashBin.objects.get(name=request.POST["bin_name"].lower())
            items = TrashItem.objects.filter(bin=trash_bin)

            messages.add_message(request, messages.ERROR, COMMON_ERROR_MESSAGE, ERROR_CSS_TAGS)
            return render(request, "trash/binitems.html", {"bin": trash_bin, "items": items})
        else:
            try:
                item_rating = ItemRating.objects.get(item=item, user=request.user)
            except ItemRating.DoesNotExist:
                item_rating = ItemRating.objects.create(item=item, user=request.user)
                item_rating.rate = 1
                item.total_rating += 1
            else:
                if item_rating.rate == 1:
                    item_rating.rate = 0
                    item.total_rating += -1
                    item.voted = "no"
                elif item_rating.rate == 0:
                    item_rating.rate = 1
                    item.total_rating += 1
                    item.voted = "yes"

            item_rating.save()
            item.save()

        result = {
            "item_id": item.id,
            "total_rating": item.total_rating
        }

        return JsonResponse(result)
    else:
        return HttpResponseRedirect(reverse("index"))
