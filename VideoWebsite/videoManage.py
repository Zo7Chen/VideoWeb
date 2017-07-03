import asyncio
import threading
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext


async def savevideo(request, partid, partvideo):
    videofilename = partid + '.mp4'
    filename = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'video', videofilename)
    fobj = open(filename, 'wb')
    await saving(fobj,partvideo)
    return render(request, 'uploadpage.html', {'message':partid+' success!'})

async def saving(fobj, partvideo):
    for chrunk in partvideo.chunks():
        fobj.write(chrunk)
    fobj.close()
