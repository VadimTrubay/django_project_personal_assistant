from django.urls import path
from . import views


app_name = 'cloud_storageapp'

urlpatterns = [
    path('authorize/', views.dropbox_oauth, name='dropbox_oauth'),
    path('authorized/', views.dropbox_authorized, name='dropbox_authorized'),
    # path('search-files/', views.search_files, name='search_files'),
    path('dropbox-folders/', views.dropbox_folders, name='dropbox_folders'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('success_upload/', views.success_upload, name='success_upload'),
    path('dropbox-folders/<path:folder_path>/', views.folder_files, name='folder_files'),
    path('download-file/<path:file_path>/', views.download_file, name='download_file'),
    path('remove-folder/<path:folder_path>/', views.remove_folder, name='remove_folder'),
    path('remove-file/<path:file_path>/', views.remove_file, name='remove_file'),
    path('dropbox-folders-docs/<path:folder_path>/', views.folder_files_docs, name='folder_files_docs'),
    path('dropbox-folders-pics/<path:folder_path>/', views.folder_files_images, name='folder_files_images'),
    path('dropbox-folders-video/<path:folder_path>/', views.folder_files_video, name='folder_files_video'),
    path('dropbox-folders-audio/<path:folder_path>/', views.folder_files_audio, name='folder_files_audio'),
]