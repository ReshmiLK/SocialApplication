from django.urls import path
from socialweb import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[

    path("register/",views.SignUpView.as_view(),name="register"),
    path("",views.SignInView.as_view(),name="signin"),
    path("profile/add",views.ProfileView.as_view(),name="profile-add"),
    path("home",views.IndexView.as_view(),name="home"),
    path("posts/<int:id>/comments/add",views.AddCommentView.as_view(),name="add-comment"),
    path("posts/<int:id>/like/add",views.LikePostView.as_view(),name="like"),
    path("profile/details",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/<int:id>/change",views.ProfileUpdateView.as_view(),name="profile-edit"),
    path("posts/<int:pk>/remove",views.PostDeleteView.as_view(),name="post-delete"),
    path("posts/<int:id>/dislike/",views.DislikeView.as_view(),name="dislike"),
    path("posts/comments/<int:id>/like/add",views.CommentLikePostView.as_view(),name="comment-like"),
    path("posts/comments/<int:id>/dislike/",views.CommentDisikePostView.as_view(),name="comment-dislike"),
    path("signout",views.SignOutView.as_view(),name="signout"),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)