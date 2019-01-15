# NewThreadAlerterBot
As suggested by the name, NewThreadAlerterBot is a python-based Reddit bot that alerts Redditors of new submissions. Users will be required to send a message to the [bot via Reddit](reddit.com/u/NewThreadAlerterBot) enclosing their desired subreddit. 

### Requirements
- [Python 3.7.2](https://www.python.org/downloads/)

### Python libraries
- praw
- request
- bs4
- mysql.connector

## Usage

To receive alerts from the bot:
1. Message the [bot via Reddit](reddit.com/u/NewThreadAlerterBot).
2. Use 'subscribe' as the subject (not case-sensitive).
3. Type the subreddit name in the body (any subreddits that do not exist will not work).

#### Example

```
Subject: subscribe
Body: redditdev
```

To disable alerts from the bot, change the subject from 'subscribe' to 'unsubscribe'.

Further documentation will be provided for users to run on the bot on their own machines. 

Bot is currently not live, but will be up soon.
