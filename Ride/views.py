from django.shortcuts import render
from django.views import generic
from .models import Entry


class EntryList(generic.ListView):
    model = Entry
    queryset = Entry.objects.filter(status=1).order_by("-created_on")
    template_name = "ride.html"
    paginate_by = 3

