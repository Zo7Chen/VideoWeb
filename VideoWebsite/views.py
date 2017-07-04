# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import os
# import asyncio
# import threading
# from .videoManage import *
from .moviewer import *
import re
from django.http import StreamingHttpResponse


class VideoNameUrl(object):
    name = ''
    url = ''
    ss_url = ''

    def __int__(self):
        pass


def homepage(request):
    if request.method == 'GET':
        videoinfo = get_videos()
        videolist = []
        for videos in videoinfo:
            video_id = videos.get_parts()[0].get_id_str()
            video_url = '/videos/' + video_id
            ss_url = '/media/' + videos.get_parts()[0].get_id_str() + '.jpg'
            newvideo = VideoNameUrl()
            newvideo.name = videos.get_name()
            newvideo.url = video_url
            newvideo.ss_url = ss_url
            videolist.append(newvideo)
        context = {
            'videolist': videolist
        }
        return render(request, 'homepage.html', context)


def uploadpage(request):
    return render(request, 'uploadpage.html')


class PartNameUrl :
    name = ''
    url = ''
    ss_url = ''
    def __int__(self):
        pass


class AdjacentPart :
    prev = ''
    next = ''
    def __int__(self):
        pass


def video(request, part_id):
    if request.method == 'GET':
        partinfo = PartInfo(int(part_id, 16))
        videoinfo = partinfo.get_video()
        
        parts = videoinfo.get_parts()
        
        adj_p = AdjacentPart()
        
        part_list = []
        
        for part in parts:
            newpart = PartNameUrl()
            newpart.name = part.get_name()
            newpart.url = '/videos/' + part.get_id_str()
            newpart.ss_url = '/media/' + part.get_id_str() + '.jpg'
            part_list.append(newpart)
            if part.get_order_num() == partinfo.get_order_num() - 1 :
                adj_p.prev = newpart.url
            if part.get_order_num() == partinfo.get_order_num() + 1 :
                adj_p.next = newpart.url

        context = {
            'video_url': '/media/' + partinfo.get_id_str() + '.mp4',
            'part_name': partinfo.get_name(),
            'video_name': videoinfo.get_name(),
            'part_list': part_list,
            'adj_p': adj_p
        }
        return render(request, 'video.html', context)


class DeleteVideoInfo(object):
    name = ''
    url = ''
    ss_url = ''
    part_id = ''
    def __int__(self):
        pass

def deletepage(request):
    if request.method == 'GET':
        all_video = get_videos()
        videolist = []
        for videos in all_video:
            video_node = DeleteVideoInfo()
            video_node.name = videos.get_name()
            video_node.url = '/videos/' + videos.get_parts()[0].get_id_str()
            video_node.ss_url = '/media/' + videos.get_parts()[0].get_id_str() + '.jpg'
            video_node.part_id = videos.get_parts()[0].get_id_str()
            videolist.append(video_node)
        context = {
            'videolist': videolist
        }
        return render(request, 'deletepage.html', context)


#########################################################################
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
            video_filename = partinfo.get_id_str() + '.mp4'
            vid_filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'video', video_filename)
            fobj = open(vid_filename, 'wb+')
            for chrunk in uploadvideo.chunks():
                fobj.write(chrunk)
            fobj.close()
            snapshot_filename = partinfo.get_id_str() + '.jpg'
            ss_filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'video', snapshot_filename)
            create_snapshot(vid_filename, ss_filename)
        context = {
            'message': 'Upload success!'
        }
        return render(request, 'uploadpage.html', context)


def video_delete(request):
    if request.method == 'POST':
        for part_list in request.POST.getlist('delete_list'):
            partinfo = PartInfo(int(part_list, 16))
            delete_videos = partinfo.get_video()
            for eachvideo in delete_videos.get_parts():
                delete_video_file = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                                                 'video', eachvideo.get_id_str() + '.mp4')
                if os.path.exists(delete_video_file):
                    os.remove(delete_video_file)
                delete_jpg_file = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                                               'video', eachvideo.get_id_str() + '.jpg')
                # print(delete_jpg_file)
                if os.path.exists(delete_jpg_file):
                    os.remove(delete_jpg_file)
            partinfo.get_video().del_this()

        videoinfo = get_videos()
        videolist = []
        for videos in videoinfo:
            video_id = videos.get_parts()[0].get_id_str()
            video_url = '/videos/' + video_id
            ss_url = '/media/' + videos.get_parts()[0].get_id_str() + '.jpg'
            newvideo = VideoNameUrl()
            newvideo.name = videos.get_name()
            newvideo.url = video_url
            newvideo.ss_url = ss_url
            videolist.append(newvideo)
        context = {
            'videolist': videolist
        }
        return render(request, 'homepage.html', context)

# def test(request):
#     return render(request, 'abc.html')


def file_download(request):
    # if request.method == 'GET':
    #     video_filename = os.path.join(os.path.abspath(os.path.dirname(__name__)),
    #                                   'video', str(re.findall(r'/media/(.*)\.mp4', request.GET['download_file'])[0]) + '.mp4')
    #     with open(video_filename, 'wb') as f:
    #         c = f.read()
    #     return HttpResponse(c)
    # def file_iterator(file_name, chunk_size=512):
    #     with open(file_name) as f:
    #         while True:
    #             c = f.read(chunk_size)
    #             if c:
    #                 yield c
    #             else:
    #                 break
    #
    # the_file_name = os.path.join(os.path.abspath(os.path.dirname(__name__)),
    #                              'video', str(re.findall(r'/media/(.*)\.mp4', request.GET['download_file'])[0]) + '.mp4')
    # response = StreamingHttpResponse(file_iterator(the_file_name))
    # response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    #
    # return response

    video_filename = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                                  'video', str(re.findall(r'/media/(.*)\.mp4', request.GET['download_file'])[0]) + '.mp4')

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    print(os.path.join(os.path.abspath(os.path.dirname(__name__)),
                       'video', str(re.findall(r'/media/(.*)\.mp4', request.GET['download_file'])[0]) + '.mp4'))
    partinfo = PartInfo(int(str(re.findall(r'/media/(.*)\.mp4', request.GET['download_file'])[0]), 16))
    response = StreamingHttpResponse(file_iterator(video_filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(partinfo.get_name() + '.mp4')

    return response
