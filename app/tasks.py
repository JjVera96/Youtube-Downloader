from django.conf import settings

from celery import task
from moviepy.editor import *
import pytube
import pytube
import redis

from downloader.celery import app

redis_client = redis.StrictRedis.from_url(settings.BROKER_URL)

@task(bind=True)
def downloader_video(self, task_id, video_url):
    print(video_url)
    video = pytube.YouTube(video_url)
    print('Descargando video', video_url)
    video.streams.filter(file_extension='mp4').first().download('../media')
    titulo = video.title.replace(',', 'mp4')
    path = '../media{}.{}'.format(titulo,'mp4')
    nuevo_path = '../media{}.{}'.format(titulo, 'mp3')
    print('Convirtiendo video', video_url)
    video_mp4 = VideoFileClip(path)
    video_mp4.audio.write_audiofile(nuevo_path)
    print('Guardado audio', video_url)
    return redis_client.publish(task_id, json.dumps({'title': 'media/{titulo}.mp3'}))