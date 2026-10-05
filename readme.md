# 🕊️ بوت مصداق | Misdaq Telegram Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask%20%7C%20python--telegram--bot-green" alt="Frameworks">
  <img src="https://img.shields.io/badge/AI Engine-Dify%20%7C%20GPT--4o-orange" alt="AI Engine">
  <img src="https://img.shields.io/badge/Deployment-Render-brightgreen" alt="Deployment">
  <img src="https://img.shields.io/badge/Status-Live%2024%2F7-success" alt="Status">
</p>

[العربية](#-باللغة-العربية) | [English](#-english)

---

## 🇸🇦 باللغة العربية

### 🤖 تجربة البوت مباشرة
يمكنك تجربة وتصفح البوت مباشرة عبر التليجرام:
👉 **[اضغط هنا للتحدث مع بوت مصداق على Telegram (@MisdaqHadithbot)](https://t.me/MisdaqHadithbot)**

---

### 📌 عن المشروع
**بوت مصداق (Misdaq Bot)** هو بوت تليجرام ذكي يهدف إلى **التحقق من صحة الأحاديث النبوية الشريفة** والتمييز بين الأحاديث الصحيحة والأحاديث الضعيفة أو الموضوعة. يعتمد البوت على تقنيات الذكاء الاصطناعي المتقدمة وربطه بقواعد بيانات معتمدة لتقديم إجابات دقيقة وموثوقة للمستخدمين على مدار الساعة (24/7).

---

### 🧱 البنية البرمجية والتقنيات المستخدمة

1. **Telegram Bot (`python-telegram-bot`)**: الواجهة البرمجية المباشرة مع المستخدمين لتلقي الأسئلة والأحاديث وإرسال النتائج بشكل منسق.
2. **Dify Chatflow & Knowledge Base**: المحرك الأساسي للتحقق وإدارة التدفق:
   * **القاعدة المعرفية (Knowledge Base)**: فحص الأحاديث الضعيفة والموضوعة المرفوقة عبر ملفات `CSV`.
   * **HTTP Request Node**: الربط المباشر مع API موسوعة الأحاديث النبوية (**HadeethEnc API**) لفحص الأحاديث الصحيحة وإصدار الحكم الدقيق عليها.
   * **GPT-4o**: نموذج الذكاء الاصطناعي لتحليل النصوص، صياغة النتائج، واستخراج الإجابات النهائية ودواعي الحكم بوضوح.
3. **Flask Server Wrapper**: سيرفر ويب مصغر يعمل بالتوازي مع البوت لضمان استمرار تشغيل الخدمة على الاستضافة المجانية بدون انقطاع.
4. **Render.com Deployment**: الاستضافة السحابية المجانية لضمان عمل الخدمة 24/7 مع تأمين التوكنات عبر المتغيرات البيئية (Environment Variables).

---

### 📂 مجلد البيانات والقاعدة المعرفية (Data & Knowledge Base)
تم إتاحة ملفات البيانات الخاصة بالأحاديث الضعيفة والموضوعة بشكل علني للجميع للتحقق والتدقيق المباشر من صحة المحتوى:

* 📁 **[استعراض مجلد البيانات العلني (data/)](./data)**
  * يحتوي على ملفات `CSV` تضم قوائم الأحاديث المفهرسة والمستخدمة في قاعدة Dify المعرفية.

---

### 🚀 كيفية التشغيل والرفع (Deployment)

#### المتغيرات البيئية المطلوب ضبطها (Environment Variables):
يتم ضبط هذه المتغيرات في منصة **Render** تحت قسم `Environment`:

* `TELEGRAM_TOKEN`: توكن البوت الصادر من BotFather.
* `DIFY_API_KEY`: مفتاح الـ API الخاص بتطبيق Dify.

#### ملفات الإعداد:
* **`Procfile`**: يحتوي على أمر بدء السيرفر `web: python main.py`.
* **`requirements.txt`**: يحتوي على المكتبات المطلوبة (`flask`, `python-telegram-bot`, `requests`, `gunicorn`).

---

<br>

---

## 🇬🇧 English

### 🤖 Live Demo & Usage
You can interact with the live bot on Telegram directly:
👉 **[Click here to chat with Misdaq Bot on Telegram (@MisdaqHadithbot)](https://t.me/MisdaqHadithbot)**

---

### 📌 Overview
**Misdaq Bot** is an AI-powered Telegram bot designed to **verify Hadiths** and distinguish authentic Hadiths (*Sahih*) from weak or fabricated ones (*Da'if / Mawdoo'*). The system utilizes modern AI Orchestration (Dify Chatflow) and integrates with trusted Hadith encyclopedias to provide instant, reliable answers 24/7.

---

### 🏗️ Architecture & Stack

1. **Telegram Interface**: Built with `python-telegram-bot` to handle user interactions smoothly.
2. **Dify Chatflow Engine**:
   * **Knowledge Base**: Indexed `CSV` files containing weak and fabricated Hadiths for instant vector search.
   * **HadeethEnc API (HTTP Node)**: Real-time queries to official Hadith databases for authentic Hadiths.
   * **GPT-4o LLM**: Evaluates context, parses API JSON responses, and generates accurate, well-formatted explanations.
3. **Flask Web Wrapper**: Runs concurrently with the Telegram bot polling loop to satisfy Render's HTTP health checks and keep the free tier active.
4. **Render.com**: Cloud hosting environment operating 24/7 with zero-downtime using secure Environment Variables.

---

### 📂 Open Knowledge Base Data
All `CSV` dataset files used to train/index the Dify Knowledge Base are publicly available for inspection and verification:

* 📁 **[Browse Public Data Folder (data/)](./data)**

---

### ⚙️ Environment & Setup

#### Environment Variables Required:
Configure these inside **Render -> Environment**:

* `TELEGRAM_TOKEN`: Bot authentication token provided by Telegram's BotFather.
* `DIFY_API_KEY`: API access key for the Dify Chatflow application.

#### Execution Entrypoint:
* **Procfile**: `web: python main.py`

---
<p align="center">
Developed with ❤️ for verifying and spreading authentic Islamic knowledge.
</p>
