import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API Key not found. Check your .env file.")
        
        self.client = Groq(api_key=self.api_key)

    def generate_script(self, topic):
        print(f"🧠 Brainstorming script for: {topic} (using Groq Llama-3)...")
        
        prompt = f"""
        You are a professional YouTube Short scriptwriter.
        Create a compelling, fast-paced 30-second script about: '{topic}'.
        
        STRICT OUTPUT FORMAT (JSON ONLY):
        Return a raw JSON list of objects. Do not include markdown formatting or explanations.
        
        Structure:
        [
            {{
                "text": "The exact spoken words for the voiceover.",
                "visual": "A precise, 3-word description for stock footage search (e.g., 'futuristic city', 'coding laptop').",
                "duration": 5
            }},
            ... (repeat for 4-5 segments)
        ]
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a JSON-only API. specific valid JSON output only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            raw_content = completion.choices[0].message.content
            
            # Clean the response (remove Markdown if Llama adds it)
            clean_text = raw_content.strip()
            if "```json" in clean_text:
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_text:
                clean_text = clean_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            return json.loads(clean_text)

        except Exception as e:
            print(f"❌ Error generating script with Groq: {e}")
            return None

if __name__ == "__main__":
    generator = ScriptGenerator()
    script = generator.generate_script("The history of AI")
    if script:
        print(json.dumps(script, indent=2))
    else:
        print("Test failed.")