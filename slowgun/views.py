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
