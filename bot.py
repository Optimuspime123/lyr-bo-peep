import requests
from telegram.ext import Updater, CommandHandler

def start(update, context):
    # Send a start message to the user
    user_id = update.effective_user.id
    print(f"User {user_id} farted")
    start_message = "Welcome! This bot can provide lyrics and synced lyrics for songs. Use the /lyrics command to get the plain lyrics or the /synced command to get synced lyrics."
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)

def lyrics(update, context):
    # Get the command from the user's message
    command = update.message.text.split()[0]

    if command == '/lyrics':
        # Handle the /lyrics command
        song_name = ' '.join(update.message.text.split()[1:])
        # Search for the song on your API
        search_url = f"https://lrclib.net/api/search?q={song_name}"
        search_response = requests.get(search_url)

        # If the song was found, get the lyrics and send them to the user
        if search_response.status_code == 200:
            songs = search_response.json()
            if len(songs) > 0:
                song_id = songs[0]['id']
                lyrics_url = f"https://lrclib.net/api/get/{song_id}"
                lyrics_response = requests.get(lyrics_url)
                if lyrics_response.status_code == 200:
                    lyrics = lyrics_response.json()['plainLyrics']

                    if lyrics:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=lyrics)
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, lyrics are not available for this song.It could be instrumental or very new.")
                    
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the lyrics for that song.")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the lyrics for that song.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the lyrics for that song.")
    elif command == '/synced':
        # Handle the /synced command
        song_name = ' '.join(update.message.text.split()[1:])
        # Search for the song on your API
        search_url = f"https://lrclib.net/api/search?q={song_name}"
        search_response = requests.get(search_url)

        # If the song was found, get the synced lyrics and send them to the user
        if search_response.status_code == 200:
            songs = search_response.json()
            if len(songs) > 0:
                song_id = songs[0]['id']
                lyrics_url = f"https://lrclib.net/api/get/{song_id}"
                lyrics_response = requests.get(lyrics_url)
                if lyrics_response.status_code == 200:
                    synced_lyrics = lyrics_response.json()['syncedLyrics']
                    if synced_lyrics:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=synced_lyrics)
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, synced lyrics are not available for this song. Please try /lyrics instead.")
                    
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the synced lyrics for that song.")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the synced lyrics for that song.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the synced lyrics for that song.")
    else:
        # Handle unknown commands
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown command.")


def main():
    # Create the Updater and pass in the bot token
    updater = Updater("5862606792:AAGyo32A-oCmYBNoH4GHndcyvHyz-ghzWhQ")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the command handler for the /lyrics command
    dp.add_handler(CommandHandler("lyrics", lyrics))

    # Add the command handler for the /synced command
    dp.add_handler(CommandHandler("synced", lyrics))

    dp.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process is stopped
    updater.idle()

if __name__ == '__main__':
    main()
