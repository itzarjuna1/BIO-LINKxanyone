import telebot
from telebot import types
import time
import datetime

API_TOKEN = '8084717420:AAEiFPyCnOzJpQqWyUxlv9E9vv0xxytYNZI'
bot = telebot.TeleBot(API_TOKEN)

# Set your logger group chat_id here
LOGGER_GROUP_CHAT_ID = '-1002148651992'

# Set the bot owner's user ID (replace with your actual user ID)
OWNER_USER_ID = '7877197608'

# Store user bio warnings and interactions
user_bio_warnings = {}
interaction_logs = []

# Function to log messages to the logger group
def log_to_logger_group(log_message):
    bot.send_message(LOGGER_GROUP_CHAT_ID, log_message)

# Function to handle /start command and log user interactions in DM
@bot.message_handler(commands=['start'])
def handle_start_command(message):
    # Log user start interaction in DM (name, username, user_id)
    log_message = f"User @{message.from_user.username} ({message.from_user.first_name}) with ID {message.from_user.id} started the bot in DM."
    log_to_logger_group(log_message)

    # Attractive welcome message with buttons
    photo_url = 'https://graph.org/file/6c0db28a848ed4dacae56-93b1bc1873b2494eb2.jpg'  # Replace with actual image URL
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Owner", url="https://t.me/TSGCODER"))
    markup.add(types.InlineKeyboardButton("Support", url="https://t.me/matalbi_duniya"))
    markup.add(types.InlineKeyboardButton("Start Exploring", callback_data="explore"))

    welcome_message = """
    **Welcome to Lɪɴᴋ Usᴇʀ Wᴀʀɴ 🤖!**

    Hi, I'm your personal assistant here to help you with [brief description of bot's purpose]. Whether you're looking for [features of the bot], I’ve got you covered!

    🌟 Here's what I can do for you:
    - [Add me to your group for bio link warning detection]
    - [This bot is completely safe, created by TEAM SANKI]

    Tap on the buttons below to get started:

    🚀 **Let's make your experience awesome!**
    """

    bot.send_photo(
        message.chat.id, 
        photo_url, 
        caption=welcome_message, 
        parse_mode='Markdown', 
        reply_markup=markup
    )

# Function to check if a user in a group has a link in their bio
def check_and_warn_users(chat_id):
    try:
        members = bot.get_chat_members(chat_id)  # Retrieve all members of the group
        for member in members:
            # Retrieve user bio one by one using get_chat_member
            member_info = bot.get_chat_member(chat_id, member.user.id)
            bio = member_info.user.bio if member_info.user.bio else "No bio"
            
            # Check for any links in the bio (http:// or https://)
            if 'http://' in bio or 'https://' in bio:
                # Send warning message mentioning the user
                bot.send_message(chat_id, f"@{member.user.username}, please remove the link from your bio within 1 hour. If not, you might be muted.")
                user_bio_warnings[member.user.id] = time.time()  # Track when the warning was sent
                start_timer(member.user.id, chat_id)
    except Exception as e:
        print(f"Error checking users: {e}")

# Timer to mute users who don't remove links within 1 hour
def start_timer(user_id, chat_id):
    time.sleep(3600)  # Wait for 1 hour
    if user_id in user_bio_warnings and time.time() - user_bio_warnings[user_id] > 3600:
        if user_id != OWNER_USER_ID:  # Prevent muting the bot owner
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)  # Mute user
            bot.send_message(chat_id, f"@{user_id} has been muted for not removing the link from their bio.")
        else:
            bot.send_message(chat_id, f"Owner @ {OWNER_USER_ID} is not muted. Mute action skipped.")

# Function to check if the bot has ban permissions in the group
def has_ban_permission(chat_id):
    try:
        chat_member = bot.get_chat_member(chat_id, bot.get_me().id)
        return chat_member.status in ['administrator', 'creator'] and chat_member.can_restrict_members
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return False

# Function to handle when the bot is added to a group
@bot.message_handler(content_types=['new_chat_members'])
def log_new_group(message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id == bot.get_me().id:  # If it's the bot being added
                log_message = f"User @{message.from_user.username} ({message.from_user.first_name}) added the bot to the group {message.chat.title}."
                log_to_logger_group(log_message)

                # Check for bio links in the group members
                check_and_warn_users(message.chat.id)

# Function to handle banning users in the group
@bot.message_handler(commands=['ban'])
def ban_user(message):
    # Only allow the bot owner to ban
    if message.from_user.id == bot.get_me().id:
        bot.send_message(message.chat.id, "You can't ban the bot itself!")
        return
    
    banned_user = message.reply_to_message.from_user
    if banned_user.id == bot.get_me().id:
        bot.send_message(message.chat.id, "Hᴇᴇ ʙʜᴀɪ ᴋʏᴀ ᴅɪᴋᴋᴀᴛ ʜᴀɪ ᴛᴜᴍʜᴇ ᴛᴜᴍ ᴍᴇʀᴇ ᴏᴡɴᴇʀ ᴋᴋᴏ ʙᴀɴ ᴋʀɴᴇ ᴘʀ Kᴀʜᴇ ᴛᴜʟᴇ ʜᴏ😏")
        return
    
    bot.kick_chat_member(message.chat.id, banned_user.id)
    bot.send_message(message.chat.id, f"User @{banned_user.username} has been banned.")

# Polling loop to keep the bot running
bot.polling(non_stop=True)
