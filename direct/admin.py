from django.contrib import admin

# Register your models here.
from direct.models import Message

class MessageModelAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('user','sender','recipient','body','date','is_read')

admin.site.register(Message, MessageModelAdmin)