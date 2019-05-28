import subprocess
from telegram import Bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
              ConversationHandler)
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#email auth start
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

server.login('appsecure.bot@gmail.com', 'appsecure123')
#email auth end


#email body start
fromaddr = "appsecure.bot@gmail.com"
toaddr = "ameya@appsecure.in"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "recon email"
#email body end


TOKEN = "893808873:AAG9l5dF-9utv9KsDWZFadYqRfk4O0kRGnc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def start(bot, update):
    print (update.message.chat.first_name)
    bot.send_message(chat_id=update.message.chat_id, text="You can type /help to know more about my functions.")

    return ConversationHandler.END

def help(bot, update):
    update.message.reply_text('''Welcome to Wreckon!
				You can control me by sending these commands:\n
				1. /sdd - Sub-Domain Discovery
				2. /sdbf - Sub-Domain Bruteforce
                		3. /dbf - Directory Bruteforce''', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def sdbf_thread(args):
    arg = args[1][0]
    bot.send_message(chat_id=int(args[0]), text="Subdomain Directory Bruteforce: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh sdbf ' + arg], shell=True, stdout=subprocess.PIPE).stdout
    output = pipe.read()
    bot.send_message(chat_id=int(args[0]), text=output)
    msg.attach(MIMEText(output, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

def sdbf(bot, update, args):
    t = threading.Thread(target=sdbf_thread, args=(update.message.chat_id, args)
    t.start()
    return ConversationHandler.END

def sdd(bot, update, args):
    arg = args[0]
    bot.send_message(chat_id=update.message.chat_id, text="Subdomain Directory Discovery: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh sdd ' + arg], shell=True,
        stdout=subprocess.PIPE).stdout
    output = pipe.read()
    bot.send_message(chat_id=update.message.chat_id, text=output)
    msg.attach(MIMEText(output, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    return ConversationHandler.END

def dbf(bot, update, args):
    arg = args[0]
    bot.send_message(chat_id=update.message.chat_id, text="Directory Bruteforce: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh dbf ' + arg], shell=True,
        stdout=subprocess.PIPE).stdout
    output = pipe.read()
    bot.send_message(chat_id=update.message.chat_id, text=output)
    msg.attach(MIMEText(output, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
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
