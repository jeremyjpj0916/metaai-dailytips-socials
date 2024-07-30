import meta_ai_api
import hashlib
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description='MetaAI DailyTips posted to socials')
parser.add_argument('--prompt', required=True, help='Prompt to help generate tip category')


# Parse command-line arguments
args = parser.parse_args()

# Use the dynamic arguments in your script
prompt = args.prompt


def generate_tip(prompt):
  # Use the meta-ai-api library to generate a tip
  tip = meta_ai_api.generate_text(prompt, max_length=2048)
  return tip

def get_tip_hash(tip):
  # Calculate the MD5 hash of the tip
  tip_hash = hashlib.md5(tip.encode()).hexdigest()
  return tip_hash
  
def is_tip_unique(tip_hash, hash_file):
  # Check if the tip hash is already in the hash file
  with open(hash_file, 'r') as f:
  existing_hashes = f.readlines()
  return tip_hash not in existing_hashes

def add_tip_hash(tip_hash, hash_file):
  # Add the tip hash to the hash file
  with open(hash_file, 'a') as f:
  f.write(tip_hash + '\n')
  
def main():
  prompt = prompt
  tip = generate_tip(prompt)
  tip_hash = get_tip_hash(tip)
  hash_file = 'tip_hashes.txt'
  if is_tip_unique(tip_hash, hash_file):
    add_tip_hash(tip_hash, hash_file)
    print("Tip of the day: {tip}")
  else:
    print("Tip already exists!")
    
if __name__ == '__main__':
  main()
