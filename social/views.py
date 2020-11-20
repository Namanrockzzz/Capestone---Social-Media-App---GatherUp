from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from social import models, forms

# Create your views here.
class Wall(LoginRequiredMixin, ListView):
    # queryset = models.Post.objects.all()
    context_object_name = 'posts'
    template_name = "social/wall.html"
    login_url = 'auth/login'

    def get_queryset(self):
        friendIDs = [ friend.person2.id for friend in models.Friends.objects.filter(person1 = self.request.user) ]
        friendIDs = friendIDs + [ friend.person1.id for friend in models.Friends.objects.filter(person2 = self.request.user) ]
        # return models.Post.objects.filter(
        # (Q(user__person1 = self.request.user.pk) | Q(user__person2 = self.request.user.pk)) & 
        # ~Q(user = self.request.user)
        # ).order_by('-created_at')
        return models.Post.objects.filter(user__in = friendIDs).order_by('-created_at')

class Home(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'social/home.html'
    login_url = 'auth/login'

    def get_queryset(self):
        return models.Post.objects.filter(user = self.request.user).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["post_form"] = forms.PostForm
        return context
    

class Post(View):
    def post(self, request):
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('/home/')

class PostLike(View):
    model = models.Post
    def post(self, request, pk):
        post = self.model.objects.get(pk=pk)
        models.Like.objects.create(post = post, user=request.user)
        return HttpResponse(code=204)

class PostComment(View):
    model = models.Post
    form = forms.PostComment

    def post(self, request, pk):
        post = self.model.objects.get(pk=pk)
        form = self.form(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponse(code=204)
        print(form.errors)
        return HttpResponse(code = 400)

