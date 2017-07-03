# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import os


def homepage(request):
    if request.method == 'GET':
        return render(request, 'homepage.html')


def video(request, video_id, part_id):
    if request.method == 'GET':
        video_uri = 'abc.mp4'

        context = {
            'video_url': video_id
        }
        return render(request, 'video.html', context)


def video_upload(request):
    if request.method == 'POST' and request.POST['video_name'] != '':
        uploadvideo = request.FILES.get('svideo')
        if not uploadvideo:
            context = {
                'message': 'no success!'
            }
            return render(request, 'homepage.html', context)
        else:
            filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'sdfsa.mp4')
            fobj = open(filename, 'wb')
            for chrunk in uploadvideo.chunks():
                fobj.write(chrunk)
            fobj.close()
            context = {
                'message': 'success!'
            }
            return render(request, 'homepage.html', context)


def test(request):
    return render(request, 'abc.html')


def uploadpage(request):
    if request.method == 'GET':
        return render(request, 'uploadpage.html')
