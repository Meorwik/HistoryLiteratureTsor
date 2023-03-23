import json

with open('data/config/config.ini', 'r') as file:
    tg_data = json.load(file)
    admins = [adm for adm in tg_data["admins"].split()]

# Bot token
BOT_TOKEN = tg_data["token"] 
# admins
ADMINS = admins 
