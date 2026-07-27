import os
import requests

def fetch_and_save_playlist():
    api_url = os.environ.get("TAPMAD_API_URL")
    
    if not api_url:
        print("Error: TAPMAD_API_URL secret is not set in GitHub Repository Secrets!")
        exit(1) # সিক্রেট না থাকলে যেন এক্সিকিউশন বন্ধ হয়ে সতর্ক করে

    try:
        print("Fetching data from API...")
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200 and response.text.strip():
            file_name = "Tapmad.m3u"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(response.text)
                
            print(f"Success: Playlist successfully saved as {file_name}")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            exit(1)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save_playlist()
