from django import forms
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib import messages
# Create your views here.
from core.models import (
    Comment, Follow, Like,Post, Request,SavedPost, Request
)
from core.forms import PostCreateForm
from django.db.models import Q
User = get_user_model()

class HomeView(View):
    template_name = "core/feed.html"
    form_class = PostCreateForm
    def get(self, request, *args, **kwargs):
        try:
            admin_user = User.objects.get(username="InstagramClone")
        except Exception as e:
            pass
        form = self.form_class()
        follow_objects = Follow.objects.filter(user=request.user)
        all_posts = Post.objects.none()
        if follow_objects:
            for follow_obj in follow_objects:
                all_posts |= Post.objects.filter(user=follow_obj.followed)
        else:
            all_posts |= Post.objects.filter(user=admin_user)
        all_posts |= Post.objects.filter(user= request.user)
        context = {'form': form, 'all_posts': all_posts}
        return render(request,self.template_name,context=context)


class PostDetailView(View):
    template_name = 'core/post_detail.html'
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post_obj =Post.objects.get(pk=post_id)
        except Exception as e:
            return redirect(request.META.get('HTTP_REFERER'))        

        user_obj = User.objects.get(email=post_obj.user)

        if user_obj.username != request.user.username:
            if user_obj.is_private_account==True:
                try:
                    follow_obj = Follow.objects.get(user=request.user, followed=user_obj)
                except Exception as e:
                    follow_obj = None
                #breakpoint()
                if follow_obj:
                    pass
                else:
                    self.template_name= 'user/anonymous_profile_private.html'
                    try:
                        Request.objects.get(user=request.user, request_user=user_obj)
                        is_requests_this_user = True
                    except Exception as e:
                        is_requests_this_user = False 
                    messages.error(request, 'Follow this user to we post!!')
                    context ={'user':user_obj,'is_requests_this_user':is_requests_this_user}
                    return render(request, self.template_name, context=context)

        try:
            Like.objects.get(user = request.user, post_id = post_id)
            liked_this_post = True
        except Exception as e:
            liked_this_post = False

        try:
            SavedPost.objects.get(user=request.user, post_id=post_id)
            post_saved = True
        except Exception as e:
            post_saved = False
        
        context = {'post': post_obj, 'liked_this_post':liked_this_post,'post_saved': post_saved,}

        return render(request,self.template_name,context=context)



class PostCreateView(View):
    template_name = "core/feed.html"
    form_class = PostCreateForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home_feed_view')
        else:
            context = {'form': form}
            return render(request,self.template_name,context=context)
        
class PostDeleteView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            pass

        if request.user == post_obj.user:
            post_obj.delete()
        
        return redirect(request.META.get('HTTP_REFERER'))

class PostSaveView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            pass

        try:
            SavedPost.objects.create(post_id=post_id)
        except Exception as e:
            pass        

        return redirect(request.META.get('HTTP_REFERER'))


class PostUnsaveView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        
        try:
            savedpost_obj = SavedPost.objects.get(post_id=post_id)
            savedpost_obj.delete()
        except Exception as e:
            pass       

        return redirect(request.META.get('HTTP_REFERER'))

class PostLikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            Like.objects.get(user = request.user, post = post_id)
        except Exception as e:
            Like.objects.create(post_id=post_id)
        return redirect(request.META.get('HTTP_REFERER'))  

class PostUnlikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            like_obj = Like.objects.get(user = request.user, post = post_id)
            like_obj.delete()
        except Exception as e:
            pass
        return redirect(request.META.get('HTTP_REFERER'))  

class PostCommentView(View):
    def post(self,request, *args, **kwargs):
        post_id = kwargs.get('id')
        comment_text = request.POST.get('comment_text')
        Comment.objects.create(post_id=post_id,text= comment_text)

        return redirect(request.META.get('HTTP_REFERER'))  

class FollowDoneView(View):
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('followed_user_id')
        followed_user_obj = User.objects.get(pk=followed_user_id)
        # try:
        #     Follow.objects.get(user=request.user, followed=followed_user_obj)
        # except Exception as e:
        follow_obj = Follow.objects.create(user=request.user, followed=followed_user_obj)

        return redirect(request.META.get('HTTP_REFERER'))

class FollowAcceptedView(View):
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('accepted_user_id')
        followed_user_obj = User.objects.get(pk=followed_user_id)
        
        follow_obj = Follow.objects.create(user=followed_user_obj, followed=request.user)

        try:
            Request_obj = Request.objects.get(user=followed_user_obj, request_user= request.user)
            Request_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))

