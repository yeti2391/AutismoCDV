from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostView, Like, Comment
from .forms import PostForm, CommentForm
#from accounts.decorators import allowed_users
# Create your views here.


class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

    #para hacer los comentarios en un post:
    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect('blog_app:detail', slug=post.slug)
        return redirect('blog_app:detail', slug=self.get_object().slug)

    # agregar el form al contexto para el template:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form':CommentForm()
        })
        return context


    #logica para hacer el conteo de vistas en el blog
    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        #se usa get_or_create para que me sume una sola vista por usuario
        #pero esto puede causar problemas con anonymoususer por eso hacemos el if
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)
        return object

"""
Por si fuera necesario modificar posts desde el frontend:

#@allowed_users(allowed_roles=['Admin'])
class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/blog/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        'view_type':'crear'
        })
        return context

#@@allowed_users(allowed_roles=['Admin'])
class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/blog/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        'view_type':'actualizar'
        })
        return context

#@allowed_users(allowed_roles=['Admin'])
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog/'
"""

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        # quitar el me gustado
        like_qs[0].delete()
        return redirect('blog_app:detail', slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect('blog_app:detail', slug=slug)
