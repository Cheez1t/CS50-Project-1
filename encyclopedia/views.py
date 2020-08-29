from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from django import forms
import random

import markdown2
from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content =  forms.CharField(label='', widget = forms.Textarea(attrs={'rows':20, 'cols':60}))

    def clean(self): # Validates the entire form.
        cleaned_data = super().clean()
        title_data = cleaned_data.get('title')
        title_content = cleaned_data.get('content')

        entered_line = title_content.partition('\n')[0]
        ideal_line = '# '+ title_data
        if entered_line.strip() != ideal_line.strip(): # Check that the content format matches the title.
            if title_data in util.list_entries():
                raise ValidationError({
                'title': ['Error: The title "' + title_data + '" already exists.'],
                'content': ['Error: The first line of this entry should be: # ' + title_data],
                })
            raise ValidationError({'content':['Error: The first line of this entry should be: # ' + title_data]})
        if title_data in util.list_entries():
            raise ValidationError('Error: The title "' + title_data + '" already exists.')

class EditForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput())
    content =  forms.CharField(label='', widget = forms.Textarea(attrs={'rows':20, 'cols':60}))

    """def clean(self): # Validates the entire form.
        cleaned_data = super().clean()
        title_data = cleaned_data.get('title')
        title_content = cleaned_data.get('content')

        first_line = title_content.partition('\n')[0]
        ideal_line = '# ' + title_data
        if first_line.strip() != ideal_line.strip(): # Check that the content format matches the title.
            raise ValidationError('Error: The first line of this entry should be: # ' + title_data)
"""
def index(request):
        # Search Bar Function
    query = request.GET.get('q')
    if query != None:
        return HttpResponseRedirect(reverse('search', args=[query]))
        # Search Bar Function

    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

def entry(request, entry):
    # Search Bar Function
    query = request.GET.get('q')
    if query != None:
        return HttpResponseRedirect(reverse('search', args=[query]))
    # Search Bar Function

    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/entryPage.html", {
        "entry" : entry,
        "exists" : False
    })
    return render(request, "encyclopedia/entryPage.html", {
        "entry" : entry,
        "exists" : True,
        "content" : markdown2.markdown(util.get_entry(entry))
    })


def search(request, search):
    # Search Bar Function
    query = request.GET.get('q')
    if query != None:
        return HttpResponseRedirect(reverse('search', args=[query]))
    # Search Bar Function

    if search in util.list_entries():
        return HttpResponseRedirect(reverse('entry', args=[search]))
    else:
        match_list = []
        for i in util.list_entries():
            if search.lower() in i.lower():
                match_list.append(i)
        return render(request, "encyclopedia/searchPage.html", {
            "list" : match_list
        })

def Create_New_Page(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid(): # Server Side Validation
            form_title = form.cleaned_data['title']
            form_content = form.cleaned_data['content']
            util.save_entry(form_title, form_content) # Make new entry
            return HttpResponseRedirect('wiki/' + form_title)
        else:
            return render(request, "encyclopedia/createNewPage.html", {
            "form": form
            })
    return render(request, "encyclopedia/createNewPage.html", {
        "form": EntryForm()
    })
    
def edit(request, page):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid(): # Server Side Validation
            form_content = form.cleaned_data['content']
            print('POST =' + form_content)
            util.save_entry(page, form_content) # Update entry
            return HttpResponseRedirect(reverse('entry', kwargs={'entry':page}))
        else:
            initial_dict = {
            "title" : page,
            "content" : util.get_entry(page)}
            return render(request, "encyclopedia/editPage.html",{
            "form" : form,
            "entry" : page
            })

    initial_dict = {
        "title" : page,
        "content" : util.get_entry(page)
    }
    print('GET = ' + initial_dict['content'])
    return render(request, "encyclopedia/editPage.html", {
        "form": EditForm(request.POST or None, initial = initial_dict),
        "entry" : page
    })

def random_page(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return HttpResponseRedirect(reverse('entry', args=[random_page]))