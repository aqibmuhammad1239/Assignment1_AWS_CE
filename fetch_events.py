import requests

# Your Ticketmaster API Key
API_KEY = 'bIaG4Q7G37594n81yVZj5lqyJTFXS0T6UR_API_KEY'
URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={API_KEY}'

def fetch_university_events():
    response = requests.get(URL)
    if response.status_status == 200:
        data = response.json()
        events = data.get('_embedded', {}).get('events', [])
        
        for event in events:
            print(f"Event: {event['name']}")
            print(f"Date: {event['dates']['start']['localDate']}")
            print(f"Poster URL: {event['images'][0]['url']}")
            print("-" * 30)
    else:
        print("Failed to fetch data. Check your API Key.")

if __name__ == "__main__":
    fetch_university_events()