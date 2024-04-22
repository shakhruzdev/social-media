from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfilePictureForm
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Comment, Post, Like, Follow
from authentication.models import MyUser


@login_required(login_url='/auth/login/')
def index_view(request):
    comments = Comment.objects.filter(is_visible=True)
    posts = Post.objects.filter(is_published=True)
    like_post = Like.objects.all()
    users = MyUser.objects.filter(user=request.user).first()
    for post in posts:
        post.comments = comments.filter(post_id=post.id)

    if request.method == 'POST':
        data = request.POST
        message = data['message']
        post_id = data['post_id']
        my_user = MyUser.objects.filter(user=request.user).first()
        obj = Comment.objects.create(message=message, post_id=post_id, author=my_user)
        obj.save()
        return redirect('/#{}'.format(post_id))

    context = {
        'posts': posts,
        'profiles': MyUser.objects.all().exclude(user=request.user),
        'comments': comments,
        'like_post': like_post,
        'profile': MyUser.objects.filter(user=request.user),
        'users': users,
    }
    return render(request, 'index.html', context=context)


def upload_view(request):
    if request.method == 'POST':
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(post_image=request.FILES['post_image'], author=my_user)
        post.save()
        return redirect('/')
    return redirect('/')


def profile_settings_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return redirect('/', pk=user.pk)
    else:
        return render(request, 'setting.html', {'user': user})


@login_required(login_url='/auth/signin/')
def like_view(request, pk):
    user = request.user
    my_user = MyUser.objects.get(id=user.id)
    post = get_object_or_404(Post, id=pk)
    if post.like_count.filter(id=my_user.id):
        post.like_count.remove(my_user)
    else:
        post.like_count.add(my_user)
    return redirect('/#{}'.format(post.id))


def follow_view(request):
    profile_id = request.GET.get('profile_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    profile = MyUser.objects.filter(id=profile_id).first()
    follow_exist = Follow.objects.filter(follower=my_user, following_id=profile_id)
    if not follow_exist.exists():
        obj = Follow.objects.create(follower=my_user, following_id=profile_id)
        obj.save()
        profile.follower_count += 1
        profile.save(update_fields=['follower_count'])
    else:
        follow_exist.delete()
        profile.follower_count -= 1
        profile.save(update_fields=['follower_count'])
    return redirect('/')


def search_view(request):
    query = request.GET.get('q')

    if query is '':
        return redirect('/')

    posts = Post.objects.filter(is_published=True, author=query).order_by('-created_at')

    context = {
        'posts': posts,
    }

    return render(request, 'index.html', context)


@login_required(login_url='/auth/signin/')
def profile_view(request):
    my_user_instance = MyUser.objects.get(user=request.GET['profile_id'])

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=my_user_instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=my_user_instance)

    return render(request, 'profile.html', {'my_user': my_user_instance, 'form': form})
