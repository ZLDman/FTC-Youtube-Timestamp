import json
import requests
from datetime import datetime, timedelta

# Ask for user input for the event code
event_code = input("Enter the Event Code: ")

request = requests.get(
    f'https://ftc-api.firstinspires.org/v2.0/2023/matches/{event_code}',
    auth=('zldman', '000000000000000000000000000000000000'))

# Parse the JSON string
data = json.loads(request.text)

# Function to convert timestamp to YouTube format
def convert_to_youtube_timestamp(start_time, offset_seconds):
    start_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")
    new_time = start_datetime + timedelta(seconds=offset_seconds)
    return new_time.strftime("%H:%M:%S")

# Ask for user input for the starting match number
# NOTE: at a 35 match qualification event enter 36 for semifinal 1 match 1 
start_match_number = int(input("Enter the starting match number: "))

# Ask for user input for the YouTube timestamp for the starting match (HH:MM:SS)
start_match_timestamp = input("Enter the YouTube timestamp for the starting match (HH:MM:SS): ")

# Convert user input to datetime
start_match_time = datetime.strptime(start_match_timestamp, "%H:%M:%S")

# Calculate offset for the starting match
offset_seconds = (start_match_time - datetime.strptime(data["matches"][start_match_number - 1]["actualStartTime"], "%Y-%m-%dT%H:%M:%S.%f")).total_seconds()

# Create a list to store individual match details
details_list = []

# Convert and append details for all matches from the specified starting match number
for i in range(start_match_number - 1, len(data["matches"])):
    match = data["matches"][i]
    youtube_timestamp = convert_to_youtube_timestamp(match["actualStartTime"], offset_seconds)

    # Extract and sort team numbers
    red_teams = sorted([team['teamNumber'] for team in match["teams"] if team["station"].startswith("Red")])
    blue_teams = sorted([team['teamNumber'] for team in match["teams"] if team["station"].startswith("Blue")])

    match_detail = f"{youtube_timestamp} {match['description']} ({match['scoreRedFinal']}) {', '.join(map(str, red_teams))} vs ({match['scoreBlueFinal']}) {', '.join(map(str, blue_teams))}"
    details_list.append(match_detail)

# Join individual match details into a single string
details_string = "\n".join(details_list)

# Print the stored details
print(details_string)

# Wait for user input before closing
input("Press Enter to close the window...")