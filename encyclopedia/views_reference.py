from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

import markdown2
from . import util


def index(request):
    query = request.GET.get('q')
    if query == None:
        print("Display Normally")
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })
    else:
        if query in util.list_entries():
            return render(request, "encyclopedia/entryPage.html", {
            "entry" : query,
            "exists" : True,
            "content" : markdown2.markdown(util.get_entry(query))
            })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })

def entry(request, entry): 
    if request.GET.get('q') != None:
        search(request.GET.get('q'))
        return()

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

def search(q):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    print("Made it in!")
    if q == None:
        return None
    if q in util.list_entries():
        print("Should redirect soon.")
        print(q)
        return HttpResponseRedirect(reverse("encyclopedia:entry"))
    else:
        return None
