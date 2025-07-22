import os
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Run OAuth2 flow in browser (use your downloaded OAuth client JSON)
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", SCOPES
)
creds = flow.run_local_server(port=8080)

# Build YouTube API client
youtube = build("youtube", "v3", credentials=creds)

# Get user's playlists
request = youtube.playlists().list(
    part="snippet",
    mine=True,
    maxResults=25
)
response = request.execute()

for item in response["items"]:
    title = item["snippet"]["title"]
    playlist_id = item["id"]
    print(f"{title} — {playlist_id}")