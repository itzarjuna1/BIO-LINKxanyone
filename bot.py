import telebot
from telebot import types
import time
import datetime

API_TOKEN = '8084717420:AAEiFPyCnOzJpQqWyUxlv9E9vv0xxytYNZI'
bot = telebot.TeleBot(API_TOKEN)

# Set your logger group chat_id here
LOGGER_GROUP_CHAT_ID = '7877197608'

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
    log_message = f"User @{message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name}) with ID {message.from_user.id} started the bot in DM."
    log_to_logger_group(log_message)

    # Attractive welcome message with buttons
    photo_url = 'https://graph.org/file/6c0db28a848ed4dacae56-93b1bc1873b2494eb2.jpg'  # Replace with actual image URL
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Owner", url="https://t.me/TSGCODER"))
    markup.add(types.InlineKeyboardButton("Support", url="https://t.me/matalbi_duniya"))
    markup.add(types.InlineKeyboardButton("Start Exploring", callback_data="explore"))

    welcome_message = """
    **Welcome to [Your Bot Name] 🤖!**

    Hi, I'm your personal assistant here to help you with [brief description of bot's purpose]. Whether you're looking for [features of the bot], I’ve got you covered!

    🌟 Here's what I can do for you:
    - [Bᴏᴛ ᴋᴏ ᴀᴘɴᴇ ɢʀᴏᴜᴘ ᴍᴇ ᴀᴅᴅ ᴋʀᴏ ᴏʀ ᴀᴘɴᴇ ɢʀᴏᴜᴘ ᴋᴏ sᴇᴄᴜʀᴇᴅ ᴋʀ ʟᴏ]
    - [Yᴇ ʙᴏᴛ ᴀᴘᴋᴇ ɢʀᴏᴜᴘ ᴍᴇ Jɪᴛɴᴇ ʙʜɪ ᴜsᴇʀ ᴋɪ ʙɪᴏ ᴍᴇ ʟɪɴᴋ ʜᴀɪ ᴜɴᴋᴏ ᴡᴀʀɴ ᴋʀᴇɢᴀ]
    - [Yᴇ ʙᴏᴛ ʙɪʟᴋᴜʟ sᴀғᴇ ʜᴀɪ ʏᴇ ʙᴏᴛ TEAM SANKI ɴᴇ ʙɴᴀʏᴀ ʜᴀɪ]

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

    # Check if bot has ban permissions in the group
    if not has_ban_permission(message.chat.id):
        bot.send_message(message.chat.id, f"@{message.from_user.username}, I do not have ban permissions. Please ask the group owner to grant me these permissions so I can warn users who add links in their bio.")

# Function to check if bot has ban permissions
def has_ban_permission(chat_id):
    try:
        chat_member = bot.get_chat_member(chat_id, bot.get_me().id)
        return chat_member.status in ['administrator', 'creator'] and chat_member.can_restrict_members
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return False

# Function to log when a bot is added to a group
@bot.message_handler(content_types=['new_chat_members'])
def log_new_group(message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id == bot.get_me().id:  # If it's the bot being added
                log_message = f"User @{message.from_user.username} ({message.from_user.first_name}) added the bot to the group {message.chat.title}."
                log_to_logger_group(log_message)

                # Notify the group owner about the permissions
                bot.send_message(message.chat.id, f"@{message.from_user.username}, please ensure I have ban permissions to warn users who add links to their bio.")

# Function to check if a user in a group has a link in their bio
@bot.message_handler(content_types=['new_chat_members'])
def check_new_member(message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            bio = get_bio(new_member.id)  # Assume a function that gets user bio
            if 'http' in bio:
                bot.send_message(message.chat.id, f"@{new_member.username}, please remove the link from your bio within 2 hours.")
                user_bio_warnings[new_member.id] = time.time()  # Start the 2-hour timer
                start_timer(new_member.id, message.chat.id)

# Timer to kick users who don't remove links within 2 hours
def start_timer(user_id, chat_id):
    time.sleep(7200)  # Wait for 2 hours
    if user_id in user_bio_warnings and time.time() - user_bio_warnings[user_id] > 7200:
        bot.kick_chat_member(chat_id, user_id)
        bot.send_message(chat_id, f"@{user_id} was kicked for not removing the link from their bio.")

# Function to get user's bio (this can be improved as per your setup)
def get_bio(user_id):
    # This should ideally fetch the bio via Telegram API, but due to limitations, 
    # this part will be simplified
    return 'http://example.com'

# Print a message to VPS terminal when bot starts
print("Bot has started!")

# Polling loop to keep the bot running
bot.polling(non_stop=True)
