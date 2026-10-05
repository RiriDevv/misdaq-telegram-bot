

import os
import requests
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
# 1. إعداد المفاتيح والروابط
# ==========================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8971556314:AAGKW_isCvcmvc4MZ4SWUcq-aM7dmwSaJsg")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "app-NtzsG3LiLC3Vbk5iwC0F6O7j")
DIFY_URL = "https://api.dify.ai/v1/chat-messages"

# قاموس لتخزين رقم المحادثة لكل مستخدم للحفاظ على سياق Dify Chatflow
user_conversations = {}


# ==========================================
# 2. دالة الاتصال بـ Dify API
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
# 3. معالجات أوامر التليجرام (Handlers)
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = "أهلاً بك في بوت (مصداق) لتوثيق الأحاديث الشريفة. أرسل نص الحديث للتحقق منه."
    await update.message.reply_text(welcome_msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # إظهار حالة "جاري الكتابة..." للمستخدم
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # إرسال السؤال لـ Dify واستلام الرد
    reply_text = ask_dify(user_id, user_text)

    # إرسال الرد المباشر للمستخدم
    await update.message.reply_text(reply_text)


# ==========================================
# 4. تشغيل البوت
# ==========================================
if __name__ == "__main__":
    print("🚀 البوت يعمل الآن وجاهز للاستقبال...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()