class FollowersView(View):
    template_name = 'user/authenticated_profile.html'
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)

        if username == request.user.username:
            self.template_name = 'user/authenticated_profile_follower.html'
        elif user.is_private_account == True:
            self.template_name = 'user/anonymous_profile_private.html'
        else:
            self.template_name = 'user/anonymous_profile_follower.html'

        #breakpoint()
        user_followers = Follow.objects.filter(followed=user)
        
        all_profiles_followers = User.objects.none()

        for followers in user_followers:
            all_profiles_followers |= User.objects.filter(email=followers.user)   

        search_term = request.GET.get('query')
        if search_term:
            all_profiles = User.objects.filter(
                Q(username__contains = search_term) | Q(full_name__contains = search_term)
            )
            followers_all_profiles = all_profiles.intersection(all_profiles_followers)        
        else:
            followers_all_profiles = all_profiles_followers

        context = {'user':user,'followers_all_profiles': followers_all_profiles}
        return render(request, self.template_name, context= context)
        
class FollowingView(View):
    template_name = 'user/anonymous_profile_private.html'
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
     
        if username == request.user.username:
            self.template_name = 'user/authenticated_profile_following.html'
        elif user.is_private_account == True:
            self.template_name = 'user/anonymous_profile_private.html'
        else:
            self.template_name = 'user/anonymous_profile_following.html'
        
        user_followings = Follow.objects.filter(user=user)
        
        all_profiles_followings = User.objects.none()

        for followings in user_followings:
            all_profiles_followings |= User.objects.filter(email=followings.followed)   

        search_term = request.GET.get('query')
        if search_term:
            all_profiles = User.objects.filter(
                Q(username__contains = search_term) | Q(full_name__contains = search_term)
            )
            following_all_profiles = all_profiles.intersection(all_profiles_followings)        
        else:
            following_all_profiles = all_profiles_followings

        context = {'user':user,'following_all_profiles': following_all_profiles}
        return render(request, self.template_name, context= context)
    
class FollowRequestView(View):
    def post(self,request, *args, **kwargs):
        request_user_id = request.POST.get('request_user_id')
        request_user_obj = User.objects.get(pk=request_user_id)
        
        try:
            Request.objects.get(user=request.user, request_user=request_user_obj)
        except Exception as e:
            Request_obj = Request.objects.create(user= request.user,request_user=request_user_obj)
        
        

        return redirect(request.META.get('HTTP_REFERER'))
        
class UnfollowDoneView(View):
    def post(self, request, *args, **kwargs):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = User.objects.get(pk=unfollowed_user_id)

        try:
            follow_obj = Follow.objects.get(user=request.user, followed=unfollowed_user_obj)
            follow_obj.delete()
        except Exception as e:
            pass
        return redirect(request.META.get('HTTP_REFERER'))

class UnfollowRequestView(View):
    def post(self, request, *args, **kwargs):
        unrequest_user_id = request.POST.get('unrequest_user_id')
        unrequest_user_obj = User.objects.get(pk=unrequest_user_id)
        print(request.user)
        print(unrequest_user_obj)

        try:
            Request_obj = Request.objects.get(user=unrequest_user_obj, request_user= request.user)
            Request_obj.delete()
        except Exception as e:
            Request_obj = Request.objects.get(user= request.user, request_user= unrequest_user_obj)
            Request_obj.delete()
        return redirect(request.META.get('HTTP_REFERER'))

class LikedPostsView(View):
    template_name = 'core/liked_posts.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SavedPostsView(View):
    template_name = 'core/saved_posts.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ExplorePostsView(View):
    template_name = 'core/posts_explore.html'
    def get(self, request, *args, **kwargs):
        
        #all_posts = Post.objects.annotate(count=Count('like')).order_by('-count')
        #context = {'all_posts': all_posts}
        

        try:
            admin_user = User.objects.get(username="InstagramClone")
        except Exception as e:
            pass
        #form = self.form_class()
        follow_objects = Follow.objects.filter(user=request.user)
        all_posts = Post.objects.none()
        if follow_objects:
            for follow_obj in follow_objects:
                all_posts |= Post.objects.filter(user=follow_obj.followed)
        else:
            all_posts |= Post.objects.filter(user=admin_user)
        all_posts |= Post.objects.filter(user= request.user)
        all_posts = all_posts.annotate(count=Count('like')).order_by('-count')
        context = {'all_posts': all_posts}
        return render(request,self.template_name,context=context)
