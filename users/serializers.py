from rest_framework import serializers
from users.models import NewUser, Comments, Likes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
import datetime


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        """ last_login = self.user.created_at
        self.user.created_at = datetime.datetime.now() """
        """ self.user.created_at = datetime.datetime.now()
        Custom data you want to include
        data.update({'user': self.user.user_name})
        data.update({'id': self.user.id}) """
        if (self.user.login_count != 0):
            data.update({'last_login': self.user.created_at})
            data.update({'user': self.user.user_name})
            data.update({'id': self.user.id})
            data.update({'image': self.user.image.url})
            data.update({'catalogue': self.user.catalogue})
            data.update({'fav_genre': self.user.fav_genre})
            data.update({'stauts': self.user.status})
            self.user.created_at = datetime.datetime.now()
            self.user.login_count = self.user.login_count + 1
            self.user.save()
            return data
        else:
            data.update({'last_login': self.user.created_at})
            data.update({'user': self.user.user_name})
            data.update({'id': self.user.id})
            data.update({'Count': self.user.login_count})
            data.update({'Fav Genre': self.user.fav_genre})
            data.update({'Fav Author': self.user.fav_author})
            data.update({'State': self.user.state})
            data.update({'country': self.user.country})
            data.update({'About': self.user.about_me})
            self.user.created_at = datetime.datetime.now()
            self.user.login_count = self.user.login_count + 1
            self.user.save()
            return data


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8)
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = NewUser
        fields = ('user_name', 'email', 'password', 'fav_genre',
                  'fav_author', 'about_me', 'genre', 'catalogue', 'curr_reading', 'readed', 'state', 'country', 'image', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value != "":
                if attr == 'password':
                    self.instance.set_password(value)
                elif attr == 'catalogue':
                    self.instance.catalogue += value
                else:
                    setattr(instance, attr, value)

        self.instance.save()
        return self.instance


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('bid', 'uid', 'body', 'created_at')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = ('bid', 'uid', 'liked', 'total_likes')

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.total_likes = 1
        instance.save()
        return instance

    def update(self, instance, validated_data):
        self.instance.liked = validated_data.get('liked')
        is_liked = validated_data['liked']
        if is_liked == False or is_liked == 'false':
            self.instance.total_likes = 0
        else:
            self.instance.total_likes = 1
        instance.save()
        return instance
