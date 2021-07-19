from django.contrib import admin
from notifications.models import(
    Notification,
)
# Register your models here.
class NotificationModelAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('post','sender','user','notification_type','text_preview','date','is_seen')


admin.site.register(Notification, NotificationModelAdmin)