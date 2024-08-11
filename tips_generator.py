from meta_ai_api import MetaAI
import hashlib
import argparse
import json
import tweepy

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

ai = MetaAI(fb_email=args, fb_password="your_fb_password")

# Twitter API credentials
twitter_consumer_key = args.twitter_consumer_key
twitter_consumer_secret = args.twitter_consumer_secret
twitter_access_token = args.twitter_access_token
twitter_access_token_secret = args.twitter_access_token_secret

# Facebook credentials
facebook_email = args.facebook_email
facebook_password = args.facebook_password

ai = MetaAI(fb_email=facebook_email, fb_password=facebook_password)

def generate_tip(prompt):
  # Use the meta-ai-api library to generate a tip
  response = ai.prompt(message=prompt)
  # Parse the JSON data
  data = json.loads(response)
  # Extract the 'message' field
  tip = data['message']
  return tip


def post_to_twitter(tip):
  # Authenticate with Twitter
  auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
  auth.set_access_token(twitter_access_token, twitter_access_token_secret)
  api = tweepy.API(auth)
  # Post the tip to Twitter
  api.update_status(status=tip)

def main():



if __name__ == '__main__':
  main()
