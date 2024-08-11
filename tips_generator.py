import csv
import hashlib
import tweepy
from meta_ai_api import MetaAI
from datetime import date, timedelta
import random

# Define command-line arguments
parser = argparse.ArgumentParser(description='MetaAI DailyTips posted to socials')
parser.add_argument('--prompt', required=True, help='Prompt to help generate tip category')
parser.add_argument('--twitter_consumer_key', required=True, help='twitter_consumer_key from X dev portal')
parser.add_argument('--twitter_consumer_secret', required=True, help='twitter_consumer_secret from X dev portal')
parser.add_argument('--twitter_access_token', required=True, help='twitter_access_token from X dev portal')
parser.add_argument('--twitter_access_token_secret', required=True, help='twitter_access_token_secret from X dev portal')
parser.add_argument('--facebook_email', required=True, help='Email for facebook auth')
parser.add_argument('--facebook_password', required=True, help='Password for facebook auth')

# Parse command-line arguments
args = parser.parse_args()

# Use the dynamic arguments in your script
prompt = args.prompt

# Twitter API credentials
twitter_consumer_key = args.twitter_consumer_key
twitter_consumer_secret = args.twitter_consumer_secret
twitter_access_token = args.twitter_access_token
twitter_access_token_secret = args.twitter_access_token_secret

# Facebook credentials
facebook_email = args.facebook_email
facebook_password = args.facebook_password

ai = MetaAI(fb_email=facebook_email, fb_password=facebook_password)

# Set up Twitter API
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# Function to check if a hash already exists in the CSV file
def check_existing_hash(hash):
    try:
        with open('tips.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[2] == hash:
                    return True
    except FileNotFoundError:
        pass
    return False

# Function to generate and save tips to CSV file
def generate_and_save_tips(prompt):
    response = ai.prompt(message=prompt)
    data = json.loads(response)
    csv_data = data['message']
    tips = []
    for line in csv_data.splitlines():
        if len(line.split(',')) == 4:  # Check if line is in CSV format
            date_generated, tip, hash, used = line.split(',')
            if not check_existing_hash(hash):  # Check if hash already exists
                tips.append([date_generated, tip, hash, used])
    with open('tips.csv', 'a', newline='') as csvfile:  # Append to file instead of overwriting
        writer = csv.writer(csvfile)
        writer.writerows(tips)

# Function to post a tip to Twitter and update CSV file
def post_tip_and_update_csv():
    with open('tips.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    unused_tips = [row for row in rows if row[3] == 'False']  # Find unused tips
    if unused_tips:
        tip_to_post = unused_tips[0]
        post_to_twitter(tip_to_post[1])
        tip_to_post[3] = 'True'  # Mark tip as used
        rows[rows.index(tip_to_post)] = tip_to_post  # Update the original list
        with open('tips.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)  # Write updated rows back to file
        return  # Return after posting one tip
    else:
        print("No unused tips available.")

# Function to post to Twitter
def post_to_twitter(tip):
    api.update_status(status=tip)

# Function to generate HTML page
def generate_html_page():
    with open('tips.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    upcoming_tips = [row for row in rows if not row[3]]
    html = "<html><body><h1>Upcoming Health Tips</h1><ul>"
    for tip in upcoming_tips[:7]:
        html += f"<li>{tip[1]}</li>"
    html += "</ul></body></html>"
    with open('upcoming_tips.html', 'w') as htmlfile:
        htmlfile.write(html)

# Main function
def main():
    prompt = "Generate 10 interesting and insightful health tips of differing sentence lengths with no added information in your next response in a csv parsable format of date_generated,tip,hash,used. date_generated in mm/dd/yyyy format. hash should be the hash value of the tip to be inserted into the csv file using blak2b. used is just a true/false boolean field to designate if its been used before"
    generate_and_save_tips(prompt)
    post_tip_and_update_csv()
    generate_html_page()

if __name__ == '__main__':
    main()
