# 🎬 AI Shorts Generator (AutoVid Pipeline)

An end-to-end automated pipeline that generates vertical YouTube Shorts from a single text prompt. 

## 🚀 Technical Architecture
The system follows a modular **Chain-of-Thought** architecture:
1.  **Scripting Engine:** Utilizes **Groq (Llama-3.3-70b)** for sub-second script generation, optimized for viral retention.
2.  **Audio Engine:** **Edge-TTS** for neural voice synthesis (en-US-ChristopherNeural).
3.  **Visual Engine:** **Pexels API** for semantic stock footage matching.
4.  **Post-Production:** **MoviePy** & **ImageMagick** for programmatic editing, resizing (9:16), and dynamic subtitle generation.

## 🔥 New Features (v2.0)
* **Automated SEO Suite:** The pipeline now analyzes the generated script using Llama-3 to automatically create:
    * Viral Clickbait Titles
    * SEO-Optimized Video Descriptions
    * High-Ranking Tags
    * *Output saved to `output/metadata.txt`*

## 🛠️ Key Solved Challenges
* **API Rate Limits:** Migrated from Gemini 1.5 Flash to **Groq Llama-3.3** to resolve persistent 429/404 errors and ensure 99.9% uptime.
* **Library Conflicts:** Implemented a custom monkey-patch for `Pillow` to resolve the `Image.ANTIALIAS` deprecation issue in MoviePy.
* **Cross-Platform Audio:** Forced `libmp3lame` codec to solve silent audio rendering issues on macOS Silicon.

## 📦 Installation
```bash
git clone [https://github.com/AdityaRajput8/AI-Video-Pipeline.git](https://github.com/AdityaRajput8/AI-Video-Pipeline.git)
cd AI-Video-Pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Install ImageMagick (Required for subtitles)
brew install imagemagick ghostscript
⚡ Usage
Bash

python main.py
# Enter topic: "The Future of AI"
# Output: final_video.mp4 + metadata.txt (SEO tags)