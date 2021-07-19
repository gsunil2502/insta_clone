from django.urls import path
from core.views import (HomeView,FollowDoneView, PostLikeView, PostUnlikeView,UnfollowDoneView,PostCreateView, PostDeleteView,PostDetailView, PostCommentView,PostSaveView,PostUnsaveView,LikedPostsView,SavedPostsView,ExplorePostsView,FollowRequestView,UnfollowRequestView,FollowAcceptedView,FollowersView, FollowingView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('feed/', login_required(HomeView.as_view()), name='home_feed_view'),
    path('follow/done',login_required(FollowDoneView.as_view()),name='follow_done_view'),
    path('follow/accepted',login_required(FollowAcceptedView.as_view()),name='follow_accepted_view'),
    path('follow/request',login_required(FollowRequestView.as_view()),name='follow_request_view'),
    path('unfollow/done',login_required(UnfollowDoneView.as_view()),name='unfollow_done_view'),
    path('unfollow/request',login_required(UnfollowRequestView.as_view()),name='unfollow_request_view'),

    path('followers/<str:username>',login_required(FollowersView.as_view()),name='followers_view'),
    path('following/<str:username>',login_required(FollowingView.as_view()),name='following_view'),

    path('post/<int:id>', login_required(PostDetailView.as_view()),name='post_detail_view'),
    path('post/create/', login_required(PostCreateView.as_view()), name='post_create_view'),
    path('post/save/<int:id>/', login_required(PostSaveView.as_view()), name='post_save_view'),
    path('post/unsave/<int:id>/', login_required(PostUnsaveView.as_view()), name='post_unsave_view'),
    path('post/delete/<int:id>',login_required(PostDeleteView.as_view()), name= 'post_delete_view'),

    path('post/liked/', login_required(LikedPostsView.as_view()), name='liked_posts_view'),
    path('post/saved/', login_required(SavedPostsView.as_view()), name='saved_posts_view'),
    path('post/explore/', login_required(ExplorePostsView.as_view()), name='explore_posts_view'),

    path('post/like/<int:id>', login_required(PostLikeView.as_view()), name='post_like_view'),
    path('post/unlike/<int:id>', login_required(PostUnlikeView.as_view()), name='post_unlike_view'),
    path('post/comment/<int:id>', login_required(PostCommentView.as_view()), name='post_comment_view')
]