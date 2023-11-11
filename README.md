## NotificationDiscordBot
A Discord Bot which can be configured to send reminders in an interval.

## Functionality
#### ?configure ['message'] [interval]    
set up a simple reminder message in that chat

Example: ?configure 'Remember to use /bump to keep your active developer badge' seconds=10,minutes=5,days=58
#### /bump
keep developer badge active for 60 days
## Setup locally
1. clone the repository
2. open cloned repository in terminal
```bash
pip install discord
python main.py
```
3. paste you bot secret in the terminal
## Setup with Heroku
1. fork the repository
2. create a heroku app and connect it to the fork
3. enable one basic worker dyno
4. add a config var "NOTI_BOT_SECRET" with your bot secret
5. deploy your application
