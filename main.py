from flask import Flask, request, redirect
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '360') 

    if not video_url:
        return "No URL provided", 400

    # ১০৮০পি প্লে না হলে এটি অটোমেটিক সেরা এভেইলএবল কোয়ালিটি নিয়ে নিবে
    ydl_opts = {
        'format': f'best[height<={quality}][ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_direct_url = info.get('url')
            return redirect(video_direct_url)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
