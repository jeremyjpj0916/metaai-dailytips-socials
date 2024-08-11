import csv
import hashlib
import tweepy
from meta_ai_api import MetaAI
from datetime import date, timedelta
import random

# MetaAI API credentials
meta_ai_email = "your_meta_ai_email"
meta_ai_password = "your_meta_ai_password"

# Twitter API credentials
twitter_consumer_key = "your_twitter_consumer_key"
twitter_consumer_secret = "your_twitter_consumer_secret"
twitter_access_token = "your_twitter_access_token"
twitter_access_token_secret = "your_twitter_access_token_secret"

# Set up MetaAI API
ai = MetaAI(fb_email=meta_ai_email, fb_password=meta_ai_password)

# Set up Twitter API
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# Function to generate health tips
def generate_tip(prompt):
    response = ai.prompt(message=prompt)
    data = json.loads(response)
    tip = data['message']
    return tip

# Function to post to Twitter
def post_to_twitter(tip):
    api.update_status(status=tip)

# Function to generate and save tips to CSV file
def generate_and_save_tips(prompt, num_tips):
    tips = []
    for _ in range(num_tips):
        tip = generate_tip(prompt)
        hash = hashlib.blake2b(tip.encode()).hexdigest()
        tips.append((date.today().strftime('%m/%d/%Y'), tip, hash, False))
    with open('tips.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tips)

# Function to check for duplicates and regenerate
def check_duplicates(tips):
    existing_hashes = set()
    with open('tips.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            existing_hashes.add(row[2])
    for i, (date_generated, tip, hash, used) in enumerate(tips):
        if hash in existing_hashes:
            tips[i] = (date_generated, generate_tip(prompt), hashlib.blake2b(generate_tip(prompt).encode()).hexdigest(), used)

# Function to post a tip to Twitter and update CSV file
def post_tip_and_update_csv():
    with open('tips.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    tip_to_post = rows[0]
    post_to_twitter(tip_to_post[1])
    tip_to_post[3] = True
    with open('tips.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

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
    generate_and_save_tips(prompt, 30)
    check_duplicates([])
    post_tip_and_update_csv()
    generate_html_page()

if __name__ == '__main__':
    main()
