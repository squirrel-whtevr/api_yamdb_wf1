from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, status,
                            viewsets)
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb.settings import EMAIL_HOST_USER
from .filters import TitlesFilter
from .models import Categories, Genres, Reviews, Titles, User
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


@api_view(['POST'])
def auth_email(request):
    email = request.data['email']
    username = request.data['username']
    if not User.objects.filter(email=email).exists():
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    user, created = User.objects.get_or_create(email=email,
                                               username=username)
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(
        'Api registration token',
        f'Your api registration confirmation code is {user.confirmation_code}',
        f'{EMAIL_HOST_USER}',
        [email],
        fail_silently=False,
    )
    return Response({'email': email, 'code': user.confirmation_code},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    email = request.data['email']
    confirmation_code = request.data['confirmation_code']
    user = get_object_or_404(User, email=email)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response({'field': 'Wrong confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.kwargs.update(username=request.user.username)
            return self.retrieve(request, *args, **kwargs)
        if request.method == 'PATCH':
            self.kwargs.update(username=request.user.username)
            return self.partial_update(request, *args, **kwargs)
        if request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ModeMixinsAPIView(ViewSetMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    pass


class CategoriesViewSet(ModeMixinsAPIView):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["name", ]
    lookup_field = "slug"


class GenresViewSet(ModeMixinsAPIView):
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["name", ]
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(rating=Avg('reviews__score'))
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filter_class = TitlesFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(
                            Titles,
                            pk=self.kwargs.get('title_id')
                        )
                        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(title.reviews,
                                   pk=self.kwargs.get('review_id')
                                   )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=get_object_or_404(
                            Reviews,
                            pk=self.kwargs.get('review_id')
                        )
                        )
