from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import auth_email, get_token
from .views import (
    UserViewSet,
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    ReviewsViewSet,
    CommentsViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/email/', auth_email),
    path('v1/auth/token/', get_token),
]
