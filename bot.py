#!/usr/bin/env python3
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests

# Define your Telegram Bot token
TOKEN = '5862606792:AAGyo32A-oCmYBNoH4GHndcyvHyz-ghzWhQ'

# Define the API endpoint URL
API_URL = 'https://lrclib.net/api/'

# Function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to the music search bot! Send /search followed by the name of the song and/or artist .')

# Function to handle the /search command
def search(update, context):
    if not context.args:
        update.message.reply_text('Please provide a search query. ')
        return

    query = ' '.join(context.args)  # Get the search query from the user
    url = API_URL + 'search?q=' + query

    try:
        # Make a GET request to the API and retrieve the first 5 results
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors
        songs = response.json()[:8]

        if not songs:
            update.message.reply_text('No songs found.')
            return

        # Create a list of InlineKeyboardButtons for each song
        keyboard = []
        for song in songs:
            button = InlineKeyboardButton(
                f'{song["name"]} - {song["artistName"]}',
                callback_data=str(song["id"])
            )
            keyboard.append([button])

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose a song:', reply_markup=reply_markup)

    except requests.exceptions.RequestException:
        update.message.reply_text('An error occurred while connecting to the API.')

# Function to handle the button presses
def button(update, context):
    query = update.callback_query
    song_id = query.data

    # Check if the button pressed is for synced lyrics
    if song_id == 'synced':
        # Get the selected song ID from the context
        song_id = context.user_data.get('song_id')

        if not song_id:
            query.message.reply_text('No song ID found. Please select a song first.')
            return

        try:
            # Get the synced lyrics using the song ID
            url = API_URL + 'get/' + song_id
            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors
            song_details = response.json()

            synced_lyrics = song_details.get('syncedLyrics')
            if not synced_lyrics:
                query.message.reply_text('No synced lyrics found for this song.')
            else:
                query.message.reply_text(synced_lyrics)

        except requests.exceptions.RequestException:
            query.message.reply_text('An error occurred while connecting to the API.')

    elif song_id == 'plain':
        # Get the selected song ID from the context
        song_id = context.user_data.get('song_id')

        if not song_id:
            query.message.reply_text('No song ID found. Please select a song first.')
            return

        try:
            # Get the plain lyrics using the song ID
            url = API_URL + 'get/' + song_id
            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors
            song_details = response.json()

            plain_lyrics = song_details.get('plainLyrics')
            if not plain_lyrics:
                query.message.reply_text('No plain lyrics found for this song.')
            else:
                query.message.reply_text(plain_lyrics)

        except requests.exceptions.RequestException:
            query.message.reply_text('An error occurred while connecting to the API.')

    else:
        # The button press is for selecting a song
        context.user_data['song_id'] = song_id

        try:
            # Get the song details using the song ID
            url = API_URL + 'get/' + song_id
            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors
            song_details = response.json()

            # Extract the required information from the song_details
            name = song_details.get('name')
            artist = song_details.get('artistName')
            spotify_id = song_details.get('spotifyId', '')

            # Create a list of InlineKeyboardButtons for the song actions
            keyboard = [
                [InlineKeyboardButton('Synced Lyrics', callback_data='synced')],
                [InlineKeyboardButton('Plain Lyrics', callback_data='plain')],
                [InlineKeyboardButton('Open on Spotify', url=f'https://open.spotify.com/track/{spotify_id}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the song information and actions to the user
            query.message.reply_text(f'Song: {name}\nArtist: {artist}', reply_markup=reply_markup)

        except requests.exceptions.RequestException:
            query.message.reply_text('An error occurred while connecting to the API.')

# Create an instance of the Updater and pass your bot's token
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register command handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(CallbackQueryHandler(button))

# Start the bot
updater.start_polling()
updater.idle()

