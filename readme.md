# Telegram Notify Bot

##### @everyone for Telegram!

### Client commands:
- /call -> @everyone notify
- /call_perm -> change permission to "/call" command for all users (default - only for group admins) (probably can notify only less than 200 users)

### Admin commands:
- /add_admin @user -> add someone to the bot's admins
- /add_bl @user -> add someone to the bot's blacklist
- /del_admin @user -> delete someone from the bot's admins
- /del_bl @user -> delete someone from the bot's blacklist

## Launch

1. Install python version **3.7**+ (tested on version **3.10.5**)
2. Downloads libraries from requirements.txt: \
   `python -m pip install -r ./requirements` \
   `pip install -r requirements.txt`
3. Change the values in `config.py` and edit "ADMINS" in `src/database.py`
4. Launch the bot: `python ./main.py`
