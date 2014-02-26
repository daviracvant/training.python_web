from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from myblog.models import Post
from myblog.models import PostForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('published_date')
    context = {'posts': posts}
    return render(request, 'list.html', context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'detail.html', context)


def post_edit(request, post_id):
    record = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=record)
        if form.is_valid():
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            messages.success(request, 'Post updated.')
    else:
        form = PostForm(instance=record)

    return render(request, "edit.html", {'form': form})


def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, "edit.html", {'form': form})