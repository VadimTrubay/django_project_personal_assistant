import json
import os
from pathlib import Path
from dropbox.exceptions import AuthError
import requests
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import environ
import dropbox
from .forms import FileUploadForm

import datetime

from personal_assistant.settings import DROPBOX_APP_KEY, DROPBOX_APP_SECRET

DROPBOX_APP_KEY = DROPBOX_APP_KEY
DROPBOX_APP_SECRET = DROPBOX_APP_SECRET
# DROPBOX_OAUTH2_REFRESH_TOKEN = env("DROPBOX_OAUTH2_REFRESH_TOKEN")
REDIRECT_URL = 'http://127.0.0.1:8000/cloud_storageapp/'


def dropbox_oauth(request):
    return redirect(
        f'https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&redirect_uri={REDIRECT_URL}authorized&response_type=code')


def dropbox_authorized(request):
    try:
        code = request.GET["code"]
        print(f"Code: {code}")
    except KeyError:
        return JsonResponse({"error": "Authorization code not found in the request."}, status=400)
    data = requests.post('https://api.dropboxapi.com/oauth2/token', {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": f"{REDIRECT_URL}authorized",
    }, auth=(DROPBOX_APP_KEY, DROPBOX_APP_SECRET))
    request.session["DROPBOX_ACCESS_TOKEN"] = data.json()["access_token"]
    with open('OAuth_token.json', 'w') as file:
        json.dump(
            {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "token": data.json()["access_token"]},
            file, indent=4, ensure_ascii=False)

    return redirect(to="cloud_storageapp:dropbox_folders")


# """query for search!"""
# def search_files(request, claudinary=None):
#     if request.method == "POST":
#         data=requests.post("https://api.dropboxapi.com/2/files/search_v2", headers={
#             "Authorization": f"Bearer {request.session['DROPBOX_ACCESS_TOKEN']}",
#         }, json={
#             "query": "cc"
#         })
#
#         results = []
#         for f in data.json()["matches"]:
#             id = f["metadata"]["metadata"]["id"]
#             data = requests.post("https://api.dropboxapi.com/2/files/get_preview", headers={
#                 "Authorization": f"Bearer {request.session['DROPBOX_ACCESS_TOKEN']}",
#                  "Dropbox-API-Arg": json.dumps({"path": id})}, stream=True)
#             print(data.text)
#             r = claudinary.uploader.upload(data.content)
#             img_url = r["secure_url"]
#             return JsonResponse(data.json())
#     else:
#         return render(request, "cloud_storageapp/search.html")


def get_access_token():
    with open('OAuth_token.json', 'r') as file:
        data = json.load(file)
        date = data.get('datetime')
        date_dt_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        curent_time = datetime.datetime.now()
        delta = ((curent_time - date_dt_obj).total_seconds()) / 60 / 60
        print(delta)
        if delta > 3:
            return None
        token = data.get('token')
        print(date, token)
        return token


def get_access_dbx(request):
    dbx = None
    try:
        access_token = get_access_token()
        if access_token:
            dbx = dropbox.Dropbox(access_token)
        else:
            print("Try refresh!!!!!!!!!!!!")
            return redirect(to="cloud_storageapp:dropbox_oauth")
    except Exception as err:
        print(f"My ERROR !!!!! ::: {err}")

    return dbx


def dropbox_folders(request):
    # try:
    #     access_token = get_access_token()
    #     if access_token:
    #         dbx = dropbox.Dropbox(access_token)
    #     else:
    #         print("Try refresh!!!!!!!!!!!!")
    #         return redirect(to="cloud_storageapp:dropbox_oauth")
    #         print("Try refresh   Ok Ok OK OK ")
    # except Exception as err:
    #     print(f"My ERROR !!!!! ::: {err}")

    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    # List all files in the root directory
    folders = []
    for entry in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            folders.append(entry)

    context = {'folders': folders}
    return render(request, 'dropbox_folders.html', context)


