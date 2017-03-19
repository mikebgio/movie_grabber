from __future__ import unicode_literals
import youtube_dl
import spinner

spin = spinner.Spinner()


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'downloading':
        spin.start()
    if d['status'] == 'finished':
        spin.stop()
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])

# known broken:
# https://www.youtube.com/watch?v=PFWkvvMxIXw
# known good:
# http://www.youtube.com/watch?v=BaW_jenozKc
