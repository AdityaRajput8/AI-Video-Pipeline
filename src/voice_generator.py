import asyncio
import edge_tts

class VoiceGenerator:
    def __init__(self, output_folder="assets/temp_audio"):
        self.output_folder = output_folder
        self.voice = "en-US-ChristopherNeural"  # Deep, professional male voice
        # self.voice = "en-US-AriaNeural"     # Alternative: Professional female voice

    async def generate_audio(self, text, filename):
        output_path = f"{self.output_folder}/{filename}"
        print(f"🎙️ Generating audio: {filename}...")
        
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return None

# Test block
if __name__ == "__main__":
    import os
    # Create folder if running directly
    os.makedirs("assets/temp_audio", exist_ok=True)
    
    gen = VoiceGenerator()
    text = "This is a test of the AI video pipeline using Python."
    asyncio.run(gen.generate_audio(text, "test_audio.mp3"))
    print("✅ Audio generated in assets/temp_audio/test_audio.mp3")