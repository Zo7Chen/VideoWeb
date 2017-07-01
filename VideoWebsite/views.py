# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    if request.method == 'GET':
        return render(request, 'homepage.html')


def video(request, video_id, part_id):
    if request.method == 'GET':
        video_uri = 'abc.mp4'

        context = {
            'video_url':video_id
        }
        return render(request, 'video.html', context)
