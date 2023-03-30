from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown

from . import util

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    try:
        index = list(map(str.lower, util.list_entries())).index(entry.lower())
    except ValueError:
        return render(request, "encyclopedia/error.html")

    entry = util.list_entries()[index]
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": markdowner.convert(util.get_entry(entry))
    })

def search(request):
    try:
        index = list(map(str.lower, util.list_entries())).index(request.GET["q"].lower())
    except ValueError:
        entries = []
        for entry in util.list_entries():
            if request.GET["q"].lower() in entry.lower():
                entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "query": request.GET["q"]
        })

    return HttpResponseRedirect(f"wiki/{util.list_entries()[index]}")
