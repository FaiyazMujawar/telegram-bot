import telegram
from functools import wraps
from telegram import ChatAction

from data import dictionary
from utils import utils


def send_typing_action(func):
    """ Set the status to 'typing' in the chat"""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)
    return command_func


@send_typing_action
def start(update, context):
    start_message = "Hi!\nI'm the dictionary 📕 bot. I can help you get the definitions of the English words 🔍"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=start_message
    )


@send_typing_action
def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Sorry, but I did\'nt understand that! 😔'
    )


@send_typing_action
def get_meaning(update, context):
    """
    Get the meaning of the word
    """
    try:
        # Exctracting the word to search from the message
        word: str = update.message.text.split()[1]

        # Getting the word meaning
        try:
            result = dictionary.search_meaninig(word=word)
            meaning_string = utils.get_meaning_text(result=result)

            # Sending the meaning
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="\n".join(
                    meaning_string), parse_mode=telegram.ParseMode.MARKDOWN_V2
            )

            # Sending the pronunciation audio
            context.bot.send_audio(
                chat_id=update.effective_chat.id, audio=result['audio'], title=result['word'], caption='Pronunciation')
        except ValueError:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Sorry! I coudln\'t find the word for you! 😔'
            )
        except Exception:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Sorry! Something on my side broke down! 😔'
            )
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Please provide something to search, of course I can\'t search the empty space 😜'
        )
