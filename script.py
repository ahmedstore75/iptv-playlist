import os
import requests

# ১. Tapmad বা আপনার টার্গেট সোর্সের হেডার্স এবং লিংক
URL = "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/main/Tapmad_sm.m3u"
OUTPUT_FILE = "Tapmad_sm.m3u"

def fetch_and_update():
    try:
        # সোর্স থেকে নতুন ডাটা বা প্লেলিস্ট ফেচ করা
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=15)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            content = response.text
            
            # আপনার কোনো কাস্টম টোকেন বা ইউআরএল রিপ্লেস করতে চাইলে এখানে প্রসেস করতে পারেন
            # Example: content = content.replace("old_token", "new_token")

            # ফাইলে রাইট করা
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            print("Successfully updated playlist!")
        else:
            print("Failed to fetch valid M3U data.")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_and_update()
