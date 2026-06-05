from flask import Flask, request, render_template_string, redirect
import random, string, datetime, os, hashlib, requests
app = Flask(__name__)
FILE_LOG = "riwayat.txt"

HTML = '''<!DOCTYPE html>
<html><head><title>Password Guard Pro</title>
<meta name=viewport content="width=device-width,initial-scale=1">
<style>
:root{--bg1:#667eea;--bg2:#764ba2;--box:#fff;--text:#333;--muted:#666;--input:#f5f5f5;--danger:#ff4d4d;--safe:#4caf50}
body.dark{--bg1:#1a1a2e;--bg2:#16213e;--box:#2a2a3e;--text:#eee;--muted:#aaa;--input:#1e1e2e}
*{box-sizing:border-box;transition:0.3s}
body{font-family:'Segoe UI',Arial;background:linear-gradient(135deg,var(--bg1) 0%,var(--bg2) 100%);display:flex;justify-content:center;align-items:flex-start;min-height:100vh;margin:0;padding:20px;color:var(--text)}
.container{width:100%;max-width:500px}
.box{background:var(--box);padding:30px;border-radius:20px;margin-bottom:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
h1{text-align:center;margin-top:0}
.topbar{display:flex;justify-content:space-between;margin-bottom:20px}
.btn-small{padding:8px 15px;background:var(--input);border:none;border-radius:8px;cursor:pointer;font-size:13px;color:var(--text)}
.btn-danger{background:var(--danger);color:white}
input{width:100%;padding:14px 45px 14px 14px;margin:10px 0;border:2px solid var(--input);border-radius:10px;font-size:16px;background:var(--input);color:var(--text)}
.input-wrap{position:relative}
.toggle{position:absolute;right:12px;top:50%;transform:translateY(-50%);cursor:pointer;font-size:20px}
.btn{width:100%;padding:14px;background:linear-gradient(135deg,var(--bg1) 0%,var(--bg2) 100%);color:white;border:none;border-radius:10px;font-size:16px;font-weight:bold;cursor:pointer;margin-top:10px}
.btn-gen{background:linear-gradient(135deg,#ff6b6b 0%,#ff8e8e 100%);margin-top:8px}
.bar{height:18px;background:var(--input);border-radius:12px;margin-top:20px;overflow:hidden}
.fill{height:100%;transition:width 0.6s;border-radius:12px}
.lemah{background:#ff4d4d}.sedang{background:#ffa500}.kuat{background:#4caf50}.aman{background:#2196f3}
.skor{font-size:24px;font-weight:bold;margin-top:15px;text-align:center}
.saran{margin-top:15px;padding:12px;background:var(--input);border-radius:8px;font-size:14px;color:var(--muted)}
.gen-box{margin-top:20px;padding:15px;background:var(--input);border-radius:10px;text-align:center}
.gen-pass{font-family:monospace;font-size:18px;font-weight:bold;word-break:break-all;margin:10px 0}
.riwayat{max-height:200px;overflow-y:auto}
.riwayat-item{padding:10px;background:var(--input);margin:5px 0;border-radius:8px;font-size:13px;display:flex;justify-content:space-between}
.badge{padding:3px 8px;border-radius:5px;font-size:12px;font-weight:bold;color:white}
.grafik{display:flex;align-items:flex-end;gap:5px;height:120px;margin-top:15px;padding:10px;background:var(--input);border-radius:10px}
.bat{flex:1;background:var(--bg1);border-radius:4px 4px 0 0;position:relative;min-height:10px;transition:height 0.5s}
.bat span{position:absolute;bottom:-20px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--muted)}
.bocor-safe{background:var(--safe);padding:12px;border-radius:8px;margin-top:15px;text-align:center;font-weight:bold}
.bocor-danger{background:var(--danger);padding:12px;border-radius:8px;margin-top:15px;text-align:center;font-weight:bold;color:white}
</style>
<script>
function togglePass(){let x=document.getElementById("pwd");let t=document.getElementById("toggle");if(x.type==="password"){x.type="text";t.innerHTML="🙈"}else{x.type="password";t.innerHTML="👁️"}}
function toggleTheme(){document.body.classList.toggle("dark");localStorage.theme=document.body.classList.contains("dark")?"dark":"light"}
if(localStorage.theme==="dark")document.body.classList.add("dark");
function copyPass(){let p=document.getElementById("gen").innerText;navigator.clipboard.writeText(p);alert("Disalin!")}
function hapusRiwayat(){if(confirm("Yakin hapus semua riwayat?"))location.href="/hapus"}
</script>
</head>
<body><div class=container>
<div class=box>
<div class=topbar><h1 style=margin:0>🔒 Password Guard Pro</h1><button class=btn-small onclick=toggleTheme()>🌙/☀️</button></div>
<form method=POST><div class=input-wrap><input id=pwd type=password name=password placeholder="Ketik password..." value="{{pwd}}" required><span id=toggle class=toggle onclick=togglePass()>👁️</span></div><button class=btn>CEK KEKUATAN</button></form>
<button class="btn btn-gen" onclick="location.href='/?gen=1'">⚡ GENERATE PASSWORD KUAT</button>
{% if gen_pass %}<div class=gen-box><div>Password Kuat Kamu:</div><div id=gen class=gen-pass>{{gen_pass}}</div><button class=btn-small onclick=copyPass()>📋 Salin</button></div>{% endif %}
{% if hasil %}
<div class=bar><div class="fill {{kelas}}" style="width:{{persen}}%"></div></div>
<div class=skor>{{hasil}} - {{skor}}/4</div>
<div class=saran><b>💡 Saran:</b> {{saran}}</div>
{% if bocor_msg %}<div class="{{bocor_kelas}}">{{bocor_msg}}</div>{% endif %}
{% endif %}
</div>

{% if riwayat %}
<div class=box>
<h3 style=margin-top:0>📊 Grafik Kekuatan</h3>
<div class=grafik>
{% for r in riwayat %}
<div class="bat {{r.kelas}}" style="height:{{r.skor|int * 25}}px"><span>{{r.skor}}</span></div>
{% endfor %}
</div>

<div style="display:flex;justify-content:space-between;align-items:center;margin-top:25px;margin-bottom:15px">
<h3 style=margin:0>📜 Riwayat Cek</h3>
<button class="btn-small btn-danger" onclick=hapusRiwayat()>🗑️ Hapus</button>
</div>
<div class=riwayat>
{% for r in riwayat %}
<div class=riwayat-item>
<div><span class="badge {{r.kelas}}">{{r.hasil}} {{r.skor}}/4</span></div>
<div style="color:var(--muted)">{{r.waktu}}</div>
</div>
{% endfor %}
</div>
</div>
{% endif %}
</div></body></html>'''

