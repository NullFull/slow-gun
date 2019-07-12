from django.http import JsonResponse
from django.shortcuts import render
import firebase_admin
from django.utils.timezone import now
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'slow-gun',
})


def index(request):
    return render(request, 'index.html')


def slogans(request):
    db = firestore.client()

    if request.method == 'GET':
        items = db.collection('slogans').get()
        return JsonResponse({
            'items': [slogan.to_dict() for slogan in items]
        })
    elif request.method == 'POST':
        content = request.POST.get('slogan', '')
        writer = request.POST.get('writer', '')

        print(content)
        print(writer)

        if not content:
            raise ValueError

        if len(content) > 100 or len(writer) > 20:
            raise ValueError  # TODO : 친절한 길이 오류 안내

        data = {
            'content': content,
            'writer': writer,
            'created': now(),
        }

        item = db.collection('slogans').document()
        item.set(data)

        return JsonResponse(data, status=201)
