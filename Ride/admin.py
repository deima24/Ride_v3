from django.contrib import admin
from .models import Entry, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):
    list_display = (
        "title",
        "author",
        "status",
        "created_on",
        "distance",
        "status",
        "difficulty",
    )

    search_fields = (
        "title",
        "author",
        "created_on",
        "distance",
        "start",
        "finish",
    )

    prepopulated_fields = {"slug": ("title",)}

    list_filter = ("created_on", "distance", "status")

    summernote_fields = ("start", "finish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "entry", "created_on", "approved")
    list_filter = ("approved", "created_on")
    search_fields = ("name", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)