from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.generic import ListView, DetailView
from rest_framework import generics
from .serializers import PostSerializers


# home view for posts. Posts are displayed in a list
class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all()


# Detail view (view post detail)
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


# New post view (Create new post)
def postview(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    form = PostForm()
    return render(request, 'post.html', {'form': form})


# Edit a post
def edit(request, pk, template_name='edit.html'):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, template_name, {'form': form})


# Delete post
def delete(request, pk, template_name='confirm_delete.html'):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, template_name, {'object': post})


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
