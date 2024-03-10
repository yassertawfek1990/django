from typing import Any
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Post
from django.views import View
from django.views.generic.base import TemplateView # to show html templates 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView 
from .forms import CommentForm

# Create your views here.

class fp(ListView): # its IMPORTANT to add .as_view() to the path in urls.py file
    template_name = "blog/index.html"
    queryset = Post.objects.all().order_by('-date')[:3] #we use queryset instead of model since we want to get specific peace or query from the table not all of it
    context_object_name = "posts"


#def allp(request):
 #   return render(request, "blog/all.html", {"allposts": postlist})

class allp(ListView):
    template_name = "blog/all.html"
    queryset = Post.objects.all().order_by("-date")
    context_object_name = "allposts"

#def p(request, slug):
#    thepost = next(post for post in postlist if post["slug"] == slug)
#    return render(request, "blog/post.html" , {"post": thepost})

class p(DetailView):
    template_name = "blog/post.html"
    model = Post

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: # we neeed to from typing import Any for this func to work
        context = super().get_context_data(**kwargs)
        loaded_post = self.object
        context["post"] = loaded_post
        context["tags"] = loaded_post.tags.all()
        context["comment_form"] = CommentForm()
        return context
    

class SinglePost(View):

    def AlreadyStored(self,request,PostId):
        stored_posts_ids = request.session.get("stored_posts")
        if stored_posts_ids is not None:
            stored = PostId in stored_posts_ids
        else:
            stored = False

        return stored


    def get(self,request,slug): # get is handling what happens when you type this url
        post = Post.objects.get(slug=slug)
        stored_posts_ids = request.session.get("stored_posts")
        if stored_posts_ids is None:
            stored_posts_ids = []
        
       # stored_posts_ids = list(map(int, stored_posts_ids))  we use map to convert list of strings to integers but here the ids are appended integers already in the read later view

        context = {"post": post, "tags": post.tags.all(),"comment_form":CommentForm(),"comments": post.comments.all().order_by("-id"),"stored": self.AlreadyStored(request,post.id),"favorite_ids": stored_posts_ids}# we use order bt id to make sure new comments with newer id show first
        return render(request, "blog/post.html", context)

    def post(self,request,slug): # Post is handling any request coming from a form that has this view's url in the action field
        post = Post.objects.get(slug=slug)
        submitted_form =CommentForm(request.POST)
        if submitted_form.is_valid():
            comment = submitted_form.save(commit=False)# this commit will make the comment saved but will not hit or change the database since this form is missing the post field
            comment.post = post # this will update the post field with the related post
            comment.save()
            return HttpResponseRedirect(reverse("detail", args=[slug] )) # this will redirect to the same page as a new one with the comment saved
        
        # this will load the page again with data submitted and the error messages
        context = {"post": post, "tags": post.tags.all(),"comment_form":CommentForm(),"comments": post.comments.all().order_by("-id")}
        return render(request, "blog/post.html", context)
    
class ReadLater(View):

    def get(self, request):
        stored_posts_ids = request.session.get("stored_posts") # we use get so if there is no data it will not make error

        
        context = {}
        if stored_posts_ids is None or len(stored_posts_ids) == 0:
            context["posts"] = []
            context["has_post"] = False
        else:
            posts = Post.objects.filter(id__in = stored_posts_ids)
            context["posts"] = posts
            context["has_post"] = True
        
        return render(request, "blog/read-later.html",context)


    
    def post(self, request):
        stored_posts = request.session.get("stored_posts") # we use get so if there is no data it will not make error

        if stored_posts is None:
            stored_posts = []
        
        saved_post_id = int(request.POST["post_id"])

        if saved_post_id not in stored_posts:
            stored_posts.append(saved_post_id)
            request.session["stored_posts"] = stored_posts # this is important to save the data to the session
        
        else:
            stored_posts.remove(saved_post_id)
            request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
        

