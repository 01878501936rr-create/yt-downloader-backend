from flask import Flask, request, redirect
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # যাতে অন্য কোনো সাইট থেকে ব্লক না হয়

@app.route('/download')
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '360') 

    if not video_url:
        return "No URL provided", 400

    ydl_opts = {
        # এই ফরম্যাটটি ১০৮০পি ভিডিও এবং অডিওকে একসাথে মার্জ করে সেরা কোয়ালিটি দিবে
        'format': f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_direct_url = info.get('url')
        return redirect(video_direct_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
