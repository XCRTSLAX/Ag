import os
from tamtam_bot import Bot, Dispatcher
from tamtam_bot.utils.deprecated import construct_action_data

# استبدال ACCESS_TOKEN بتوكن البوت الخاص بك
ACCESS_TOKEN = os.environ.get('XzgPQGjHPzXu-ptpZuBSpZaFZnbdiHxfoQb4Q5WcXAM', None)
bot = Bot(ACCESS_TOKEN)
dispatcher = Dispatcher(bot)

# قائمة الكلمات الممنوعة
forbidden_words = ["bad_word_1", "bad_word_2", "bad_word_3"]

# وظيفة للكشف عن الكلمات الممنوعة في الرسائل وإرسال رسالة تحذيرية للمستخدم
async def check_forbidden_words(update):
    message = update.message.body.text.lower()
    for word in forbidden_words:
        if word in message:
            user_id = update.message.sender.user_id
            chat_id = update.message.recipient.chat_id
            await bot.send_message(chat_id=chat_id, text=f"⚠️ تم اكتشاف استخدام كلمة غير لائقة! الرجاء عدم استخدام هذه الكلمات {user_id}")
            return True
    return False

# وظيفة لحذف الرسائل التي تحتوي على الكلمات الممنوعة
async def delete_forbidden_messages(update):
    message = update.message
    if await check_forbidden_words(update):
        await bot.delete_message(chat_id=message.recipient.chat_id, message_id=message.body.mid)

# وظيفة للرد على الرسائل الخاصة بالبوت
async def handle_bot_message(update):
    message = update.message
    user_id = message.sender.user_id
    chat_id = message.recipient.chat_id
    text = message.body.text.lower()

    # التحقق من أن الرسالة هي رسالة خاصة بالبوت
    if user_id == bot.user_id:
        return

    # الرد على الرسائل الخاصة بالبوت
    if text == '/start':
        await bot.send_message(chat_id=chat_id, text="مرحبا! أنا بوت الحماية. سأحمي هذه المجموعة من الكلمات النابية والرد على المستخدمين الذين يتحدثون بشكل غير لائق.")
    else:
        await bot.send_message(chat_id=chat_id, text="شكرا للتحدث معي! سأحمي هذه المجموعة بكل ما لدي من قدرات.")

# تسجيل الوظائف مع المراقب
dispatcher.register_message_handler(handle_bot_message, is_bot=True)
dispatcher.register_message_handler(delete_forbidden_messages)

# بدء البوت
bot.run()
