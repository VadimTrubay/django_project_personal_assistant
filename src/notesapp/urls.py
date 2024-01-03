from django.urls import path
from . import views

app_name = 'notesapp'

urlpatterns = [
    path('search_note/', views.search_note, name="search_note"),
    path('search_tag/', views.search_tag, name="search_tag"),
    path('add_tag/', views.add_tag, name="add_tag"),
    path('add_note/', views.add_note, name="add_note"),
    path('detail_note/<int:note_id>', views.detail_note, name="detail_note"),
    path('detail_tag/<int:tag_id>', views.detail_tag, name="detail_tag"),
    path('delete_note/<int:note_id>', views.delete_note, name="delete_note"),
    path('delete_tag/<int:tag_id>', views.delete_tag, name="delete_tag"),
    path('edit_note/<int:note_id>', views.edit_note, name="edit_note"),
]
