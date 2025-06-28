# import subprocess
# import json

# url = 'https://www.youtube.com/watch?v=StRmUQsAByQ&pp=ygUDaGV5'
# videoInfo = json.loads(subprocess.run(f'yt-dlp --dump-json "{url}"', capture_output=True).stdout)

# title = videoInfo['title']
# thumbnail = videoInfo['thumbnail']
# desc = videoInfo['description']
# duration = videoInfo['duration']

# # hd_url = str()
# # for line in output['thumbnails']:
# #     if line['preference'] == 0:
# #         hd_url = line['url']

# # print(hd_url)

# ret = json.dumps({'title': title,
#             'thumbnail': thumbnail,
#             'description': desc,
#             'duration': duration})

from yt_dlp import YoutubeDL
import json

opts = {'continuedl': False,
         'extract_flat': 'discard_in_playlist',
         'fragment_retries': 10,
         'ignoreerrors': 'only_download',
         'no_warnings': True,
         'noplaylist': True,
         'noprogress': True,
         'outtmpl': {'default': 'video.%(ext)s', 'pl_thumbnail': ''},
         'overwrites': True,
         'postprocessors': [{'already_have_subtitle': False,
                             'key': 'FFmpegEmbedSubtitle'},
                            {'add_chapters': True,
                             'add_infojson': 'if_exists',
                             'add_metadata': True,
                             'key': 'FFmpegMetadata'},
                            {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
                            {'key': 'FFmpegConcat',
                             'only_multi_video': True,
                             'when': 'playlist'}],
         'quiet': True,
         'retries': 10,
         'simulate': False,
         'writesubtitles': True,
         'writethumbnail': True}
with YoutubeDL(opts) as ydl:
    # videoInfo = json.loads(subprocess.run(f'yt-dlp --force-overwrites --embed-subs --embed-thumbnail --embed-metadata --dump-json --no-playlist --output "video.%(ext)s" "{url}"', capture_output=True).stdout)
    url = "https://www.youtube.com/watch?v=StRmUQsAByQ&pp=ygUDaGV5"
    videoInfo = json.loads(json.dumps(ydl.sanitize_info(ydl.extract_info(url, download=False))))
    # for key, values in videoInfo.items():
    #     print(key, values)

    title = videoInfo['title']
    thumbnail = videoInfo['thumbnail']
    desc = videoInfo['description']
    duration = videoInfo['duration']

    videoPreviewInfo = {'title': title,
           'thumbnail': thumbnail,
           'description': desc,
           'duration': duration}
