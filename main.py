from database import DataBase
from info import *
from telegram.ext import *
from telegram import *
import telegram
import config

CHANNELS = ["@onsbase", "@menfesonsbase", "@ratemyonspartner"]

class ChatBot:
    def __init__(self, api_id, api_hash,bot_name, bot_key):
        self.boys = []
        self.girls = []
        self.chat_pair = {}

        self.api_id, self.api_hash, self.bot_name, self.bot_key = api_id, api_hash,bot_name, bot_key

        # Calling  database
        self.record = DataBase()

        # Bot command handler
        self.command_handler()

    def start(self, update, context):
        user_id, name, username = self.common_args(update, context)

        # chat type (group or private)
        chat_type = update.message.chat.type

        if chat_type == "private":
            try:
                check_user = self.record.search(user_id)
                if not check_user:
                    # record insertion
                    self.record.insert(user_id, name, username)

                # Typing Action
                context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING, timeout=1)
                # User welcome
                update.message.reply_text(text="send numeric for set age and send text for set domisili")
            except telegram.error.Unauthorized:
                pass

    def common_args(self, update, context):
        if update.message.chat.type != "private":
            user_id = update.message.chat.id
            name = context.bot.get_chat(chat_id=user_id).title
            username = context.bot.get_chat(chat_id=user_id).username

        else:
            user_id = update.message.from_user.id
            name = update.message.from_user.first_name
            username = update.message.from_user.username

        return user_id, name, username

    def message_handler(self, update, context):
        user_id, name, username = self.common_args(update, context)

        # chat type (group or private)
        chat_type = update.message.chat.type

        if chat_type == "private":
            try:
                msg = update.message.text
                if not msg.isdigit():
                    new_data = {"domisili": f"{msg}"}
                    self.record.update(user_id, new_data)
                    data = self.record.search(user_id)
                    domisilii = data.get("domisili")

                    context.bot.send_message(chat_id=user_id, text=f"congrast your dom set {domisilii}")
                else:
                    kon = int(msg)
                    new_data = {"old": f"{kon}"}
                    self.record.update(user_id, new_data)
                    data = self.record.search(user_id)
                    age_user = data.get("old")

                    context.bot.send_message(chat_id=user_id, text=f"congrast your old set {age_user}")

            # if user stop the bot
            except telegram.error.Unauthorized:
                self.end_conversation(update, context)

    def end_conversation(self, update, context):
        user_id, name, username = self.common_args(update, context)

        # chat type (group or private)
        chat_type = update.message.chat.type

        if chat_type == "private":
            try:
                # getting user info
                data = self.record.search(user_id)
                my_gender = data.get("gender")

                if user_id not in self.chat_pair:
                    # remove instance from list
                    if my_gender == "🤴🏻 Boy" and user_id in self.boys:
                        self.boys.remove(user_id)
                    elif my_gender == "👸🏻 Girl" and user_id in self.girls:
                        self.girls.remove(user_id)

                    # user reply
                    context.bot.send_message(chat_id=user_id, text=invalid_destroy())
                else:
                    partner_id = self.chat_pair.get(user_id)

                    # update chat pair
                    del self.chat_pair[user_id]
                    del self.chat_pair[partner_id]

                    context.bot.send_message(chat_id=user_id, text=destroy(who="You"))
                    context.bot.send_message(chat_id=partner_id, text=destroy(who="Your"))

            # if user stop the bot
            except telegram.error.Unauthorized:
                pass

    def command_handler(self):
        updater = Updater(self.bot_key, use_context=True)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start, run_async=True))
        dp.add_handler(MessageHandler(Filters.text, self.message_handler, run_async=True))


        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    bot_name = "One Night Stand"
    bot_key = config.bot_token
    api_id = config.api_id
    api_hash = config.api_hash

    ChatBot(api_id, api_hash, bot_name, bot_key)
