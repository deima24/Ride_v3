from . import views
from django.urls import path

urlpatterns = [
    path("", views.EntryList.as_view(), name="entry"),
    path('<slug:slug>', views.EntryDetail.as_view(), name='entry_detail'),
    path('edit/<slug:pk>', views.EntryEdit.as_view(), name='entry_edit'),
    path('delete/<slug:pk>', views.EntryDelete.as_view(), name='delete_entry'),
    path('create/', views.CreateEntry.as_view(), name='create'),
]