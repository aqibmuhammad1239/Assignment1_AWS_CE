import boto3
import requests
import mysql.connector
from datetime import datetime

# --- CONFIGURATION () ---
TICKETMASTER_API_KEY = 'bIaG4Q7G37594n81yVZj5lqyJTFXS0T6UR_API_KEY'
S3_BUCKET_NAME = 'unievent-bucket-name' 
RDS_HOST = 'unievent-db.cz4k0uq606lh.eu-north-1.rds.amazonaws.com' 
RDS_USER = 'admin'
RDS_PASS = 'YourDatabasePassword'
RDS_NAME = 'unievent_db'

# Initialize S3 Client
s3 = boto3.client('s3')

def fetch_and_store_events():
    # 1. Fetch Events from Ticketmaster (Searching for "University" events)
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?keyword=university&apikey={TICKETMASTER_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching from Ticketmaster")
        return

    events_data = response.json().get('_embedded', {}).get('events', [])

    # 2. Connect to RDS Database
    db = mysql.connector.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASS,
        database=RDS_NAME
    )
    cursor = db.cursor()

    for event in events_data:
        name = event['name']
        date_str = event['dates']['start']['localDate'] + " " + event['dates']['start'].get('localTime', '00:00:00')
        venue = event['_embedded']['venues'][0]['name'] if '_embedded' in event else 'Unknown Venue'
        ticket_url = event['url']
        img_url = event['images'][0]['url']
        
        # 3. Download Image and Upload to S3
        img_data = requests.get(img_url).content
        s3_key = f"posters/{event['id']}.jpg"
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=img_data, ContentType='image/jpeg')
        
        # Final S3 Link for the database
        final_s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        # 4. Insert into RDS Table
        sql = "INSERT INTO campus_events (event_name, event_date, venue_name, ticket_url, s3_image_url) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, date_str, venue, ticket_url, final_s3_url))
        
        print(f"Successfully processed: {name}")

    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    fetch_and_store_events()
