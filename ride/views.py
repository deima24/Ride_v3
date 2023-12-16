from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Entry, Rating
from .forms import CommentForm, EntryForm
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class EntryList(generic.ListView):
    model = Entry
    queryset = Entry.objects.filter(status=1).order_by("-created_on")
    template_name = "ride.html"
    paginate_by = 3


class EntryDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Entry.objects.filter(status=1)
        entry = get_object_or_404(queryset, slug=slug)
        comments = entry.comments.filter(approved=True).order_by("created_on")
        rating = entry.average_rating

        return render(
            request,
            "post_detail.html",
            {
                "entry": entry,
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm(),
                "rating": rating,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Entry.objects.filter(status=1)
        entry = get_object_or_404(queryset, slug=slug)
        comments = entry.comments.filter(approved=True).order_by("created_on")
        rating = entry.average_rating

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.entry = entry
            comment.save()

            user_rating = request.POST.get("rating")
            if user_rating:
                rating = int(user_rating)
            Rating.objects.create(
                entry=entry, user=request.user, rating=rating
            )
        else:
            comment_form = CommentForm()
        return render(
            request,
            "post_detail.html",
            {
                "entry": entry,
                "comments": comments,
                "commented": True,
                "comment_form": CommentForm(),
                "rating": rating,
            },
        )


class EntryEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """A view to edit an idea"""

    Model = Entry
    form_class = EntryForm
    success_url = "/entry/"
    template_name = "entry_edit.html"
    queryset = Entry.objects

    def form_valid(self, form):
        """If form is valid return to browse ideas"""
        self.success_url + str(self.object.pk) + "/"
        messages.success(self.request, "Post updated successfully")
        return super().form_valid(form)

    def test_func(self):
        """A function to test if the user is the author"""
        return self.request.user == self.get_object().author


class EntryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """A view to delete an post"""

    model = Entry
    success_url = "/entry/"
    template_name = "delete_entry.html"

    def test_func(self):
        return self.request.user == self.get_object().author


class CreateEntry(CreateView):
    """A view to create an post"""

    form_class = EntryForm
    template_name = "create_entry.html"
    success_url = "/entry/"
    model = Entry

    def form_valid(self, form):
        """If form is valid return to browse pots"""
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, "Post created successfully")
        return super(CreateEntry, self).form_valid(form)