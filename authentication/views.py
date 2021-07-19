from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse_lazy
from authentication.forms import UserForm
from django.contrib.auth import (
    authenticate, 
    login, logout,
    get_user_model
    )
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView, 
    PasswordResetDoneView, 
    PasswordResetView, 
    PasswordResetConfirmView, 
    PasswordResetDoneView, 
    PasswordResetCompleteView,
    PasswordChangeDoneView
    )
# Create your views here.
User = get_user_model()

def home(request):
    return HttpResponse('sunilll')

class SignInView(View):
    template_name = 'authentication/signin.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_feed_view')
        return render(request,self.template_name)

    def post(self, request, *args, **kwargs):
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username = email_username)
            email = user_obj.email
        except Exception as e:
            email = email_username

        user = authenticate(request,email=email, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            return render(request,self.template_name)
        login(request, user)
        messages.success(request, "Thanks for login, Welcome to Insta clone")
        return redirect('home_feed_view')
        

class SignUpView(View):
    template_name = 'authentication/signup.html'
    form_class = UserForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_feed_view')
        return render(request, self.template_name)
        #return HttpResponse('SUnillaaa')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin_view')
        
        context = {'form': form}
        return render(request, self.template_name, context)

class SignOutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('signin_view')

class PRView(PasswordResetView):
    html_email_template_name = "authentication/password_reset_email.html"
    template_name = "authentication/password_reset.html"

class PRConfirm(PasswordResetConfirmView):
    template_name = "authentication/password_reset_confirm.html"

class PRDone(PasswordResetDoneView):
    template_name = "authentication/password_reset_done.html"

class PRComplete(PasswordResetCompleteView):
    template_name = "authentication/password_reset_complete.html"

class PWDChangeView(PasswordChangeView):
    template_name = "authentication/password_change.html"
    success_url = reverse_lazy('password_change_done_view')

class PWDChangeDoneView(PasswordChangeDoneView):
    template_name = "authentication/password_change_done.html"