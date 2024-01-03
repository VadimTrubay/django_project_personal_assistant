from django.urls import path
from . import views
from .views import ContactSendEmail

app_name = 'contactsapp'

urlpatterns = [
    path('add_contact/', views.add_contact, name='add_contact'),
    path('edit_contact/<int:contact_id>', views.edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>', views.delete_contact, name='delete_contact'),
    path('search_contact/', views.search_contact, name='search_contact'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
    path('detail_contact/<int:contact_id>', views.detail_contact, name="detail_contact"),
    path('<int:id>/email/',  ContactSendEmail.as_view(), name='send_email')
]