from flask import Flask, request, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '360') # ডিফল্ট ৩৬০পি

    if not video_url:
        return "No URL provided", 400

    ydl_opts = {
        # কোয়ালিটি অনুযায়ী ফরম্যাট সিলেক্ট করবে
        'format': f'best[height<={quality}][ext=mp4]/best[ext=mp4]',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_direct_url = info.get('url')
        return redirect(video_direct_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
