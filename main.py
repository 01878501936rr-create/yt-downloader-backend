import yt_dlp
from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '720')

    if not video_url:
        return "URL is missing", 400

    # ব্লকিং এড়ানোর জন্য নতুন সেটিংস
    ydl_opts = {
        'format': f'best[height<={quality}][ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.youtube.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_direct_url = info.get('url')
            return redirect(video_direct_url)
    except Exception as e:
        # এরর মেসেজটি সরাসরি ব্রাউজারে দেখাবে যাতে আপনি বুঝতে পারেন কী সমস্যা
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
