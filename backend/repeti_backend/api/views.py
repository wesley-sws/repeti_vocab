from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .models import *
from .serializers import *


@api_view(['POST'])
# Later change to include email verification, but for now register user without it
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if CustomUser.objects.filter(username=request.data.get('username', None)).exists():
        return Response({'error' : 'Username already exists'}, status=400)
    if request.data.get('password', None) != request.data.get('confirm_password', None):
        return Response({'error': 'Password does not match'}, status=400)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    serializer.save()
    return Response({'success': 'User registered successfully'}, status=201)


@api_view(['POST'])
def login_user(request):
    # Authenticate the user based on username and password
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    # Also need to check user's email is verified
    verified_email = not user.email_verified #for now set to false
    if user is not None and verified_email:
        # Token is sent to the frontend and included in subsequent HTTP requests for processing
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    elif user is not None and not verified_email:
        return Response({'error': 'Email has not been verified.'}, status=403)
    else:
        return Response({'error': 'Invalid username or password'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Successfully logged out."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_details(request):
    return Response(CustomUserSerializer(request.user).data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_details(request):
    # only include field's first name, last name, and username for update
    serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
    if CustomUser.objects.filter(username=request.data.get('username', None)).exists():
        return Response({'error' : 'Username already exists'}, status=400)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    serializer.save()
    return Response({'success': 'Your details have been updated'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_password(request):
    user = authenticate(username=request.user.username, password=request.data.get('password'))
    if user is None:
        return Response({'error': 'Incorrect password'}, status=401)
    return Response({'success': 'Enter your new password'})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    if new_password != confirm_password:
        return Response({'error': 'Passwords do not match.'}, status=400)
    if not new_password:
        return Response({'error': 'New password should not be empty.'}, status=400)
    # Set the new password with hashing included
    user.set_password(new_password)
    user.save()
    return Response({'success': 'Your password has been updated'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userlist(request):
    user_lists = UserList.objects.filter(user=request.user)
    serializer = UserListSerializer(user_lists, many=True)
    return Response(serializer.data) # includes related fields from AppSynset


@api_view(['GET'])
def load_definitions(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_word_synset(request):
    pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_word_synset(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_quiz(request):
    pass



