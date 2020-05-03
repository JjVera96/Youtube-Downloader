from django.conf import settings

from celery import task
import json
from moviepy.editor import *
import pytube
import redis

from downloader.celery import app

redis_client = redis.StrictRedis.from_url(settings.BROKER_URL)

@task(bind=True)
def downloader_video(self, task_id, video_url):
    try:
        video = pytube.YouTube(video_url)
        video.streams.filter(file_extension='mp4').first().download('../media')
        redis_client.publish(task_id, json.dumps({'response': 'Video descargado de Youtube al servidor y en proceso de convertir a MP3'}))
    except:
        return redis_client.publish(task_id, json.dumps({'error': 'Error al descargar video de Youtube al servidor'}))
    title = video.title.replace(',', '').replace('.', '').replace('/', '').replace('|', '')
    path = '../media/{}.{}'.format(title,'mp4')
    new_path = 'media/{}.{}'.format(title, 'mp3')
    try:
        video_mp4 = VideoFileClip(path)
        video_mp4.audio.write_audiofile('../' + new_path)
        return redis_client.publish(task_id, json.dumps({'response': 'Video convertido a MP3', 'download_url': new_path, 'title': tile}))
    except:
        return redis_client.publish(task_id, json.dumps({'error': 'Error al convertir en MP3'}))
    
