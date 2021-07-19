from django.urls import path
from direct.views import InboxView,DirectsView,SendDirectView,NewConversationView,DirectProfilesView,SendLinkView
from django.contrib.auth.decorators import login_required
urlpatterns = [
   	path('inbox/', login_required(InboxView.as_view()), name='inbox_view'),
   	path('directs/<str:username>/',login_required(DirectsView.as_view()) , name='directs_view'),
   	#path('new/', UserSearch, name='usersearch'),
   	path('new/in/<str:username>/', login_required(NewConversationView.as_view()), name='new_conversation_view'),
	path('sendlink/post/<int:id>/<str:username>',login_required(SendLinkView.as_view()),name='send_link_view'),
   	path('send/', login_required(SendDirectView.as_view()), name='send_direct_view'),
	path('sendpost/post/<int:id>', login_required(DirectProfilesView.as_view()), name='send_post_view'),

]