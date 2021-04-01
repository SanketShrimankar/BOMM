from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, UserUpdate, userdetailview, CommentsCreateRetrieve, BookComments, LikeUpdate, CatalogueRemove, getCatalogue, UserCatalogue, getLikeCount

app_name = 'users'

urlpatterns = [
    path('user/', CustomUserCreate.as_view(), name="users"),
    path('user/register/', CustomUserCreate.as_view(), name="create_user"),
    path('user/logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('user/update/<int:pk>/', UserUpdate, name="update"),
    path("user/<int:pk>/", userdetailview, name="user_details"),
    path('user/comments/', CommentsCreateRetrieve.as_view(), name="all_comments"),
    path('user/comment/<str:pk>/', BookComments, name="comment"),
    path('book/likes/', LikeUpdate.as_view(), name="likes"),
    path('book/likes/<str:pk>/', getLikeCount, name="likes_count"),
    path('book/likes/<str:pk>/<str:uid>/', LikeUpdate.as_view(), name="likes"),
    path('user/catalogue/<int:pk>/', CatalogueRemove, name = "catalogue"),
    path('user/get_catalogue/<str:id>/<str:pk>/', getCatalogue, name = "get_catalogue")
]