def folder_files(request, folder_path):
    print(str(folder_path).strip('/'))
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    files = []
    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                files.append(entry)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_path() and \
                e.user_message_text.startswith("not_folder/"):
            # The provided path is not a folder path, handle the error as needed
            pass
        else:
            raise

    context = {'files': files, 'folder_path': folder_path}
    return render(request, 'folder_files.html', context)

    # for entry in dbx.files_list_folder(folder_path).entries:
    #     if isinstance(entry, dropbox.files.FileMetadata):
    #         files.append(entry)
    #
    # context = {'files': files, 'folder_path': folder_path}
    # return render(request, 'folder_files.html', context)


def success_upload(request):
    return render(request, 'upload_success.html', {})


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Replace 'YOUR_DROPBOX_ACCESS_TOKEN' with your Dropbox access token
            dbx = get_access_dbx(request)
            if isinstance(dbx, (HttpResponseRedirect, type(None))):
                print(f'ISTANCE ::::::::::::::: {dbx}')
                return redirect(to='cloud_storageapp:dropbox_oauth')
            folder = form.cleaned_data['folder'].replace(' ', '_')
            print(f"FOLDER::::::  ::  : :: : {folder}")

            file = request.FILES['file']
            print(f"FILE CLEAN NAME :  {file.name.replace(' ', '_')}")
            clean_file_name = file.name.replace(' ', '_')
            file_path = f'/{folder}/{clean_file_name}' if folder else f'/unknown/{clean_file_name}'
            print(f"FILE PASS II : {file_path}")
            dbx.files_upload(file.read(), file_path)

            # Redirect to a success page or display a success message
            return redirect(to='cloud_storageapp:success_upload')

    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})


# dbx.files_download(db_query_file, rev=None)

def download_file(request, file_path):
    file_full_path = 'cloud_storageapp/download-file/' + file_path

    # while '//' in file_full_path:
    #     file_full_path = file_full_path.replace('//', '/')
    print(f'FILE PASSSSSSSSSS    {file_full_path}')
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    # file = request.FILES['file']

    try:
        metadata, response = dbx.files_download(file_path, rev=None)

    except dropbox.exceptions.ApiError as e:
        return HttpResponseNotFound("File not found. Exeption from except!")

    file_content = response.content
    # content_type = metadata.mime_type
    content_type = response.headers.get('Content-Type')
    print(f"CONTENT TYPE::::::::   {content_type}")
    response = HttpResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_full_path)}"'
    return response


def remove_folder(request, folder_path):
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')

    folder_path = folder_path.replace('%20', ' ')
    dbx.files_delete_v2(folder_path)
    print('files was removed')
    return redirect(to='cloud_storageapp:dropbox_folders')


def remove_file(request, file_path):
    print(file_path)
    folder = file_path.split('/')[1]
    print(folder)
    dbx = get_access_dbx(request)
    file_path = file_path.replace('%2520', ' ')
    file_path = file_path.replace('%20', ' ')

    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')

    dbx.files_delete_v2(file_path)
    print('files was removed')
    return redirect(to='cloud_storageapp:folder_files', folder_path=f"/{folder}")


def folder_files_docs(request, folder_path):
    print(str(folder_path).strip('/'))
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    files = []
    folders = []

    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                _, file_extension = os.path.splitext(entry.name)
                if file_extension.lower() in ['.docx', '.doc', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.xps', '.dot',
                                              '.wbk', '.docm', '.txt', '.rtf', '.log']:
                    files.append(entry)
        for entry in dbx.files_list_folder('', recursive=True).entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                folders.append(entry)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_path() and \
                e.user_message_text.startswith("not_folder/"):
            # The provided path is not a folder path, handle the error as needed
            pass
        else:
            raise

    context = {'files': files, 'folder_path': folder_path, 'folders': folders}
    return render(request, 'folder_files_docs.html', context)


