import re
import datetime
import requests
import pytz

OUTPUT_FILE = "Tapmad_sm.m3u"
RAW_M3U_URL = "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/main/Tapmad_sm.m3u"

def update_playlist():
    try:
        # ১. বাংলাদেশ সময় বের করা
        bd_tz = pytz.timezone('Asia/Dhaka')
        current_bd_time = datetime.datetime.now(bd_tz).strftime("%Y-%m-%d %H:%M:%S")

        # ২. সোর্স থেকে প্লেলিস্ট ফেচ করা
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(RAW_M3U_URL, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Failed to fetch source playlist. Status code: {response.status_code}")
            return

        raw_text = response.text.strip()

        # ৩. হেডার ব্লকের পর থেকে শুধু চ্যানেল সংক্রান্ত লাইনগুলো বের করে নেওয়া
        lines = raw_text.splitlines()
        clean_lines = []
        skip_header = True

        for line in lines:
            line_str = line.strip()
            # হেডার বা পুরোনো কমেন্ট বাদ দেওয়া
            if skip_header and (line_str.startswith("#EXTM3U") or line_str.startswith("#=") or line_str.startswith("#  ")):
                continue
            skip_header = False
            if line_str:
                clean_lines.append(line_str)

        # ৪. সঠিকভাবে মোট চ্যানেলের সংখ্যা গণনা করা (#EXTINF গণনা করে)
        channel_count = sum(1 for line in clean_lines if line.startswith("#EXTINF:"))

        # ৫. আপনার হুবহু ফরম্যাটে নতুন হেডার তৈরি করা
        header = f"""#EXTM3U
#=================================
#  Developed by: Ahammad Ali
#  Telegram: https://t.me/banglatvlivefree
#  Last Updated: {current_bd_time} (BD Time)
#  Channels Count: {channel_count}
#=================================
"""

        # ৬. হেডার এবং চ্যানেলের ডাটা যুক্ত করে ফাইলে সেভ করা
        channels_body = "\n".join(clean_lines)
        final_playlist = f"{header}\n{channels_body}\n"

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_playlist)

        print(f"Playlist successfully updated! Total Channels: {channel_count}")

    except Exception as e:
        print(f"Error occurred while updating playlist: {e}")

if __name__ == "__main__":
    update_playlist()
