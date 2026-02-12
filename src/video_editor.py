import os
import PIL.Image
from moviepy.config import change_settings

# --- CONFIGURATION ---
# Ensure MoviePy finds ImageMagick
IMAGEMAGICK_BINARY = "/opt/homebrew/bin/magick"
if os.path.exists(IMAGEMAGICK_BINARY):
    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})
else:
    change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/magick"})
# ---------------------

# --- MONKEY PATCH ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# --------------------

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

class VideoEditor:
    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def create_clip(self, video_path, audio_path, text):
        try:
            # 1. Load Audio
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # 2. Load Video
            video_clip = VideoFileClip(video_path)
            
            # 3. Resize & Crop (Vertical 9:16)
            if video_clip.h != 1920:
                video_clip = video_clip.resize(height=1920)
            if video_clip.w > 1080:
                video_clip = video_clip.crop(x1=video_clip.w/2 - 540, y1=0, width=1080, height=1920)
            
            # 4. Sync Video to Audio Duration
            if video_clip.duration < duration:
                video_clip = video_clip.loop(duration=duration)
            else:
                video_clip = video_clip.subclip(0, duration)
            
            # 5. ATTACH AUDIO
            # We explicitly set the audio here
            video_clip = video_clip.set_audio(audio_clip)

            # 6. Add Subtitles
            try:
                # Use 'Arial' if available, otherwise 'Helvetica' (Mac safe)
                font = 'Arial-Bold'
                
                txt_clip = TextClip(
                    text, 
                    fontsize=70, 
                    color='yellow', 
                    stroke_color='black', 
                    stroke_width=3, 
                    font=font, 
                    size=(900, None), 
                    method='caption'
                )
                txt_clip = txt_clip.set_pos(('center', 0.8), relative=True).set_duration(duration)
                final_clip = CompositeVideoClip([video_clip, txt_clip])
                print(f"   ✅ Subtitle added: {text[:20]}...")
            except Exception as e:
                print(f"   ⚠️ TextClip failed: {e}")
                final_clip = video_clip

            return final_clip
            
        except Exception as e:
            print(f"❌ Error creating clip: {e}")
            return None

    def assemble_video(self, clips, final_filename):
        print("🎬 Concatenating all clips...")
        try:
            final_video = concatenate_videoclips(clips, method="compose")
            output_path = f"{self.output_folder}/{final_filename}"
            
            # AUDIO CHECK
            if final_video.audio is None:
                print("❌ WARNING: Final video has no audio track!")
            else:
                print("🔊 Audio track confirmed.")

            # WRITE VIDEO FILE
            # Switched audio_codec to 'libmp3lame' for maximum compatibility
            final_video.write_videofile(
                output_path, 
                fps=24, 
                codec='libx264', 
                audio_codec='libmp3lame',  # <--- CHANGED THIS
                audio_bitrate="192k",
                threads=4
            )
            return output_path
        except Exception as e:
            print(f"❌ Error assembling video: {e}")
            return None