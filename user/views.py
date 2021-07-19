from django import forms
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from user.forms import UserEditForm
from core.models import Follow, Request
# Create your views here.
User = get_user_model()

class ProfileView(View):
    template_name_anon = 'user/anonymous_profile.html'
    template_name_auth = 'user/authenticated_profile.html'
    template_name_anon_private= 'user/anonymous_profile_private.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        
        user_followers = Follow.objects.filter(followed=user)
        
        all_profiles_followers = User.objects.none()

        for followers in user_followers:
            all_profiles_followers |= User.objects.filter(email=followers.user)   

        followers_all_profiles = all_profiles_followers


        ###
        user_followings = Follow.objects.filter(user=user)
        
        all_profiles_followings = User.objects.none()

        for followings in user_followings:
            all_profiles_followings |= User.objects.filter(email=followings.followed)   

        #breakpoint()
        following_all_profiles = all_profiles_followings

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse('<h1>Doesnot exits</h1>')
        if username == request.user.username:
            context = {'user': user,'followers_all_profiles':followers_all_profiles , 'following_all_profiles':following_all_profiles}
            return render(request, self.template_name_auth, context=context)
        else:
            try:
                Follow.objects.get(user=request.user, followed=user)
                is_follows_this_user = True
            except Exception as e:
                is_follows_this_user = False        

                if user.is_private_account == True:
                    try:
                        Request.objects.get(user=request.user, request_user=user)
                        is_requests_this_user = True
                    except Exception as e:
                        is_requests_this_user = False 
                    context ={'user':user,'is_requests_this_user':is_requests_this_user,'followers_all_profiles':followers_all_profiles  , 'following_all_profiles':following_all_profiles}

                    return render(request, self.template_name_anon_private, context=context)

            context = {'user': user, 'is_follows_this_user': is_follows_this_user ,'followers_all_profiles':followers_all_profiles , 'following_all_profiles':following_all_profiles}
        
            return render(request, self.template_name_anon, context=context)


class ProfileEditView(View):
    template_name = 'user/profile_edit.html'
    form_class = UserEditForm

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        if username != request.user.username:
            return HttpResponse('<h1>This page does not exist</h1>')

        form = self.form_class(instance= request.user)
        context = {'form': form}
        return render(request, self.template_name,context=context)

    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES , instance = request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved your details in a safe place.')
            return redirect('profile_edit_view',request.user.username)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            context = {'form': form}
            return render(request,self.template_name, context=context)

class AllProfilesView(View):
    template_name = 'user/all_profiles.html'

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('query')
        if search_term:
            all_profiles = User.objects.filter(
                Q(username__contains = search_term) | Q(full_name__contains = search_term)
            ).exclude(username=request.user.username)
        else:
            all_profiles = User.objects.none()

        context = {'all_profiles': all_profiles}
        return render(request, self.template_name, context= context)

