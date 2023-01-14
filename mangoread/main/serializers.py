from rest_framework import serializers

from main.models import Manga, Genre, Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name',)


class MangaListSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        model = Manga
        fields = ('name', 'year', 'genre', 'main_photo')


class MangaDetailSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        model = Manga
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("user", "stars", 'text', 'id')

    def get_user(self, obj):
        return obj.user.nickname


class ReviewCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200, required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=True)

    def create(self, validated_data):
        manga = Manga.objects.get(id=self.context['view'].kwargs.get('pk'))
        print(validated_data)
        if Review.objects.filter(user=validated_data['user']).count() > 0:
            raise serializers.ValidationError({'message':'You already have review for this manga'})
        return Review.objects.create(**validated_data, manga=manga)