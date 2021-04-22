import markdown2
from random import randint
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    entriesList = util.list_entries()

    if title in entriesList:
        content = util.get_entry(title) 
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": markdown2.markdown(content)

        })

    else:
        return render(request, "encyclopedia/error.html", {
            'error_message': 'Sorry, that page does not exist.'
        } )


def search(request):
    if request.method == "GET":
        entriesList = util.list_entries()
        title = request.GET['q']
        newList = []
        for entry in entriesList:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/page.html", {
                    "content": markdown2.markdown(util.get_entry(title)),
                    "title": title
                })
                        
            #Substring matches displayed as a list
            if title.lower() in entry.lower():
                newList.append(entry)
                    #return list of substring matches

        if len(newList) == 0:
            return render(request, "encyclopedia/error.html", {
                "error_message": f"No results for \'{title}\'"
            })

        return render(request, "encyclopedia/search.html", {
            "entries": newList
        })


    
def add(request):
    entriesList = util.list_entries()
    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title in entriesList:
            return render(request, "encyclopedia/add.html", {
                "available": True
            })

        else:
            util.save_entry(title, content)
            return redirect(wiki, title=title)
    return render(request, "encyclopedia/add.html", {
        "available": False
    })


def edit(request, title):
    content = util.get_entry(title)
    if request.method == "GET":
        return render (request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
    if request.method == "POST":
        content = request.POST.get("editedContent")
        util.save_entry(title, content)
        return redirect(wiki, title=title)


def random(request):
    entries = util.list_entries()
    randomPage = entries[randint(0, len(entries)-1)]
    return redirect(wiki, title=randomPage)
    
    
