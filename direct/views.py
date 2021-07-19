from django.http import request
from authentication.views import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from direct.models import Message
from django.contrib.auth import get_user_model
from django.db.models import Q
from core.models import Follow, Post, Request

User = get_user_model()

class InboxView(View):
    template_name = "direct/direct.html"

    def get(self, request, *args, **kwargs):
        messages = Message.get_messages(user=request.user)
        active_direct = None
        directs = None
        if messages:
            message = messages[0]
            active_direct = message['user'].username
            print(active_direct)
            directs = Message.objects.filter(user=request.user, recipient=message['user'])
            directs.update(is_read=True)
            for message in messages:
                if message['user'].username == active_direct:
                    message['unread'] = 0
        context = {'directs': directs,'messages': messages,'active_direct': active_direct}
        
        return render(request,self.template_name,context=context)

class DirectsView(View):

    template_name = "direct/direct.html"

    def get(self,request,*args, **kwargs):
        username = kwargs.get('username')
        try:
            profileuser = User.objects.get(username=username)
        except Exception as e:
            profileuser = request.user
        user = request.user
        messages = Message.get_messages(user=user)
        active_direct = username
        directs = Message.objects.filter(user=user, recipient__username=username)
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == username:
                message['unread'] = 0

        context = {'directs': directs,'messages': messages,'active_direct':active_direct,'profileuser':profileuser}

        return render(request,self.template_name,context=context)


class SendLinkView(View):

    template_name = "direct/direct_link.html"
    template_name_anon = 'user/anonymous_profile.html'
    template_name_auth = 'user/authenticated_profile.html'
    template_name_anon_private= 'user/anonymous_profile_private.html'
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            profileuser = User.objects.get(username=username)
        except Exception as e:
            profileuser = request.user
        
        try:
            followeduser = Follow.objects.get(user= request.user, followed= profileuser)
            body = "http://127.0.0.1:8000/post/"+str(kwargs.get('id'))
            from_user = request.user
            
            to_user = User.objects.get(username=username)
            Message.send_message(from_user, to_user, body)
            #linkkk

            user = request.user
            messages = Message.get_messages(user=user)
            active_direct = username
            directs = Message.objects.filter(user=user, recipient__username=username)
            directs.update(is_read=True)
            for message in messages:
                if message['user'].username == username:
                    message['unread'] = 0

            context = {'directs': directs,'messages': messages,'active_direct':active_direct,'profileuser':profileuser, 'username':username}

            return render(request,self.template_name,context=context)
        except Exception as e:
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                return HttpResponse('<h1>Doesnot exits</h1>')
            if username == request.user.username:
                context = {'user': user}
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
                        context ={'user':user,'is_requests_this_user':is_requests_this_user,'is_follows_this_user': is_follows_this_user}

                        return render(request, self.template_name_anon_private, context=context)

                context = {'user': user, 'is_follows_this_user': is_follows_this_user}
            
                return render(request, self.template_name_anon, context=context)
    

class NewConversationView(View):
    def get(self, request, *args, **kwargs):
        from_user = request.user
        username = kwargs.get('username')
        body = ''
        try:
            to_user = User.objects.get(username=username)
        except Exception as e:
            return redirect('all_profiles_view')
        if from_user != to_user:
            Message.send_message(from_user, to_user, body)
        return redirect('inbox_view')


class SendDirectView(View):
    
    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_username = request.POST.get('to_user')
        body = request.POST.get('body')
        if request.method == 'POST':
            to_user = User.objects.get(username=to_user_username)
            Message.send_message(from_user, to_user, body)
            return redirect(request.META.get('HTTP_REFERER'))
        return HttpResponse("not sent")



class DirectProfilesView(View):
    template_name = 'core/post_send_detail.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post = Post.objects.get(pk=post_id)
        except Exception as e:
            pass

        search_term = request.GET.get('query')
        if search_term:
            all_profiles = User.objects.filter(
                Q(username__contains = search_term) | Q(full_name__contains = search_term)
            ).exclude(username=request.user.username)
        else:
            all_profiles = User.objects.none()

        context = {'all_profiles': all_profiles,'post':post}
        return render(request, self.template_name, context= context)

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()
	return {'directs_count':directs_count}

