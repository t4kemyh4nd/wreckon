import os
from telegram import Bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
												  ConversationHandler)

TOKEN = "893808873:AAG9l5dF-9utv9KsDWZFadYqRfk4O0kRGnc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def start(bot, update):
		print (update.message.chat.first_name)
		bot.send_message(chat_id=update.message.chat_id, text="You can type /help to know more about my Functions.")

		return ConversationHandler.END

def help(bot, update):
		update.message.reply_text('''Welcome to Wreckon!
				You can control me by sending these commands:\n
				1. /sdd - Sub-Domain Discovery
				2. /sdbf - Sub-Domain Bruteforce''', reply_markup=ReplyKeyboardRemove())

		return ConversationHandler.END

def sdbf(bot, update, args):
		arg = args[0]
		bot.send_message(chat_id=update.message.chat_id, text="Subdomain Directory Bruteforce: " + arg)
		os.system("./wreckon.sh sdbf " + arg)
		return ConversationHandler.END

def sdd(bot, update, args):
		arg = args[0]
		bot.send_message(chat_id=update.message.chat_id, text="Subdomain Directory Discovery: " + arg)
		os.system("./wreckon.sh sdd " + arg)
		return ConversationHandler.END

def dbf(bot, update, args):
		arg = args[0]
		bot.send_message(chat_id=update.message.chat_id, text="Directory Bruteforce: " + arg)
		os.system("./wreckon.sh dbf " + arg)
		return ConversationHandler.END

def main():
		updater = Updater(TOKEN)
		dp = updater.dispatcher

		start_handler = CommandHandler('start', start)
		help_handler = CommandHandler('help', help)
		sdbf_handler = CommandHandler('sdbf', sdbf, pass_args=True)
		sdd_handler = CommandHandler('sdd', sdd, pass_args=True)
		dbf_handler = CommandHandler('dbf', dbf, pass_args=True)

		dp.add_handler(start_handler)
		dp.add_handler(help_handler)
		dp.add_handler(sdbf_handler)
		dp.add_handler(sdd_handler)
		dp.add_handler(dbf_handler)

		updater.start_polling()
		updater.idle()


if __name__ == '__main__':
		main()