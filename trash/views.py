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
import requests
from .models import *
from .forms import *


def index(request):
    return render(request, "trash/index.html")


class AddItem(View):
    def get(self, request):
        bins = TrashBin.objects.all()
        materials = TrashMaterial.objects.all()

        context = {
            "bins": bins,
            "materials": materials
        }

        return render(request, "trash/additem.html", context)

    def post(self, request):
        pass


class TrashBins(View):
    def get(self, request):
        return render(request, "trash/bins.html")

    def post(self, request):
        pass


def show_binitems(request, bin_name):
    bin = get_object_or_404(TrashBin, name=bin_name)
    return render(request, "trash/binitems.html", {"bin": bin})

