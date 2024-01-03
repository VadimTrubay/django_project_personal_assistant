from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, NoteForm
from .models import Tag, Note
from django.db import models


@login_required
def search_note(request):
    search_query_note = request.GET.get('search_query', '')
    user_notes = Note.objects.filter(user=request.user)
    search_results_note = user_notes.filter(title__icontains=search_query_note)
    if search_query_note == ' ' or search_query_note == 'all':
        context = {
            'search_query_note': search_query_note,
            'all_notes': user_notes,
        }
        return render(request, 'notesapp/search_note.html', context)

    else:
        context = {
            'search_query_note': search_query_note,
            'search_results_note': search_results_note,
        }

        return render(request, 'notesapp/search_note.html', context)


@login_required
def search_tag(request):
    search_query_tag = request.GET.get('search_query', '')
    user_tags = Tag.objects.filter(user=request.user)
    search_results_tag = user_tags.filter(name__icontains=search_query_tag)

    if search_query_tag == ' ' or search_query_tag == 'all':
        context = {
            'search_query_tag': search_query_tag,
            'all_tags': user_tags
        }
        return render(request, 'notesapp/search_tag.html', context)

    else:
        context = {
            'search_query_tag': search_query_tag,
            'search_results_tag': search_results_tag
        }

        return render(request, 'notesapp/search_tag.html', context)


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='usersapp:success')
        else:
            return render(request, 'notesapp/add_tag.html', context={'form': form})

    return render(request, 'notesapp/add_tag.html', context={'form': TagForm()})


@login_required
def add_note(request):
    tags = Tag.objects.filter(user=request.user).all()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags:
                note.tags.add(tag)
            return redirect(to='usersapp:success')
        else:
            return render(request, 'notesapp/add_note.html', context={'form': form, 'tags': tags})

    return render(request, 'notesapp/add_note.html', context={'form': NoteForm(), 'tags': tags})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    tags = Tag.objects.filter(user=request.user).all()
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.tags.clear()
            note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'),
                                             user=request.user)
            for tag in choice_tags:
                note.tags.add(tag)
            return redirect(to="notesapp:detail_note", note_id=note_id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notesapp/edit_note.html',
                  context={'form': form, 'note': note, 'tags': tags})


@login_required
def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notesapp/detail_note.html', context={"note": note})


@login_required
def detail_tag(request, tag_id):
    tag = Tag.objects.filter(id=tag_id).first()
    notes = Note.objects.filter(tags=tag_id).all()
    return render(request, 'notesapp/detail_tag.html', context={"tag": tag, "notes": notes})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect(to='usersapp:success')
    return render(request, 'notesapp/delete_note.html', {'note': note})


@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id, user=request.user)
    if request.method == 'POST':
        tag.delete()
        return redirect(to='usersapp:success')
    return render(request, 'notesapp/delete_tag.html', {'tag': tag})


@login_required
def tag_sort(request, tag_id):
    tags = Tag.objects.filter(id=tag_id).first()
    notes = Note.objects.filter(tags=tag_id).all()
    return render(request, 'notesapp/tag_sort.html', {'notes': notes, 'tags': tags})

