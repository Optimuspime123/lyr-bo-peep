import requests
from telegram.ext import Updater, CommandHandler

def lyrics(update, context):
    # Get the type of lyrics (plain or synced) and the name of the song from the user's message
    args = context.args
    lyrics_type = args[0]
    song_name = ' '.join(args[1:])

    # Search for the song on your API
    search_url = f"https://lrclib.net/api/search?q={song_name}"
    search_response = requests.get(search_url)

    # If the song was found, get the lyrics and send them to the user
    if search_response.status_code == 200:
        songs = search_response.json()['data']
        if len(songs) > 0:
            song_id = songs[0]['id']
            lyrics_url = f"https://lrclib.net/api/get/{song_id}"
            lyrics_response = requests.get(lyrics_url)
            if lyrics_response.status_code == 200:
                lyrics = lyrics_response.json()[lyrics_type]
                context.bot.send_message(chat_id=update.effective_chat.id, text=lyrics)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the lyrics for that song.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the lyrics for that song.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the lyrics for that song.")

def main():
    # Create the Updater and pass in the bot token
    updater = Updater("YOUR_BOT_TOKEN_HERE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the command handler for the /lyrics command
    dp.add_handler(CommandHandler("lyrics", lyrics))

    # Add the command handler for the /synced command
    dp.add_handler(CommandHandler("synced", lyrics))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process is stopped
    updater.idle()

if __name__ == '__main__':
    main()
