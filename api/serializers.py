from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Categories, Comments, Genres, Reviews, Titles, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email',
                  'role')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['name', 'slug']
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['name', 'slug']
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True,
                                         slug_field='slug',
                                         queryset=Genres.objects.all())
    category = serializers.SlugRelatedField(many=False,
                                            slug_field='slug',
                                            queryset=Categories.objects.all())

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(required=False)
    category = CategoriesSerializer(many=False, read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False
    )

    def validate(self, data):
        view = self.context.get('view')
        if view.action == 'create':
            user = view.request.user
            title_id = view.kwargs.get('title_id')
            title = get_object_or_404(Titles, pk=title_id)
            if title.reviews.filter(author=user).exists():
                raise serializers.ValidationError('There can be only one')
        return data

    class Meta:
        model = Reviews
        exclude = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('author', 'review',)
