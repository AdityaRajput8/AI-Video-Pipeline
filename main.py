import asyncio
import os
import shutil
from src.script_generator import ScriptGenerator
from src.voice_generator import VoiceGenerator
from src.media_fetcher import MediaFetcher
from src.video_editor import VideoEditor

async def main():
    # 1. Input Topic
    topic = input("🎥 Enter a video topic: ")
    
    # Initialize Tools
    script_gen = ScriptGenerator()
    voice_gen = VoiceGenerator()
    media_fetcher = MediaFetcher()
    editor = VideoEditor()

    # Ensure output folder exists for metadata
    os.makedirs("output", exist_ok=True)

    # 2. Generate Script
    print("\n🚀 Step 1: AI Script Generation...")
    script_data = script_gen.generate_script(topic)
    if not script_data:
        print("❌ Script generation failed.")
        return

    print(f"📝 Script generated with {len(script_data)} segments.")

    # --- NEW FEATURE: SEO METADATA GENERATION ---
    # Combine all script segments into one text block for analysis
    full_script_text = " ".join([seg['text'] for seg in script_data])
    metadata = script_gen.generate_metadata(topic, full_script_text)
    
    if metadata:
        with open("output/metadata.txt", "w") as f:
            f.write(f"TITLE: {metadata.get('title', 'No Title')}\n\n")
            f.write(f"DESCRIPTION:\n{metadata.get('description', 'No Description')}\n\n")
            f.write(f"TAGS:\n{metadata.get('tags', 'No Tags')}")
        print("✅ SEO Metadata saved to output/metadata.txt")
    # ---------------------------------------------

    # 3. Process Segments
    generated_clips = []
    
    for i, segment in enumerate(script_data):
        print(f"\n--- Processing Segment {i+1}/{len(script_data)} ---")
        
        # A. Voiceover
        audio_path = await voice_gen.generate_audio(segment['text'], f"segment_{i}.mp3")
        if not audio_path: continue
        
        # B. Get Duration for Video Search
        video_path = media_fetcher.download_video(segment['visual'], 5, f"segment_{i}.mp4")
        if not video_path: continue

        # C. Create Clip
        clip = editor.create_clip(video_path, audio_path, segment['text'])
        if clip:
            generated_clips.append(clip)

    # 4. Final Assembly
    if generated_clips:
        print("\n🔨 Step 4: Final Assembly...")
        output_file = editor.assemble_video(generated_clips, "final_video.mp4")
        print(f"\n✅ SUCCESS! Video saved at: {output_file}")
    else:
        print("\n❌ No clips were generated.")

    # Cleanup (Optional: remove temp files)
    # shutil.rmtree("assets/temp_audio")
    # shutil.rmtree("assets/temp_video")

if __name__ == "__main__":
    asyncio.run(main())