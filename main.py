import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ==========================================
# 1. إعداد سيرفر الويب (Flask) لإبقاء Render نشطاً
# ==========================================
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# تشغيل سيرفر الويب في خلفية مستقلة (Daemon Thread)
threading.Thread(target=run_web, daemon=True).start()


# ==========================================
# 2. إعداد المفاتيح والمتغيرات البيئية
# ==========================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8971556314:AAGKW_isCvcmvc4MZ4SWUcq-aM7dmwSaJsg")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "app-NtzsG3LiLC3Vbk5iwC0F6O7j")
DIFY_URL = "https://api.dify.ai/v1/chat-messages"

# قاموس لتخزين رقم المحادثة لكل مستخدم للحفاظ على سياق Dify Chatflow
user_conversations = {}


# ==========================================
# 3. دالة الاتصال بـ Dify API
# ==========================================
def ask_dify(user_id: int, message_text: str) -> str:
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {},
        "query": message_text,
        "response_mode": "blocking",
        "user": str(user_id),
        "conversation_id": user_conversations.get(user_id, "")
    }

    try:
        response = requests.post(DIFY_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            # حفظ conversation_id للمحادثات القادمة
            if "conversation_id" in data and data["conversation_id"]:
                user_conversations[user_id] = data["conversation_id"]
            
            # 1. فحص المخرجات المخصصة للـ Workflow أولاً (Outputs)
            if "data" in data and isinstance(data["data"], dict) and "outputs" in data["data"]:
                outputs = data["data"]["outputs"]
                if isinstance(outputs, dict):
                    result_text = outputs.get("result") or outputs.get("text") or outputs.get("answer")
                    if result_text:
                        return str(result_text)

            # 2. فحص الرد المباشر (answer)
            if "answer" in data and data["answer"]:
                return str(data["answer"])
            
            return "تمت معالجة الطلب ولكن لم يتوفر نص للرد."
            
        else:
            print(f"Dify API Error: {response.status_code} - {response.text}")
            return "تعذر الاتصال بخدمة التحقق حالياً. يرجى المحاولة لاحقاً."
            
    except Exception as e:
        print(f"Exception in ask_dify: {e}")
        return "حدث خطأ أثناء الاتصال بالنظام."


# ==========================================
# 4. معالجات أوامر التليجرام (Handlers)
# ==========================================

# دالة التعامل مع أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "أهلاً بك في **بوت مصداق** 🕊️✨\n\n"
        "أنا هنا لمساعدتك في **التحقق من صحة الأحاديث النبوية الشريفة**، والتمييز بين الأحاديث الصحيحة والضعيفة أو الموضوعة.\n\n"
        "💬 **طريقة الاستخدام:**\n"
        "أرسل لي نص الحديث أو جزءاً منه في المحادثة مباشرة، وسأقوم بالتحقق منه فوراً!"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')


# دالة التعامل مع الرسائل النصية الموجهة لـ Dify
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # إظهار حالة "جاري الكتابة..." للمستخدم أثناء معالجة الطلب
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # إرسال السؤال لـ Dify واستلام الرد
    reply_text = ask_dify(user_id, user_text)

    # إرسال الرد المباشر للمستخدم
    await update.message.reply_text(reply_text)


# ==========================================
# 5. تشغيل البوت
# ==========================================
if __name__ == "__main__":
    print("🚀 البوت يعمل الآن وجاهز للاستقبال...")
    bot_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # إضافة المعالجات (Handlers)
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # بدء استقبال الرسائل عبر Polling
    bot_app.run_polling()