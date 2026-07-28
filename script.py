import json
import datetime
import requests
import pytz

M3U_OUTPUT_FILE = "Tapmad_sm.m3u"
JSON_OUTPUT_FILE = "Tapmad_sm.json"
RAW_M3U_URL = "https://raw.githubusercontent.com/sm-monirulislam/Tapmad_Auto_Update_Playlist/main/Tapmad_sm.m3u"

def parse_and_update_playlists():
    try:
        # ১. বাংলাদেশ সময় বের করা
        bd_tz = pytz.timezone('Asia/Dhaka')
        current_bd_time = datetime.datetime.now(bd_tz).strftime("%Y-%m-%d %H:%M:%S")

        # ২. সোর্স থেকে M3U ডাটা ফেচ করা
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(RAW_M3U_URL, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Failed to fetch source playlist. Status code: {response.status_code}")
            return

        raw_text = response.text.strip()
        lines = raw_text.splitlines()

        # ৩. প্রসেসিং ও এক্সট্রাকশন
        clean_m3u_lines = []
        channels_json_data = []
        skip_header = True

        current_channel_info = {}

        for line in lines:
            line_str = line.strip()

            # হেডার বা পুরোনো কমেন্ট বাদ দেওয়া
            if skip_header and (line_str.startswith("#EXTM3U") or line_str.startswith("#=") or line_str.startswith("#  ")):
                continue
            skip_header = False

            if not line_str:
                continue

            clean_m3u_lines.append(line_str)

            # EXTINF লাইন পার্স করা
            if line_str.startswith("#EXTINF:"):
                current_channel_info = {}
                
                # tvg-id বের করা
                if 'tvg-id="' in line_str:
                    current_channel_info['id'] = line_str.split('tvg-id="')[1].split('"')[0]
                else:
                    current_channel_info['id'] = ""

                # tvg-logo বের করা
                if 'tvg-logo="' in line_str:
                    current_channel_info['logo'] = line_str.split('tvg-logo="')[1].split('"')[0]
                else:
                    current_channel_info['logo'] = ""

                # group-title বের করা
                if 'group-title="' in line_str:
                    current_channel_info['group'] = line_str.split('group-title="')[1].split('"')[0]
                else:
                    current_channel_info['group'] = ""

                # চ্যানেলের নাম বের করা
                if ',' in line_str:
                    current_channel_info['name'] = line_str.split(',', 1)[1].strip()
                else:
                    current_channel_info['name'] = "Unknown Channel"

            # ইউআরএল / লিঙ্ক লাইন পার্স করা
            elif line_str.startswith("http://") or line_str.startswith("https://"):
                if current_channel_info:
                    current_channel_info['url'] = line_str
                    channels_json_data.append(current_channel_info)
                    current_channel_info = {}

        # ৪. চ্যানেলের মোট সংখ্যা গণনা
        channel_count = len(channels_json_data)

        # ৫. M3U ফাইল তৈরি
        m3u_header = f"""#EXTM3U
#=================================
#  Developed by: Ahammad Ali
#  Telegram: https://t.me/banglatvlivefree
#  Last Updated: {current_bd_time} (BD Time)
#  Channels Count: {channel_count}
#=================================
"""
        m3u_content = m3u_header + "\n".join(clean_m3u_lines) + "\n"
        with open(M3U_OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)

        # ৬. JSON ফাইল তৈরি
        json_payload = {
            "developer": "Ahammad Ali",
            "telegram": "https://t.me/banglatvlivefree",
            "last_updated": f"{current_bd_time} (BD Time)",
            "channels_count": channel_count,
            "channels": channels_json_data
        }

        with open(JSON_OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(json_payload, f, indent=4, ensure_ascii=False)

        print(f"Playlist & JSON successfully updated! Total Channels: {channel_count}")

    except Exception as e:
        print(f"Error occurred while updating playlists: {e}")

if __name__ == "__main__":
    parse_and_update_playlists()
