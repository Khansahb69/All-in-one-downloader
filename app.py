from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = 'downloads'

# Ensure folder exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    
    # Generate unique filename
    filename = f"video_{uuid.uuid4().hex}.mp4"
    filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    
    # yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': filepath,
        'noplaylist': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False
    )
