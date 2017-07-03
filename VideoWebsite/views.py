# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import os
import asyncio
import threading
# from .videoManage import *
from .moviewer import *


class VideoNameUrl(object):
    name = ''
    url = ''

    def __int__(self):
        name = ''
        url = ''


def homepage(request):
    if request.method == 'GET':
        videoinfo = get_videos()
        videolist = []
        for i in range(len(videoinfo)):
            video_id = str(videoinfo[i].get_parts()[0].get_id())
            video_url = '/video/' + video_id
            newvideo = VideoNameUrl()
            newvideo.name = videoinfo[i].get_name()
            newvideo.url = video_url
            videolist.append(newvideo)
        context = {
            'videolist': videolist
        }
        return render(request, 'homepage.html', context)


def video(request, part_id):
    if request.method == 'GET':
        partinfo = PartInfo(part_id)
        videoinfo = partinfo.get_video()

        context = {
            'video_url': '/media/' + str(partinfo.get_id()) + '.mp4',
            'part_name': partinfo.get_name(),
            'video_name': videoinfo.get_name(),

        }
        return render(request, 'video.html', context)


def video_upload(request):
    if request.method == 'POST' and request.POST['video_name'] != '':
        videoinfo = add_video(request.POST['video_name'])
        # loop = asyncio.get_event_loop()
        # tasks = [print_sum(1,2),print_sum(3,4)]
        # loop.run_until_complete(asyncio.wait(tasks))
        # uploadvideo = request.FILES.get('svideo')
        # if not uploadvideo:
        #     context = {
        #         'message': 'no success!'
        #     }
        #     return render(request, 'homepage.html', context)
        # else:
        #     filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'sdfsa.mp4')
        #     fobj = open(filename, 'wb')
        #     for chrunk in uploadvideo.chunks():
        #         fobj.write(chrunk)
        #     fobj.close()
        #     context = {
        #         'message': 'success!'
        #     }
        #     return render(request, 'homepage.html', context)
        for i in range(1, int(request.POST['count'])+1):
            uploadvideo = request.FILES.get('video' + str(i))
            if not uploadvideo:
                context = {
                    'message': 'Please select video to upload!'
                }
                return render(request, 'uploadpage.html', context)
        # loop = asyncio.get_event_loop()
        # tasks = []
        # for i in range(1, int(request.POST['count'])+1):
        #     tasks.append(savevideo(request, request.POST['part_name' + str(i)]), request.FILES.get('video' + str(i)))
        # loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()
        # for i in range(1, int(request.POST['count'])+1):
        #     uploadvideo = request.FILES.get('video' + str(i))
        #     videofilename = request.POST['part_name' + str(i)] + '.mp4'
        #     filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'video', videofilename)
        #     fobj = open(filename, 'wb')
        #     for chrunk in uploadvideo.chunks():
        #         fobj.write(chrunk)
        #     fobj.close()
        for i in range(1, int(request.POST['count'])+1):
            uploadvideo = request.FILES.get('video' + str(i))
            partinfo = videoinfo.append_part(request.POST['part_name' + str(i)])
            videofilename = str(partinfo.get_id()) + '.mp4'
            filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'video', videofilename)
            fobj = open(filename, 'wb')
            for chrunk in uploadvideo.chunks():
                fobj.write(chrunk)
            fobj.close()
        context = {
            'message': 'Upload success!'
        }
        return render(request, 'uploadpage.html', context)


def test(request):
    return render(request, 'abc.html')


def uploadpage(request):
    if request.method == 'GET':
        return render(request, 'uploadpage.html')
