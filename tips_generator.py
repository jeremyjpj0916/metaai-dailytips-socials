from meta_ai_api import MetaAI
import hashlib
import argparse
import json
import os
import tweepy
from facebook_sdk import FacebookSDK

# Define command-line arguments
parser = argparse.ArgumentParser(description='MetaAI DailyTips posted to socials')
parser.add_argument('--prompt', required=True, help='Prompt to help generate tip category')

# Parse command-line arguments
args = parser.parse_args()

# Use the dynamic arguments in your script
prompt = args.prompt

ai = MetaAI()

# Twitter API credentials
twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Facebook API credentials
facebook_app_id = os.environ['FACEBOOK_APP_ID']
facebook_app_secret = os.environ['FACEBOOK_APP_SECRET']
facebook_page_id = os.environ['FACEBOOK_PAGE_ID']
facebook_page_access_token = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']

def generate_tip(prompt):
  # Use the meta-ai-api library to generate a tip
  response = ai.prompt(message=prompt)
  # Parse the JSON data
  data = json.loads(response)
  # Extract the 'message' field
  tip = data['message']
  return tip

def get_tip_hash(tip):
  # Calculate the MD5 hash of the tip
  tip_hash = hashlib.md5(tip.encode()).hexdigest()
  return tip_hash

def is_tip_unique(tip_hash, hash_file):
  # Check if the tip hash is already in the hash file
  with open(hash_file, 'r') as f:
    existing_hashes = f.readlines()
  return tip_hash not in [h.strip() for h in existing_hashes]

def add_tip_hash(tip_hash, hash_file):
  # Add the tip hash to the hash file
  with open(hash_file, 'a') as f:
    f.write(tip_hash + '\n')

def post_to_twitter(tip):
  # Authenticate with Twitter
  auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
  auth.set_access_token(twitter_access_token, twitter_access_token_secret)
  api = tweepy.API(auth)
  # Post the tip to Twitter
  api.update_status(status=tip)

def post_to_facebook(tip):
  # Authenticate with Facebook
  facebook = FacebookSDK(facebook_app_id, facebook_app_secret)
  facebook.set_page_access_token(facebook_page_id, facebook_page_access_token)
  # Post the tip to Facebook
  facebook.post_page_feed(facebook_page_id, message=tip)

def main():
  hash_file = 'tip_hashes.txt'
  max_attempts = 10
  attempts = 0

  while attempts < max_attempts:
    tip = generate_tip(prompt)
    tip_hash = get_tip_hash(tip)
    if is_tip_unique(tip_hash, hash_file):
      add_tip_hash(tip_hash, hash_file)
      print(f"Tip of the day: {tip}")
      post_to_twitter(tip)
      post_to_facebook(tip)
      break
    else:
      print(f"Tip already exists! Attempt {attempts + 1}/{max_attempts}")
      attempts += 1
  else:
    print("Failed to generate a unique tip after 10 attempts.")

if __name__ == '__main__':
  main()
