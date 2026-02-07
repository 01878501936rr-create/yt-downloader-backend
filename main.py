import yt_dlp
from flask import Flask, request, redirect, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '1080')

    if not video_url:
        return "URL is missing", 400

    # ১০৮০পি-র জন্য সেরা ভিডিও এবং অডিও স্ট্রীম খুঁজে বের করা
    ydl_opts = {
        'format': f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best',
        'quiet': True,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_direct_url = info.get('url')
            
            # ডাউনলোড করার জন্য হেডার সেট করা
            response = redirect(video_direct_url)
            response.headers['Content-Disposition'] = f'attachment; filename="video_{quality}p.mp4"'
            return response
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
