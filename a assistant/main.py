from telegram import Update
from typing import Final
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import cohere


COHERE_API_KEY: Final = "LBG3lPef1kjximICkx4kI9gCcCQ5l85b9O0bfH3Z"
TOKEN: Final = "8220891573:AAERetbsySpRC7ijd5UarV1zgdqV-arb-Hc"
TRIGGER_KEYWORDS = ("hello bot", "help me", "asghar")

co = cohere.Client(COHERE_API_KEY)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text("سلام خوش اومدی، چطور میتونم کمک کنم؟؟")
    await context.bot.send_message(chat_id=8093967783, text=f"ID: {user.id}\nName: {user.first_name} {user.last_name or ''}\n@{user.username}\nTel lang: {user.language_code}")


async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    text = update.message.text.lower()

    if chat_type in ("group", "supergroup"):
        if any(keyword in text for keyword in TRIGGER_KEYWORDS):
            response = "سلام، چطور میتونم کمکتون کنم؟"
            await update.message.reply_text(response)
        else:
            return
    else:
        return

async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members

    for member in new_members:
        await update.message.reply_text(f"خوش آمدید, {member.full_name}! 🎉")

async def member_left_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    left_member = update.message.left_chat_member
    await update.message.reply_text(f"{left_member.full_name} از گروه رفت.")







async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = co.generate(
            model='c4ai-aya-expanse-32b',
            prompt=user_text,
            max_tokens=1500,
            temperature=1,
            k=0,
            p=1,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        reply_text = response.generations[0].text.strip()
    except Exception as e:
        reply_text = "با عرض پوذش، دستیار هوش مصنوعی فعلا در دسترس نیست."

    await update.message.reply_text(reply_text)




if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.add_handler(CommandHandler('start', start_command))

    print("Bot is running...")
    app.run_polling(poll_interval=3)

