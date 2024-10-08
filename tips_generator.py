import csv
import argparse
import tweepy
import hashlib
from meta_ai_api import MetaAI
from datetime import date, timedelta
import random
import json

# Define command-line arguments
parser = argparse.ArgumentParser(description='MetaAI DailyTips posted to socials')
parser.add_argument('--prompt', required=True, help='Prompt to help generate tip category')
#parser.add_argument('--twitter_consumer_key', required=True, help='twitter_consumer_key from X dev portal')
#parser.add_argument('--twitter_consumer_secret', required=True, help='twitter_consumer_secret from X dev portal')
#parser.add_argument('--twitter_access_token', required=True, help='twitter_access_token from X dev portal')
#parser.add_argument('--twitter_access_token_secret', required=True, help='twitter_access_token_secret from X dev portal')
#parser.add_argument('--facebook_email', required=True, help='Email for facebook auth')
#parser.add_argument('--facebook_password', required=True, help='Password for facebook auth')

# Parse command-line arguments
args = parser.parse_args()

# Use the dynamic arguments in your script
prompt = args.prompt

# Twitter API credentials
#twitter_consumer_key = args.twitter_consumer_key
#twitter_consumer_secret = args.twitter_consumer_secret
#twitter_access_token = args.twitter_access_token
#twitter_access_token_secret = args.twitter_access_token_secret

# Facebook credentials
#facebook_email = args.facebook_email
#facebook_password = args.facebook_password

#Username/Pass functionality seems busted.
#ai = MetaAI(fb_email=facebook_email, fb_password=facebook_password)
ai = MetaAI()

# Set up Twitter API
#auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
#auth.set_access_token(twitter_access_token, twitter_access_token_secret)
#api = tweepy.API(auth)

def generate_hash_blake2b(tip):
    try:
        # Use Blake2b hashing instead of MD5
        hash_object = hashlib.blake2b(tip.encode('utf-8'))
        return hash_object.hexdigest()
    except Exception as e:
        print(f"An unexpected error occurred in generate_hash_blake2b: {e}")
        return None

def generate_hash_md5(tip):
    try:
        # Use Blake2b hashing instead of MD5
        hash_object = hashlib.md5(tip.encode('utf-8'))
        return hash_object.hexdigest()
    except Exception as e:
        print(f"An unexpected error occurred in generate_hash_md5: {e}")
        return None

# Function to generate and save tips to CSV file
def generate_and_save_tips(prompt):
    try:
        response = ai.prompt(message=prompt)
        csv_data = response['message']
        tips = []
        existing_hashes = set()
        try:
            with open('tips.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    existing_hashes.add(row[2])  # Add hashes from tips.csv to set
        except FileNotFoundError:
            print("Tips CSV file not found. Creating a new one.")
        except Exception as e:
            print(f"An unexpected error occurred while reading tips.csv: {e}")
        for line in csv_data.splitlines():
            if len(line.split(',')) == 2:  # Check if line is in CSV format
                date_generated, tip = line.split(',')
                cleaned_date = date_generated.strip().strip('"')
                cleaned_tip = tip.strip().strip('"')
                hash_of_tip = generate_hash_md5(cleaned_tip)
                if hash_of_tip not in existing_hashes:  # Check if hash is not in tips.csv
                    tips.append([cleaned_date, cleaned_tip, hash_of_tip, "False"])
        try:
            with open('tips.csv', 'a', newline='') as csvfile:  # Append to file instead of overwriting
                writer = csv.writer(csvfile)
                for tip in tips:
                    writer.writerow([field.strip('"') for field in tip])
        except Exception as e:
            print(f"An unexpected error occurred while writing to tips.csv: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_and_save_tips: {e}")


# Function to post a tip to Twitter and update CSV file
def post_tip_and_update_csv():
    try:
        with open('tips.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        for row in rows:
            if row[3] == 'False':  # Find first unused tip
                tip_to_post = row
                # post_to_twitter(tip_to_post[1])
                tip_to_post[3] = 'True'  # Mark tip as used
                try:
                    with open('tips.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        for r in rows:
                            if r == tip_to_post:
                                writer.writerow(tip_to_post)  # Write updated row
                            else:
                                writer.writerow(r)  # Write unchanged rows
                except Exception as e:
                    print(f"An unexpected error occurred while updating tips.csv: {e}")
                return  # Return after posting one tip
        print("No unused tips available.")
    except FileNotFoundError:
        print("Tips CSV file not found.")
    except Exception as e:
        print(f"An unexpected error occurred in post_tip_and_update_csv: {e}")


# Function to post to Twitter
#def post_to_twitter(tip):
#    try:
#        api.update_status(status=tip)
#    except tweepy.TweepError as e:
#        print(f"Error posting to Twitter: {e}")
#    except Exception as e:
#        print(f"An unexpected error occurred: {e}")

# Function to generate HTML page
def generate_html_page():
    try:
        with open('tips.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        print("Tips CSV file not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading tips.csv: {e}")
        return

    try:
        upcoming_tips = [row for row in rows if row[3] == "False"]
        html = """
        <html>
        <head>
            <title>Upcoming Health Tips</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                h1 {
                    color: #007bff;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <h1>Upcoming Health Tips</h1>
            <ul>
        """
        for tip in upcoming_tips[:7]:
            html += f"<li>{tip[1]}</li>"
        html += """
            </ul>
        </body>
        </html>
        """
        with open('upcoming_tips.html', 'w') as htmlfile:
            htmlfile.write(html)
    except Exception as e:
        print(f"An unexpected error occurred while generating HTML page: {e}")

# Main function
def main():
    generate_and_save_tips(prompt)
    post_tip_and_update_csv()
    generate_html_page()

if __name__ == '__main__':
    main()
