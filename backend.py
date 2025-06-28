from flask import Flask, request
from flask_cors import cross_origin, CORS
from yt_dlp import YoutubeDL
import json

app = Flask(__name__)

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

        title = videoInfo['title']
        thumbnail = videoInfo['thumbnail']
        desc = videoInfo['description']
        duration = videoInfo['duration']

        return {'title': title,
                'thumbnail': thumbnail,
                'description': desc,
                'duration': duration}

@app.route('/download/<path:url>', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def download(url):
    return 'You pressed the download button'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
