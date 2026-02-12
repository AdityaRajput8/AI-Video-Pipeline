import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MediaFetcher:
    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")
        if not self.api_key:
            raise ValueError("Pexels API Key not found.")
        
        self.headers = {'Authorization': self.api_key}

    def download_video(self, query, duration, filename):
        print(f"🔍 Searching Pexels for: '{query}'...")
        
        # Search specifically for vertical videos (9:16) for Shorts/Reels
        # If you want landscape, change orientation to 'landscape'
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=portrait&size=medium"
        
        try:
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            if not data.get('videos'):
                print(f"⚠️ No videos found for '{query}'. Trying generic backup...")
                return self.download_video("technology abstract", duration, filename)

            # Logic: Find a video that is at least as long as the segment needed
            # to avoid looping too much.
            best_video = data['videos'][0]
            for video in data['videos']:
                if video['duration'] >= duration:
                    best_video = video
                    break
            
            video_file_url = best_video['video_files'][0]['link']
            
            # Download
            print(f"⬇️ Downloading video...")
            video_content = requests.get(video_file_url).content
            
            output_path = f"assets/temp_video/{filename}"
            with open(output_path, 'wb') as f:
                f.write(video_content)
                
            return output_path

        except Exception as e:
            print(f"❌ Error fetching video: {e}")
            return None

# Test block
if __name__ == "__main__":
    fetcher = MediaFetcher()
    # Ensure folder exists
    os.makedirs("assets/temp_video", exist_ok=True)
    fetcher.download_video("coding laptop", 5, "test_video.mp4")
    print("✅ Video downloaded to assets/temp_video/test_video.mp4")