import subprocess
from telegram import Bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
              ConversationHandler)
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import threading

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
    intro_text = """
 __      __                         __                   
/  \    /  \_______   ____   ____  |  | __ ____    ____  
\   \/\/   /\_  __ \_/ __ \_/ ___\ |  |/ //  _ \  /    \ 
 \        /  |  | \/\  ___/\  \___ |    <(  <_> )|   |  \
  \__/\  /   |__|    \___  >\___  >|__|_ \\____/ |___|  /
       \/                \/     \/      \/            \/ 
 Reconnaissance bot by @YashitM and @takemyhand
 
 Commands:
    1) /sdd - Sub Domain Discovery
    2) /sdbf - Sub Domain Bruteforce
    3) /dbf - Directory Bruteforce
    4) /nikto - HTTP Nikto Scan
    5) /niktossl - HTTPS Nikto Scan
    
    """
    bot.send_message(chat_id=update.message.chat_id, text=intro_text)

    return ConversationHandler.END

def help(bot, update):
    update.message.reply_text('''
    Welcome to Wreckon!\n
    You can control me by sending these commands:\n
    1. /sdd - Sub-Domain Discovery
    2. /sdbf - Sub-Domain Bruteforce
    3. /dbf - Directory Bruteforce
    4. /nikto - HTTP nikto scan
    5. /niktossl - HTTPS nikto scan
                ''', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def send_msg(id, message, bot):
    chunks, chunk_size = len(4096), len(4096)/4
    split_messages = [ x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    
    for msg in split_messages:
        bot.send_message(chat_id=id, text=msg)
        
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
  
def sdbf(bot, update, args):
    t = threading.Thread(target=sdbf_thread, args=(update.message.chat_id, args, bot))
    t.start()
    return ConversationHandler.END

def sdbf_thread(id, args, bot):
    arg = args[0]
    bot.send_message(chat_id=id, text="Subdomain Bruteforce: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh sdbf ' + arg], shell=True, stdout=subprocess.PIPE).stdout
    output = pipe.read()
    send_msg(id, output, bot)

def sdd(bot, update, args):
    t = threading.Thread(target=sdd_thread, args=(update.message.chat_id, args, bot))
    t.start()
    return ConversationHandler.END

def sdd_thread(id, args, bot):
    arg = args[0]
    bot.send_message(chat_id=id, text="Subdomain Directory Discovery: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh sdd ' + arg], shell=True,
        stdout=subprocess.PIPE).stdout
    output = pipe.read()
    send_msg(id, output, bot)
    return ConversationHandler.END

def dbf(bot, update, args):
    t = threading.Thread(target=dbf_thread, args=(update.message.chat_id, args, bot))
    t.start()
    return ConversationHandler.END

def dbf_thread(id, args, bot):
    arg = args[0]
    bot.send_message(chat_id=id, text="Directory Bruteforce: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh dbf ' + arg], shell=True,
        stdout=subprocess.PIPE).stdout
    output = pipe.read()
    send_msg(id, output, bot)
    return ConversationHandler.END

def nikto(bot, update, args):
    t = threading.Thread(target=nikto_thread, args=(update.message.chat_id, args, bot))
    t.start()
    return ConversationHandler.END

def nikto_thread(id, args, bot):
    arg = args[0]
    bot.send_message(chat_id=id, text="Nikto scan: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh nikto ' + arg], shell=True,
        stdout=subprocess.PIPE).stdout
    output = pipe.read()
    send_msg(id, output, bot)
    return ConversationHandler.END

def niktossl(bot, update, args):
    t = threading.Thread(target=niktossl_thread, args=(update.message.chat_id, args, bot))
    t.start()
    return ConversationHandler.END

def niktossl_thread(id, args, bot):
    arg = args[0]
    bot.send_message(chat_id=id, text="Nikto (ssl) scan: " + arg)
    pipe = subprocess.Popen(
        ['./wreckon.sh niktossl ' + arg], shell=True,
        stdout=subprocess.PIPE).stdout
    output = pipe.read()
    send_msg(id, output, bot)
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    sdbf_handler = CommandHandler('sdbf', sdbf, pass_args=True)
    sdd_handler = CommandHandler('sdd', sdd, pass_args=True)
    dbf_handler = CommandHandler('dbf', dbf, pass_args=True)
    nikto_handler = CommandHandler('nikto', nikto, pass_args=True)
    niktossl_handler = CommandHandler('niktossl', niktossl, pass_args=True)

    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(sdbf_handler)
    dp.add_handler(sdd_handler)
    dp.add_handler(dbf_handler)
    dp.add_handler(nikto_handler)
    dp.add_handler(niktossl_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
