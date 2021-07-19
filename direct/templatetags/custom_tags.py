from django import template
from django import forms
from core.models import Post
register = template.Library()
@register.filter

def replace_and_digit(value):
    value = value.replace("http://127.0.0.1:8000/post/","")
    value = int(value)
    return value

def get_post_obj(value):
    try:
        post_obj = Post.objects.get(pk=value)
    except Exception as e:
        post_obj = None
    return post_obj

def check_followed_using_post(post):
    if post.user.is_private_account == True:
        pass
    else:
        return True
    pass

register.filter('replace_and_digit', replace_and_digit)
register.filter('get_post_obj', get_post_obj)