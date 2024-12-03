import telebot
from telebot import types
import time
import datetime

API_TOKEN = '8084717420:AAEiFPyCnOzJpQqWyUxlv9E9vv0xxytYNZI'  # Your bot API token
bot = telebot.TeleBot(API_TOKEN)

# Set your logger group chat_id here
LOGGER_GROUP_CHAT_ID = '-1002148651992'  # Replace with actual logger group chat ID

# Define the owner's user ID (replace with the actual owner ID)
OWNER_ID = 7877197608  # Replace with the actual owner user ID

# Store user bio warnings and interactions
user_bio_warnings = {}
interaction_logs = {}
group_sync_timers = {}

# Function to log messages to the logger group
def log_to_logger_group(log_message):
    bot.send_message(LOGGER_GROUP_CHAT_ID, log_message)

# Function to handle bot start and log the hosting info
def log_bot_start():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Bot has started at {current_time}. Hosting details: VPS/Server detected."
    log_to_logger_group(log_message)

# Function to handle /start command and log user interactions in DM
@bot.message_handler(commands=['start'])
def handle_start_command(message):
    # Log user start interaction in DM (name, username, user_id)
    log_message = f"User @{message.from_user.username} with ID {message.from_user.id} started the bot."
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
    - [Yᴇ ʙᴏᴛ ᴀᴘᴋᴇ ɢʀᴏᴜᴘ ᴍᴇ Jɪᴛɴᴇ ʙʜᴀɪ ᴜsᴇʀ ᴋɪ ʙɪᴏ ᴍᴇ ʟɪɴᴋ ʜᴀɪ ᴜɴᴋᴏ ᴡᴀʀɴ ᴋʀᴇɢᴀ]
    - [Yᴇ ʙᴏᴛ ʙɪʟᴋᴜʟ sᴀғᴇ ʜᴀɪ ʏᴇ ʙᴏᴛ TEAM SANKI ɴᴇ ʙᴀʏᴀ ʜᴀɪ]

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

# Function to log when a bot is added to a group
@bot.message_handler(content_types=['new_chat_members'])
def log_new_group(message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id == bot.get_me().id:  # If it's the bot being added
                log_message = f"User @{message.from_user.username} added the bot to the group {message.chat.title}."
                log_to_logger_group(log_message)

                # Check bios of all users in the group for links
                check_and_warn_users(message.chat.id)

# Function to check bios of users and warn them
def check_and_warn_users(chat_id):
    try:
        members = bot.get_chat_administrators(chat_id)  # Get admins as an example
        for member in members:
            user_id = member.user.id
            bio = get_bio(user_id)  # Assume a function that fetches user bio
            if 'http' in bio:  # If bio contains a link
                bot.send_message(chat_id, f"@{member.user.username}, please remove the link from your bio within 2 hours. If not, you might be banned.")
                user_bio_warnings[member.user.id] = time.time()  # Track when the warning was sent
                start_timer(member.user.id, chat_id)
    except Exception as e:
        print(f"Error checking users: {e}")

# Function to start a timer for each user's bio warning
def start_timer(user_id, chat_id):
    # Wait for 2 hours (7200 seconds) to recheck the user's bio
    time.sleep(7200)  # 2 hours
    # After 2 hours, recheck the bio
    if user_id in user_bio_warnings and time.time() - user_bio_warnings[user_id] > 7200:
        bio = get_bio(user_id)
        if 'http' in bio:
            bot.kick_chat_member(chat_id, user_id)
            bot.send_message(chat_id, f"@{user_id} was kicked for not removing the link from their bio.")

# Polling loop to keep the bot running
if __name__ == "__main__":
    log_bot_start()  # Log when the bot starts
    bot.polling(non_stop=True)
