# metaai-dailytips-socials

A program designed to manage social media engagement posts for businesses

```mermaid

graph TD
    A["Cron Schedule"] --> B["GitHub Actions Workflow"]
    B --> C["Python Script"]
    C --> D["Meta AI API"]
    D --> C
    C --> E["Daily Tips"]
    E --> F["Social Media Platforms"]
    F --> G["Users"]
```

Interestingly enough, seems meta ai has blocked github action runner source ips from executing the AI. Alternatively lets clone it down for now and test locally.

I also disabled the twitter and facebook credential related stuff for now for simplicity of demo purposes. Running python script locally still works for me.

```python

pip install -r requirements.txt
```

```python

python3 tips_generator.py --prompt "Generate 10 interesting and insightful health tips of differing sentence lengths with no added information in your next response in a csv parsable format of date_generated,tip,hash,used. date_generated in mm/dd/yyyy format. hash should be the hash value of the tip to be inserted into the csv file using blak2b. used is just a true/false boolean field to designate if its been used before."
```
