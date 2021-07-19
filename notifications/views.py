from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, View
from notifications.models import Notification
from core.models import Post
# Create your views here.
class NotificationView(View):
    template_name = "core/notification.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-date')
        Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
        
        post_obj =Post.objects.filter(user=user)
        
        context = { 'notifications': notifications,'post_obj':post_obj}
        return render(request,self.template_name, context=context)

class DeleteNotificationView(View): 

    def get(self, request, *args, **kwargs):
        user = request.user
        noti_id = kwargs.get("noti_id")
        Notification.objects.filter(id=noti_id, user=user).delete()
        return redirect('notification_view')

def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications':count_notifications}