def folder_files_audio(request, folder_path):
    print(str(folder_path).strip('/'))
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    files = []
    folders = []

    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                _, file_extension = os.path.splitext(entry.name)
                if file_extension.lower() in ['.aac', '.mp3', '.wav', '.wma', '.dolby', '.digital', '.dts', '.aiff',
                                              '.asf', '.flac', '.adpcm', '.dsd', '.lpcm', '.ogg']:
                    files.append(entry)
        for entry in dbx.files_list_folder('', recursive=True).entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                folders.append(entry)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_path() and \
                e.user_message_text.startswith("not_folder/"):
            # The provided path is not a folder path, handle the error as needed
            pass
        else:
            raise

    context = {'files': files, 'folder_path': folder_path, 'folders': folders}
    return render(request, 'folder_files_docs.html', context)


def folder_files_video(request, folder_path):
    print(str(folder_path).strip('/'))
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    files = []
    folders = []

    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                _, file_extension = os.path.splitext(entry.name)
                if file_extension.lower() in ['.mpeg-1', '.mpeg-4', '.mpeg-2', '.avi', '.mov', '.avchd', '.divx', '.hd',
                                              '.mkv', '.webm', '.flv', '.viv', '.ts', '.mpg']:
                    files.append(entry)
        for entry in dbx.files_list_folder('', recursive=True).entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                folders.append(entry)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_path() and \
                e.user_message_text.startswith("not_folder/"):
            # The provided path is not a folder path, handle the error as needed
            pass
        else:
            raise

    context = {'files': files, 'folder_path': folder_path, 'folders': folders}
    return render(request, 'folder_files_docs.html', context)


def folder_files_images(request, folder_path):
    print(str(folder_path).strip('/'))
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'ISTANCE ::::::::::::::: {dbx}')
        return redirect(to='cloud_storageapp:dropbox_oauth')
    files = []
    folders = []

    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                _, file_extension = os.path.splitext(entry.name)
                if file_extension.lower() in ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.png', '.gif', '.webp',
                                              '.tiff', '.tif', '.psd', '.bmp', '.dib', '.raw', '.arw', '.nrw', '.img']:
                    files.append(entry)
        for entry in dbx.files_list_folder('', recursive=True).entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                folders.append(entry)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_path() and \
                e.user_message_text.startswith("not_folder/"):
            # The provided path is not a folder path, handle the error as needed
            pass
        else:
            raise

    context = {'files': files, 'folder_path': folder_path, 'folders': folders}
    return render(request, 'folder_files_docs.html', context)


"""GEt ACCESS TOKEN """
#
# BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env()
#
# environ.Env.read_env(BASE_DIR / ".env")
# # print(f'{BASE_DIR} ~~ YOUR BASE_DIR')
#
# # /Users/ekaterina/Documents/GitHub/Personal-Assistant-Django
# Secret_Key = env("SECRET_KEY")
# # Create your views here.
#
# DROPBOX_APP_KEY = env("DROPBOX_APP_KEY")
# DROPBOX_APP_SECRET = env("DROPBOX_APP_SECRET")
# DROPBOX_OAUTH2_REFRESH_TOKEN = env("DROPBOX_OAUTH2_REFRESH_TOKEN")
# REDIRECT_URL = 'http://127.0.0.1:8000/cloud_storageapp/'
#
# def dropbox_oauth(request):
#     return redirect(f'https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&redirect_uri={REDIRECT_URL}authorized&response_type=code')
#
#
# def dropbox_authorized(request):
#     try:
#         code = request.GET["code"]
#         print(f"Code: {code}")
#     except KeyError:
#         return JsonResponse({"error": "Authorization code not found in the request."}, status=400)
#     data = requests.post('https://api.dropboxapi.com/oauth2/token', {
#         "code": code,
#         "grant_type": "authorization_code",
#         "redirect_uri": f"{REDIRECT_URL}authorized",
#     }, auth=(DROPBOX_APP_KEY, DROPBOX_APP_SECRET))
#     return JsonResponse(data.json())


# Check if the file exists
# if os.path.exists(file_full_path):
#     # Open the file in binary mode and create a FileResponse to stream the file to the client
#     with open(file_full_path, 'rb') as file:
#         response = FileResponse(file, content_type='application/octet-stream')
#         # Set the content disposition header to force the file download
#         response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_full_path)}"'
#         return response
# else:
#     # Return a 404 Not Found response if the file does not exist
#     return HttpResponseNotFound("File not found.")
