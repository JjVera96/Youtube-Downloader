from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

import json

from app.tasks import *

# Create your views here.
class IndexView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications_url'] = settings.NOTIFICATIONS_URL
        return context


def downloadVideo(request):
    data = json.loads(request.GET.get('data'))
    task_id = downloader_video.delay(data['uuid'], data['video_url'])
    return HttpResponse(json.dumps({'Ok': 'Ok'}))

        