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

python3 tips_generator.py --prompt "Generate 10 interesting and insightful health tips of differing sentence lengths with no added information in your next response in a csv parsable format of date_generated,tip. date_generated in mm/dd/yyyy format."
```

Example Outputs:

The CSV file essentially serving as our tips datastore to be utlized and added to by the program:

View in mac terminal:
```
column -t -s , tips.csv
```

Output:
```
date_generated  tip                                                                                                hash                              used
08/17/2024      Stay hydrated by drinking at least 8 cups of water a day.                                          9d9c2efa2939aaec5c7225a4b9d52b81  True
08/17/2024      Exercise for 30 minutes daily to boost mood and energy.                                            19e5bc18846c444b748618431750aa3a  True
08/17/2024      Aim for 7-9 hours of sleep each night to support immune function.                                  62ea9022954edcea63dcaea66d1f6b90  True
08/17/2024      Incorporate stress-reducing activities like meditation or yoga into your routine.                  458dd81b3d927e45623caa5626a671e7  False
08/17/2024      Get regular check-ups and health screenings to stay on top of your health.                         31873032d6c8ea029ee66cfafc297f7b  False
08/17/2024      Take breaks and move throughout the day to reduce the risk of chronic disease.                     a896c03bef7453f9f856d6b62a5e26af  False
08/17/2024      Limit screen time before bed to improve sleep quality and duration.                                6d8207300e66f0095c0f3c9b730a3283  False
08/17/2024      Stay hydrated by drinking at least 8 cups of water per day.                                        c28c5d51236d47489fd48e98f91b30a4  False
08/17/2024      Exercise for 30 minutes daily to reduce stress and anxiety.                                        40c2c3ea76c7fb4790615e6bc7b41fb2  False
08/17/2024      Practice mindfulness and meditation for mental clarity.                                            6c4ae5d02d09f90971f0431eba281caf  False
08/17/2024      Limit screen time before bed to improve sleep quality.                                             ddd75f88a501a02db54fd0821d68a08a  False
08/17/2024      Incorporate strength training into your workout routine.                                           6103b69ec9ff6f669cfad9efdadfaf4a  False
08/17/2024      Listen to your body and take rest days when needed.                                                09c843966793eb8087d9c94392812dd9  False
08/17/2024      Stay connected with friends and family for emotional support.                                      a7297d1cea9254c39c97acad83a2117f  False
08/17/2024      Consult a healthcare professional before starting new supplements.                                 e1fa3faf2b16e1ea28b13d6744c8069e  False
08/17/2024      Drink plenty of water throughout the day to stay hydrated and maintain focus.                      d68cea14c0360f125c318caabcfd6d01  False
08/17/2024      Regular exercise can reduce symptoms of anxiety and depression by releasing endorphins.            7b2642a5d329301954a65cdb78beb599  False
08/17/2024      Aim for 7-8 hours of sleep each night to allow your body to repair and recharge.                   a127c8051ec29439ff0d0fe445ee0e0b  False
08/17/2024      Incorporate stress-reducing activities like meditation or deep breathing into your daily routine.  ea0af76f66431d83a34769a1b749cda1  False
08/17/2024      Stay connected with friends and family to support mental health and well-being.                    9f696c85c065ffdf926ddff32d437cba  False
08/17/2024      Take breaks and prioritize self-care to avoid burnout and maintain productivity.                   4a4b59fe661655b01fdbd1d1adfd517f  False
```


Human readable HTML page detailing next social media tips that will be posted for human review days prior:

![image](https://github.com/user-attachments/assets/dceaeb39-2a26-428c-91ac-106c15fa90d5)

Special thanks to underlying library used:
https://github.com/Strvm/meta-ai-api

