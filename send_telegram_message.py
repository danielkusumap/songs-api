import telepot

token = "1754667648:AAHknck7u_DL5Kjvho0FAo_LF9us33FkiHQ"
reciever_id = 993596412
bot = telepot.Bot(token)

def send_message(text):
    bot.sendMessage(reciever_id, text)
