from django.urls import path
from notifications.views import NotificationView,DeleteNotificationView
from django.contrib.auth.decorators import login_required
urlpatterns = [
   	path('notifications/', login_required(NotificationView.as_view()), name='notification_view'),
   	path('<noti_id>/delete', login_required(DeleteNotificationView.as_view()), name='delete_notification_view'),
]