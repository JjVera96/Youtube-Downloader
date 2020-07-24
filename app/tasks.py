from django.conf import settings

from celery import task
import json
from moviepy.editor import *
import pytube
import redis
from pytube.exceptions import PytubeError

from downloader.celery import app

redis_client = redis.StrictRedis.from_url(settings.BROKER_URL)

@task(bind=True)
def downloader_video(self, task_id, video_url, video_format):
    try:
        video = pytube.YouTube(video_url)
        video.streams.filter(file_extension='mp4', res='720p').first().download('../media')
        redis_client.publish(task_id, json.dumps({'response': 'Video descargado de Youtube al servidor y en proceso de convertir'}))
    except:
        return redis_client.publish(task_id, json.dumps({'error': 'Error al descargar video de Youtube al servidor'}))
    title = video.title.replace(',', '').replace('.', '').replace('/', '').replace('|', '').replace(':', '')
    if video_format == 'mp3':
        path = '../media/{}.{}'.format(title,'mp4')
        new_path = 'media/{}.{}'.format(title, 'mp3')
        try:
            video_mp4 = VideoFileClip(path)
            video_mp4.audio.write_audiofile('../' + new_path)   
            return redis_client.publish(task_id, json.dumps({'response': 'Video convertido a MP3', 'download_url': new_path, 'title': title}))
        except:
            return redis_client.publish(task_id, json.dumps({'error': 'Error al convertir en MP3'}))
    path = 'media/{}.{}'.format(title,'mp4')
    return redis_client.publish(task_id, json.dumps({'response': 'Video convertido a MP4', 'download_url': path, 'title': title}))
    
