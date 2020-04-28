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
    print(video_url)
    video = pytube.YouTube(video_url)
    print('Descargando video', video_url)
    video.streams.filter(file_extension='mp4').first().download('../media')
    title = video.title.replace(',', 'mp4')
    path = '../media/{}.{}'.format(title,'mp4')
    new_path = 'media/{}.{}'.format(title, 'mp3')
    print('Convirtiendo video', video_url)
    video_mp4 = VideoFileClip(path)
    video_mp4.audio.write_audiofile('../' + new_path)
    print('Guardado audio', video_url)
    return redis_client.publish(task_id, json.dumps({'download_url': new_path}))
