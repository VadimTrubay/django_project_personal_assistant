from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usersapp.views import root

urlpatterns = [
    path('', root, name='root'),
    path('admin/', admin.site.urls),
    path('users/', include('usersapp.urls')),
    path('bot/', include('ai_chat_bot.urls')),
    path('contacts/', include('contactsapp.urls')),
    path('notes/', include('notesapp.urls')),
    path('news/', include('newsapp.urls')),
    path('cloud_storageapp/', include('cloud_storageapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
