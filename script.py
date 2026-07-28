import datetime
import requests
import pytz  # BD TimeZone এর জন্য

OUTPUT_FILE = "Tapmad_sm.m3u"

# আপনার M3U প্লেলিস্টের ডাটা (সরাসরি সোর্স ইউআরএল থাকলে এখানে বসাতে পারেন)
RAW_M3U_URL = "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/main/Tapmad_sm.m3u"

def generate_playlist():
    try:
        # বাংলাদেশ সময় নির্ধারণ
        bd_tz = pytz.timezone('Asia/Dhaka')
        current_bd_time = datetime.datetime.now(bd_tz).strftime("%Y-%m-%d %H:%M:%S")

        # সোর্স থেকে প্লেলিস্ট ডাউনলোড করা
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(RAW_M3U_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            lines = response.text.splitlines()
        else:
            print("Failed to fetch M3U playlist from source.")
            return

        # চ্যানেল সংখ্যা গণনা (#EXTINF দিয়ে যতগুলো চ্যানেল শুরু হয়েছে)
        channel_count = sum(1 for line in lines if line.strip().startswith("#EXTINF:"))

        # বডি থেকে পুরনো হেডার/কমেন্ট বাদ দিয়ে শুধু চ্যানেলের অংশ আলাদা করা
        channel_body_lines = []
        for line in lines:
            if line.strip().startswith("#EXTM3U") or line.strip().startswith("#="):
                continue
            channel_body_lines.append(line)

        # আপনার পছন্দমত কাস্টম হেডার তৈরি
        custom_header = f"""#EXTM3U
#=================================
#  Developed by: Ahammad Ali
#  Telegram: https://t.me/banglatvlivefree
#  Last Updated: {current_bd_time} (BD Time)
#  Channels Count: {channel_count}
#=================================
"""

        # নতুন কাস্টম হেডার ও চ্যানেল লিস্ট একত্র করা
        full_playlist_content = custom_header + "\n".join(channel_body_lines)

        # ফাইলে সেভ করা
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(full_playlist_content.strip() + "\n")

        print(f"Playlist successfully updated! Channels found: {channel_count}")

    except Exception as e:
        print(f"Error updating playlist: {e}")

if __name__ == "__main__":
    generate_playlist()
