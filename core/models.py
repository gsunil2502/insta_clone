from django.db.models.deletion import CASCADE
from user.admin import User
from django.db import models
from django.contrib.auth import get_user_model
from core.utils import auto_save_current_user
from django.db.models.signals import post_save, post_delete
from notifications.models import Notification

#from crum import get_current_user
# Create your models here.
User = get_user_model()

#posts model
class Post(models.Model):
    #id =models.Autofield(primary_key=True) generated automatically
    text = models.CharField(max_length = 140, blank=True, null=True)
    image = models.ImageField(upload_to = 'post_images')    #BASE_DIR -> media ->post_images
    user = models.ForeignKey(User,on_delete = models.PROTECT, editable= False) #user_id_id
    created_on = models.DateTimeField(auto_now_add= True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-created_on']
        
    def __str__(self):
        return str(self.pk)
    
    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Post, self).save(*args, **kwargs)

    @property
    def likes_count(self):
        count = self.like_set.count()
        return count

    @property
    def comments_count(self):
        count = self.comment_set.count()
        return count

#comment model
class Comment(models.Model):
    text = models.CharField(max_length = 240)
    post = models.ForeignKey(Post, on_delete =models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE,editable= False)
    commented_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.text)

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Comment, self).save(*args, **kwargs)

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.text[:90]
        sender = comment.user
        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
        notify.save()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
        notify.delete()

#likes model
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete =models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, editable= False)
    #is_like = models.BooleanField(default=True)
    liked_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.post.id)
    
    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Like, self).save(*args, **kwargs)

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.save()
    
    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()

#followers model
class Follow(models.Model):
    user = models.ForeignKey(User,related_name= 'follow_follower',on_delete=models.CASCADE, editable= False)
    followed = models.ForeignKey(User,related_name= 'follow_followed',on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.user} --> {self.followed}"

    # def save(self, *args, **kwargs):
    #     print("inside save")
    #     print(self.user)
    #     print(self.followed)
    #     auto_save_current_user(self)
    #     super(Follow, self).save(*args, **kwargs)

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.user
        following = follow.followed
        notify = Notification(sender=sender, user=following, notification_type=3)
        notify.save()
        
    def user_unfollow(sender, instance, *args, **kwargs):
	    follow = instance
	    sender = follow.user
	    following = follow.followed
	    notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
	    notify.delete()

class Request(models.Model):
    user = models.ForeignKey(User,related_name= 'request_follower',on_delete=models.CASCADE, editable= False)
    request_user = models.ForeignKey(User,related_name= 'request_followed',on_delete=models.CASCADE)
    requested_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} --> {self.request_user}"

    # def save(self, *args, **kwargs):
    #     auto_save_current_user(self)
    #     super(Request, self).save(*args, **kwargs)

    def user_request(sender, instance, *args, **kwargs):
        request = instance
        sender = request.user
        requesting = request.request_user
        notify = Notification(sender=sender, user=requesting, notification_type=4)
        notify.save()
        
    def user_unrequest(sender, instance, *args, **kwargs):
        request = instance
        sender = request.user
        requesting = request.request_user
        notify = Notification.objects.filter(sender=sender, user=requesting, notification_type=4)
        notify.delete()

class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.pk)

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(SavedPost, self).save(*args, **kwargs)


post_save.connect(Like.user_liked_post, sender=Like)
post_delete.connect(Like.user_unlike_post, sender=Like)

post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)

post_save.connect(Request.user_request, sender=Request)
post_delete.connect(Request.user_unrequest, sender=Request)

post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)