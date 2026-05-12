from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "post_list.html", {"posts": posts})

def sign_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/signup.html', {'error_message': "Username already exists."})

        if User.objects.filter(email=email).exists():
            return render(request, 'auth/signup.html', {'error_message': "Email already exists."})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'auth/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error_message': "Invalid username or password."})

    return render(request, 'auth/login.html')

@login_required(login_url='login')
def dashboard_view(request):

    search = request.GET.get('search', '')

    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    if search:
        posts = posts.filter(title__icontains=search)

    context = {
        "posts": posts,
        "total_posts": posts.count(),
    }

    return render(request, "dashboard/index.html", context)

@login_required
def create_post_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        Post.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user
        )

        return redirect("dashboard")

    return render(request, "dashboard/create_post.html")

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")

        if request.FILES.get("image"):
            post.image = request.FILES.get("image")

        post.save()
        return redirect("dashboard")

    return render(request, "dashboard/edit_post.html", {"post": post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    post.delete()
    return redirect("dashboard")


def logout_view(request):
    logout(request)
    return redirect('login')

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "post_detail.html", {"post": post})


