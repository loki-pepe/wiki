from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from random import choice

from . import util

markdowner = Markdown()


def edit(request, entry):
    if request.method == "POST":
        with open(f"entries/{entry}.md", "w") as file:
            file.write(request.POST["text"])
            return HttpResponseRedirect(f"../wiki/{entry}")

    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "entry": util.get_entry(entry)
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new(request):
    if request.method == "POST":
        try:
            index = list(map(str.lower, util.list_entries())).index(request.POST['title'].lower())
        except ValueError:
            with open(f"entries/{request.POST['title']}.md", "a") as file:
                file.write(f"# {request.POST['title']}\n\n{request.POST['text']}")
                return HttpResponseRedirect(f"wiki/{request.POST['title']}")

        return render(request, "encyclopedia/error.html", {
            "error": f"An entry named <a href='wiki/{util.list_entries()[index]}'>{util.list_entries()[index]}</a> already exists."
        })

    return render(request, "encyclopedia/new.html")


def random(request):
    return HttpResponseRedirect(f"wiki/{choice(util.list_entries())}")


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


def wiki(request, entry):
    try:
        index = list(map(str.lower, util.list_entries())).index(entry.lower())
    except ValueError:
        return render(request, "encyclopedia/error.html", {
            "error": "The requested page was not found."
        })

    entry = util.list_entries()[index]
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": markdowner.convert(util.get_entry(entry))
    })
