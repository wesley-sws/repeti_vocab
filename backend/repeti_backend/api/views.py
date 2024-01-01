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
from nltk.corpus import wordnet
from datetime import date


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
    verified_email = not user.email_verified #for now set to false, change when include email verification
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
    if CustomUser.objects.filter(username=request.data.get('username', None)).exists():
        return Response({'error' : 'Username already exists'}, status=400)
        # only include field's first name, last name, and username for update
    serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    serializer.save()
    return Response({'success': 'Your details have been updated'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_password(request):
    user = authenticate(username=request.user.username, password=request.data.get('password'))
    if user is None:
        return Response({'error': 'Authentication failed'}, status=401)
    return Response({'success': 'Authentication successful'})


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

# displays all synsets in user's vocabulary list, including their defintiion, examples and part of speech
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userlist(request):
    user_lists = UserList.objects.filter(user=request.user)
    serializer = UserListSerializer(user_lists, many=True)
    return Response(serializer.data) # includes related fields from AppSynset

# 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_word_synsets(request):
    word_synset_pairs = request.data.get('word_synset_pairs', []) # [] for default case

    # Process each pair and delete from UserList
    for pair in word_synset_pairs:
        word = pair.get('word')
        synset_id = pair.get('synset_id')

        # Find and delete the UserList entry
        user_list_entry = UserList.objects.filter(user=request.user, word=word, synset__synset_id=synset_id)
        user_list_entry.delete()

    return Response({'success': 'Word-synset pairs deleted'})

# 
@api_view(['GET'])
def load_definitions(request):
    word = request.GET.get('word', '')
    synsets = wordnet.synsets(word)
    if word == []:
        return Response({'error': 'You did not enter a word'}, status=400)
    details = []
    for syn in synsets:
        details.append({
            'synset_id' : syn.name(),
            'part_of_speech': syn.pos(),
            'definition': syn.definition(),
            'examples': syn.examples()
        })
    return Response(details)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_word_synset(request):
    syn = wordnet.synset.get(request.data.get('synset_id'))
    if syn == []:
        return Response({'error': 'Incorrect Synset'}, status=400)
    as_data = {
        'synset_id' : syn.name(),
        'definition': syn.definition(),
        'examples': syn.examples(),
        'part_of_speech': syn.pos()
    }
    as_serializer = AppSynsetSerializer(data=as_data) # Add to AppSynset
    if as_serializer.is_valid():
        as_serializer.save()
    else:
        return Response(as_serializer.errors, status=400)
    ul_serializer = UserListSerializer(data=request.data) # Add to UserList
    if ul_serializer.is_valid():
        ul_serializer.save()
    else:  
        return Response(ul_serializer.errors, status=400)
    # It remains to add the MCQOptions to the MCQOptions table 
    return Response({'success': 'Added to list'}, status=201)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_for_review(request):
    if WordReview.objects.filter(next_review_date=date.today()).exists():
        return Response(True)
    else:
        return Response(False)

def generate_quiz(request):
    if request.data.get('review') == True:
        pass
    def new_words_quiz():
        pass
    def new_words_flashcards():
        pass

def update_wordreview():
    pass
    