def cek(p):
    s=0; sr=[]
    if len(p)>=12: s+=1
    elif len(p)>=8: sr.append("Tambah jadi 12+ karakter")
    else: sr.append("Minimal 8 karakter")
    if any(c.isupper() for c in p): s+=1
    else: sr.append("Pakai huruf BESAR")
    if any(c.isdigit() for c in p): s+=1
    else: sr.append("Pakai angka 0-9")
    if any(c in "!@#$%^&*()_+-=" for c in p): s+=1
    else: sr.append("Pakai simbol !@#$%")
    if s==0: h,k="SANGAT LEMAH","lemah"
    elif s==1: h,k="LEMAH","lemah"
    elif s==2: h,k="SEDANG","sedang"
    elif s==3: h,k="KUAT","kuat"
    else: h,k="AMAN BANGET","aman"
    saran = ", ".join(sr) if sr else "Perfect! Sudah sangat aman"
    return h,s,k,s*25,saran

def cek_bocor(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        res = requests.get(url, timeout=5)
        hashes = (line.split(':') for line in res.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"🚨 PERNAH BOCOR {count} KALI! Ganti password sekarang!", "bocor-danger"
        return "✅ Password AMAN, belum pernah bocor di database hacker", "bocor-safe"
    except:
        return None, None

def gen_pass():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        p = ''.join(random.choice(chars) for _ in range(16))
        if any(c.isupper() for c in p) and any(c.isdigit() for c in p) and any(c in "!@#$%^&*" for c in p):
            return p

def simpan_riwayat(hasil, skor, kelas):
    waktu = datetime.datetime.now().strftime("%d/%m %H:%M")
    baris = f"{waktu}|{hasil}|{skor}|{kelas}\n"
    with open(FILE_LOG, "a") as f:
        f.write(baris)

def baca_riwayat():
    if not os.path.exists(FILE_LOG): return []
    with open(FILE_LOG, "r") as f:
        lines = f.readlines()[-10:]
    data=[]
    for l in lines:
        w,h,s,k = l.strip().split("|")
        data.append({"waktu":w,"hasil":h,"skor":s,"kelas":k})
    return data[::-1]

@app.route("/",methods=["GET","POST"])
def home():
    pwd=""; gen_pass=None; bocor_msg=None; bocor_kelas=None
    if request.args.get("gen"): gen_pass=gen_pass()
    if request.method=="POST":
        pwd=request.form.get("password","")
        h,s,k,pr,sr=cek(pwd)
        bocor_msg, bocor_kelas = cek_bocor(pwd)
        simpan_riwayat(h,s,k)
        return render_template_string(HTML,hasil=h,skor=s,kelas=k,persen=pr,saran=sr,pwd="",gen_pass=gen_pass,riwayat=baca_riwayat(),bocor_msg=bocor_msg,bocor_kelas=bocor_kelas)
    return render_template_string(HTML,pwd="",gen_pass=gen_pass,riwayat=baca_riwayat())

@app.route("/hapus")
def hapus():
    if os.path.exists(FILE_LOG): os.remove(FILE_LOG)
    return redirect("/")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000)