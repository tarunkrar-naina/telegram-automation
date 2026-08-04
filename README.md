# Telegram AI Agent 🤖
### (Groq AI + SerpAPI + Supabase + Render)

Ye ek **personal AI agent** hai jise aap Telegram par directly message karke kaam karwa sakte hain:
- "Aaj ki top tech news batao" → Google search karke Groq AI se jawab dega
- "Ye news channel mein post karo" → search + jawab + apne channel mein auto-post
- Koi bhi sawaal poochein → live web search + AI jawab

Iske saath-saath, **background mein automatically** din mein 3 baar (9 AM, 2 PM, 8 PM) channel mein content bhi post hota rahega (News/Quiz/Motivational rotation) — bina aapko kuch bole.

---

## PART 1: Saari API Keys Lena

### 1. Groq API Key (AI ke liye — bahut fast aur free hai)
1. https://console.groq.com par jaakar sign up karein
2. Left sidebar mein **"API Keys"** → **"Create API Key"**
3. Key copy karke save kar lein
4. Groq ka **free tier generous hai**, is scale ke liye kaafi hoga

### 2. SerpAPI Key (Google Search ke liye)
1. https://serpapi.com/users/sign_up par free account banayen
2. Dashboard mein **API Key** milegi
3. Free plan: 100 searches/month

### 3. Unsplash Access Key (Images ke liye)
1. https://unsplash.com/developers → Register → New Application
2. **Access Key** copy karein

### 4. Supabase (Database)
1. https://supabase.com par free project banayen (region: Mumbai select karein)
2. **SQL Editor** mein jaakar is repo ki `supabase_setup.sql` file ka **pura content paste karke Run** karein
   - Isse 2 tables ban jayengi: `posted_content` aur `chat_history`
3. **Project Settings → API** se:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_KEY`

### 5. Apna Telegram Chat ID Nikalna (Security ke liye)
Ye zaroori hai taaki sirf AAP hi apne agent ko command de sakein, koi aur nahi:
1. Telegram mein **@userinfobot** ko search karke `/start` bhejein
2. Wo aapko aapka **Chat ID** (ek number) bhejega — ise copy kar lein → ye `OWNER_CHAT_ID` hai

### 6. Telegram Bot Token + Channel ID
Aapke paas already hai:
- Bot Token: BotFather se
- Channel ID: `@TarunFitnessHub`

---

## PART 2: VS Code Mein Setup

1. Is `telegram-ai-agent` folder ko VS Code mein open karein (**File → Open Folder**)
2. Terminal kholein (`Ctrl + ~`)
3. (Optional local testing) Virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   pip install -r requirements.txt
   ```

---

## PART 3: GitHub Par Push Karna

```bash
git init
git add .
git commit -m "Telegram AI Agent - Groq + SerpAPI + Supabase"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-agent.git
git push -u origin main
```

---

## PART 4: Render Par Deploy Karna

1. https://render.com → sign up (GitHub se login karna asaan hai)
2. **"New +" → "Web Service"** → apna repo select karein
3. Settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
4. **Environment Variables** mein ye 8 keys add karein:

   | Key | Value |
   |---|---|
   | `TELEGRAM_BOT_TOKEN` | BotFather wala token |
   | `TELEGRAM_CHANNEL_ID` | `@TarunFitnessHub` |
   | `OWNER_CHAT_ID` | Aapka personal chat ID (Part 1, Step 5) |
   | `GROQ_API_KEY` | Groq wali key |
   | `SERPAPI_KEY` | SerpAPI wali key |
   | `UNSPLASH_ACCESS_KEY` | Unsplash wali key |
   | `SUPABASE_URL` | Supabase project URL |
   | `SUPABASE_KEY` | Supabase anon key |

5. **"Create Web Service"** click karein - deploy hone mein 2-5 minute lagenge
6. Deploy hone ke baad aapko URL milega, jaise: `https://telegram-ai-agent.onrender.com`

---

## PART 5: Bot Ko Webhook Se Connect Karna (Zaroori Step!)

Iske bina bot aapke messages receive nahi karega. Browser mein ye URL kholein (apni values daal kar):

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app-name.onrender.com/webhook
```

Example:
```
https://api.telegram.org/bot7123456789:AAHxxxxx/setWebhook?url=https://telegram-ai-agent.onrender.com/webhook
```

Response mein `"ok":true` dikhna chahiye. Iska matlab webhook set ho gaya!

---

## PART 6: Test Karna

1. Apna bot Telegram mein kholein (`@TarunFitnessHubBot`) aur `/start` bhejein
2. Ab kuch bhi poochein: **"Aaj ki cricket news batao"**
3. Bot Google search karke aur Groq AI se jawab dega!
4. Try karein: **"Ye news channel mein post kar do"** — reply channel mein bhi chala jayega

Home route check: `https://your-app-name.onrender.com/` par `"status": "running"` dikhna chahiye

---

## ⚠️ Render Free Tier Ko Awake Rakhna

Free plan 15 min inactivity ke baad so jaata hai. Isse bachne ke liye:
1. https://uptimerobot.com par free account
2. **Add New Monitor** → HTTP(s) → apna Render URL
3. Interval: 5 minutes

---

## Security Note

`OWNER_CHAT_ID` set karna **bahut zaroori hai**, warna koi bhi random insaan jo aapke bot ko dhoondh le (agar username public hai), wo bhi agent use kar sakega aur aapke API credits/quota use ho sakte hain.

---

## File Structure

```
telegram-ai-agent/
├── app.py                   # Flask server: webhook route + auto-poster scheduler
├── bot.py                   # Telegram update handler
├── agent.py                 # Core AI agent logic (search + reasoning + reply)
├── groq_client.py           # Groq API wrapper
├── database.py              # Supabase: chat history + duplicate-check
├── telegram_poster.py       # Telegram ko messages/photos bhejna
├── supabase_setup.sql       # Database tables banane ka SQL
├── content/
│   ├── serp_search.py       # SerpAPI: Google search + Google news
│   ├── news_writer.py       # Groq se news caption likhwana
│   ├── trending_news.py     # Auto-poster ke liye trending news pipeline
│   ├── quiz.py               # Trivia quiz (free, no key)
│   └── motivational.py      # Quote + Unsplash image
├── requirements.txt
├── render.yaml
└── .env.example
```

## Kaise Kaam Karta Hai

**Jab aap bot ko message karte hain:**
```
Aap: "Best budget phone 2026 batao"
        │
        ▼
  SerpAPI se Google search
        │
        ▼
  Groq AI ko search results + question diya jata hai
        │
        ▼
  Groq ek accurate, contextual jawab likhta hai
        │
        ▼
  Reply aapko Telegram par milta hai
  (agar "channel mein post karo" bola to channel mein bhi chala jata hai)
```

**Background mein (automatically, bina bole):**
```
9 AM / 2 PM / 8 PM
        │
        ▼
  Trending News ya Quiz ya Motivational (rotation)
        │
        ▼
  Duplicate check (Supabase)
        │
        ▼
  Channel mein auto-post
```
