from django.urls import path
from authentication.views import SignUpView, home, SignInView,SignOutView,PRView, PRConfirm, PRDone, PRComplete,PWDChangeView, PWDChangeDoneView
urlpatterns = [
    #path('', home ,name= 'home_view'),
    path('signup/', SignUpView.as_view(),name= 'signup_view'),
    path('', SignInView.as_view(),name= 'signin_view'),
    path('signout/', SignOutView.as_view(),name= 'signout_view'),
    path('password/reset/',PRView.as_view() ,name='password_reset'),
    path('password/reset/done',PRDone.as_view() ,name = 'password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>', PRConfirm.as_view(),name = 'password_reset_confirm'),
    path('password/reset/complete',PRComplete.as_view() ,name = 'password_reset_complete'),
    path('password/change/',PWDChangeView.as_view(), name='password_change_view'),
    path('password/change/done/',PWDChangeDoneView.as_view(), name='password_change_done_view')
]