# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    if request.method == 'GET':
        return render(request, 'homepage.html')


def video(request, video_id):
    if request.method == 'GET':
        video_uri = 'abc'
        if video_id == video_uri:
            return render(request, 'video.html', video_uri)
