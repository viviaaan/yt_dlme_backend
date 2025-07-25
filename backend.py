import re
from flask import Flask, request, send_from_directory, send_file
from flask_cors import cross_origin
from yt_dlp import YoutubeDL
import json
from os import getcwd
from os.path import join

app = Flask(__name__, static_folder='data')

@app.route('/preview/<path:url>', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def query(url):
    opts = {'extract_flat': 'discard_in_playlist',
             'fragment_retries': 10,
             'ignoreerrors': 'only_download',
             'no_warnings': True,
             'noplaylist': True,
             'noprogress': True,
             'postprocessors': [{'key': 'FFmpegConcat',
                                 'only_multi_video': True,
                                 'when': 'playlist'}],
             'quiet': True,
             'retries': 10,
             'simulate': True}
    with YoutubeDL(opts) as ydl:
        videoInfo = ydl.sanitize_info(ydl.extract_info(url, download=False))
        resolutions = map(lambda format: format['resolution'],  videoInfo['formats'])

        return {
                'title': videoInfo['title'],
                'id': videoInfo['id'],
                'channel': videoInfo['channel'],
                'channel_url': videoInfo['channel_url'],
                'thumbnail': videoInfo['thumbnail'],
                'resolutions': list(set(resolutions)),
                'description': videoInfo['description'],
                'duration': videoInfo['duration'],
                'view_count': videoInfo['view_count'],
                'like_count': videoInfo['like_count'],
                }

@app.route('/download/<path:url>', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def download(url):
    def progressHook(progressInfo):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        if progressInfo['status'] == 'downloading':
            percent = ansi_escape.sub('', progressInfo['_percent_str'])
            eta = ansi_escape.sub('', progressInfo['_eta_str'])
            if progressInfo['info_dict'].get('id') != None:
                with open(f"status\\{progressInfo['info_dict']['id']}", 'w') as statusfile:
                    statusfile.write(json.dumps({'percent': percent, 'eta': eta}))
        elif progressInfo['status'] == 'finished':
            if progressInfo['info_dict'].get('id') != None:
                with open(f"status\\{progressInfo['info_dict']['id']}", 'w') as statusfile:
                    statusfile.write('finished')

    res = request.args.get('res')
    opts = {'continuedl': False,
             'extract_flat': 'discard_in_playlist',
             'format_sort': [f'res:{res}', '+size'],
             'fragment_retries': 10,
             'ignoreerrors': 'only_download',
             'no_warnings': True,
             'merge_output_format': 'mkv',
             'noplaylist': True,
             'noprogress': True,
             'outtmpl': {'default': 'data/%(id)s.mkv', 'pl_thumbnail': ''},
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
             'quiet': False,
             'progress_hooks': [progressHook],
             'retries': 10,
             'simulate': False,
             'writesubtitles': True,
             'writeautomaticsub': True,
             'writethumbnail': True}
    with YoutubeDL(opts) as ydl:
        videoInfo = ydl.sanitize_info(ydl.extract_info(url, download=True))
        filename = videoInfo['id'] + '.mkv'
        print(f'sending {filename}')

        return send_file(join(getcwd(), 'data', filename), as_attachment=True)

@app.route('/progress/<id>', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def progress(id):
    with open(f'status\\{id}', 'r') as statusfile:
        content = statusfile.read()
    if content != 'finished':
        try:
            progressInfo = json.loads(content)
            return progressInfo
        except:
            return '0.0%'
    else:
        return 'finished'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
