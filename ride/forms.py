from .models import Comment, Entry
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    """
    The class uses the Comment model
    and displays the body field on the form.
    """

    class Meta:
        model = Comment
        fields = ("body",)


class EntryForm(forms.ModelForm):
    """A form to create an idea"""

    class Meta:
        model = Entry
        fields = (
            "title",
            "featured_image",
            "content",
            "distance",
            "start",
            "finish",
            "difficulty",
        )
        widgets = {"review": SummernoteWidget()}