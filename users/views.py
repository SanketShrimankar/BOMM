from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer, CommentSerializer, LikeSerializer
from .models import NewUser, Comments, Likes
from rest_framework.decorators import api_view
from django.http import JsonResponse
import datetime
from django.db.models import Sum


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def get(self, format='json'):
        users = NewUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, id, format='json'):
        serializer = CustomUserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return JsonResponse(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def UserUpdate(request, pk):
    user = NewUser.objects.get(id=pk)
    serializer = CustomUserSerializer(
        instance=user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        user_catalogue = user.catalogue
        data = [serializer.data, user_catalogue]
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
def userdetailview(request, pk):
    user = NewUser.objects.get(id=pk)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentsCreateRetrieve(APIView):

    permission_classes = [AllowAny]

    def get(self, format='json'):
        c = Comments.objects.all()
        serializer = CommentSerializer(c, many=True)
        return Response(serializer.data)

    def post(self, id, format='json'):
        serializer = CommentSerializer(
            data=self.request.data)
        if serializer.is_valid():
            comment = serializer.save()
            if comment:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
def BookComments(request, pk):
    c = Comments.objects.filter(bid=pk)
    serializer = CommentSerializer(c, many=True)
    data = {}
    # data['name'] = "Sanket"
    data = serializer.data
    for item in serializer.data:
        user = NewUser.objects.get(id = item['uid'])
        item['name'] = user.user_name
        print(item)
        # data.update(item)
    return Response(data)


class LikeUpdate(APIView):

    def get(self, id, pk, uid, format='json'):
        if Likes.objects.filter(bid=pk).exists():
            book = Likes.objects.filter(bid=pk)
            user = book.get(uid=uid)
            
            serializer = LikeSerializer(instance = user)
            no_of_likes = book.aggregate(Sum('total_likes'))
            if no_of_likes == 'null':
                no_of_likes = 0  
            data = dict(serializer.data)
            data.update(no_of_likes)
            return Response(data)
        return Response({'error': 'Book doesnt exists', 'total_likes__sum': 0})

    def post(self, id, format='json'):
        val = self.request.data['liked']
        if Likes.objects.filter(bid=self.request.data['bid']).exists() and val == 'True':
            book = Likes.objects.filter(bid=self.request.data['bid'], uid=self.request.data['uid'])
            liked_book = Likes.objects.filter(bid = self.request.data['bid'])
            if book.exists():
                user = liked_book.get(uid = self.request.data['uid'])
                serializer = LikeSerializer(instance=user, data=self.request.data)
            else:   
                serializer = LikeSerializer(data=self.request.data)
        else:
            if val == 'True':
                serializer = LikeSerializer(data=self.request.data)

        if serializer.is_valid():
            serializer.save()
            book = Likes.objects.filter(bid=self.request.data['bid'])
            no_of_likes = book.aggregate(Sum('total_likes'))
            data = dict(serializer.data)
            data.update(no_of_likes)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, format='json'):
        book = Likes.objects.filter(bid=self.request.data['bid'])
        user = book.get(uid=self.request.data['uid'])
        serializer = LikeSerializer(
            instance=user, data=self.request.data, partial=True)
        if serializer.is_valid():
            json = serializer.save()
            book = Likes.objects.filter(bid=self.request.data['bid'])
            no_of_likes = book.aggregate(Sum('total_likes'))
            data = dict(serializer.data)
            data.update(no_of_likes)
            """ data.update(serializer.data)
            data.update(no_of_likes) """
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def CatalogueRemove(request, pk):
    user = NewUser.objects.get(id=pk)
    serializer = CustomUserSerializer(instance = user)
    book_id = request.data['catalogue']
    #if serializer:
    if book_id in user.catalogue:
        user.catalogue.remove(book_id)
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getCatalogue(request, id, pk):
    user = NewUser.objects.get(id=id)
    book_id = pk 
    if user.catalogue is not None and book_id in user.catalogue:
        return Response({'val': True})
    return Response({'val': False})

@api_view(['GET'])
def UserCatalogue(request, id):
    user = NewUser.objects.get(id=id)
    #serializer = CustomUserSerializer(instance=user.catalogue)
    if user:
        return Response(user.catalogue)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getLikeCount(request, pk):
    book = Likes.objects.filter(bid=pk)
    no_of_likes = book.aggregate(Sum('total_likes'))
    return Response(no_of_likes)