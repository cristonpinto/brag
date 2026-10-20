import json, os
os.chdir('/home/user/brag/flow-video/composition')
vo = json.load(open('vo.json'))
keys = [f"s{i:02d}" for i in range(1, 14)]
pad = {k: 0.5 for k in keys}
pad['s05'] = 1.4; pad['s06'] = 0.6; pad['s13'] = 2.2
LEAD = 0.8
ST, DUR = {}, {}
t = LEAD
for k in keys:
    ST[k] = round(t, 3); DUR[k] = round(vo[k] + pad[k], 3); t += DUR[k]
TOTAL = round(t, 3)

def person(c1, c2, w=120):
    return f'''<svg viewBox="0 0 100 120" width="{w}" height="{int(w*1.2)}"><defs><linearGradient id="pg{c1[1:]}{w}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><circle cx="50" cy="32" r="22" fill="url(#pg{c1[1:]}{w})"/><path d="M8 118 C8 78 28 62 50 62 C72 62 92 78 92 118 Z" fill="url(#pg{c1[1:]}{w})"/></svg>'''

NOTE = '<svg viewBox="0 0 24 24" width="150" height="150" fill="none" stroke="#f3ead8" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>'
LEAF = '<svg viewBox="0 0 24 24" width="150" height="150" fill="none" stroke="#f3ead8" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19C5 10 10 5 20 4c0 10-5 15-14 15z"/><path d="M5 19c3-5 6-8 10-10"/></svg>'
PIN = '<svg viewBox="0 0 24 24" width="84" height="84" fill="none" stroke="#e8a33d" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>'
SHIELD = '<svg width="520" height="650" viewBox="3.2 1 17.6 22" preserveAspectRatio="none" fill="rgba(63,208,201,0.08)" stroke="#3fd0c9" stroke-width="0.45" stroke-linejoin="round"><path d="M12 2l8 3v6c0 5.2-3.4 9.3-8 11-4.6-1.7-8-5.8-8-11V5z"/></svg>'
CURSOR = '<svg viewBox="0 0 24 24" width="46" height="46"><path d="M4 2l15 9-7 1.6L9 20z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
def cursor(id_):
    return f'<div class="abs cursor" id="{id_}" style="left:0;top:0;opacity:0;z-index:50;">{CURSOR}<div class="ripple" id="{id_}-r"></div></div>'

def chip(id_, text, x, y, w=560, cls='', style=''):
    return f'<div class="abs chip {cls}" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;{style}">{text}</div>'

SC = {}

# ---------- S01
gens = ''.join(f'<div class="abs gen" id="g{i}" style="left:{170+i*345}px; top:{250+[0,0,15,45,80][i]}px;">{person(["#e8a33d","#d9873a","#cf6f3a","#c75a3a","#c0453a"][i], "#6b2b1d", [150,150,140,120,100][i])}</div>' for i in range(5))
SC['s01'] = f'''
<div class="abs serif" id="s01t" style="left:0;width:1920px;top:50px;text-align:center;font-size:68px;">Passed down, generation to generation</div>
{gens}
<div class="abs orb" id="s01orb" style="left:0;top:0;opacity:0;"></div>
{chip('s01a','Traditional knowledge',110,470,540,'amberc')}
{chip('s01b','Skills',730,470,260,'amberc')}
{chip('s01c','Cultural practices',1060,470,470,'amberc')}
<div class="abs card tile" id="s01m" style="left:100px;top:600px;width:400px;height:360px;"><img src="assets/img/kana.jpg" alt=""/><div class="tl">Traditional masks</div></div>
<div class="abs card tile" id="s01f" style="left:540px;top:600px;width:400px;height:360px;background:linear-gradient(160deg,#7a3a1f,#2b1410);"><div class="ic">{NOTE}</div><div class="tl">Folk songs</div></div>
<div class="abs card tile" id="s01h" style="left:980px;top:600px;width:400px;height:360px;background:linear-gradient(160deg,#2f6a3b,#10241a);"><div class="ic">{LEAF}</div><div class="tl">Traditional medicinal knowledge</div></div>
<div class="abs card tile dashed" id="s01x" style="left:1420px;top:600px;width:400px;height:360px;"><div class="ic serif" style="font-size:120px;color:#e8a33d;">+</div><div class="tl">Many other forms of cultural expression</div></div>
'''

# ---------- S02
SC['s02'] = f'''
<div class="abs eyebrow" id="s02e" style="left:120px;top:110px;">An example · Traditional masks</div>
<div class="abs card pinc" id="s02p" style="left:120px;top:190px;width:800px;height:260px;"><div style="position:absolute;left:46px;top:84px;">{PIN}</div><div class="abs serif" style="left:160px;top:50px;font-size:104px;line-height:1.1;">Ambalangoda</div><div class="abs" style="left:166px;top:176px;font-size:46px;color:#b9ad99;">Sri Lanka</div></div>
<div class="abs serif" id="s02h" style="left:120px;top:520px;font-size:64px;width:800px;">Traditional mask makers</div>
{chip('s02a','Unique skills',120,640,560,'amberc')}
{chip('s02b','Techniques',120,740,560,'amberc')}
{chip('s02c','Cultural knowledge',120,840,560,'amberc')}
<div class="abs card ph" id="s02i1" style="left:1090px;top:130px;width:430px;height:430px;"><img src="assets/img/ginijala.jpg" alt=""/></div>
<div class="abs card ph" id="s02i2" style="left:1380px;top:380px;width:430px;height:430px;"><img src="assets/img/deva.jpg" alt=""/></div>
<div class="abs card ph" id="s02i3" style="left:1020px;top:610px;width:400px;height:400px;"><img src="assets/img/maru.jpg" alt=""/></div>
'''

# ---------- S03
SC['s03'] = f'''
<div class="abs serif" id="s03h" style="left:0;width:1920px;top:60px;text-align:center;font-size:74px;">Not simply <span id="s03s" class="strike">artistic objects</span></div>
<div class="abs glow" id="s03g" style="left:560px;top:230px;width:800px;height:800px;"></div>
<div class="abs card" id="s03m" style="left:700px;top:290px;width:520px;height:520px;"><img src="assets/img/bihiri.jpg" alt=""/></div>
<div class="abs line" id="s03l1" style="left:470px;top:395px;width:230px;height:3px;transform-origin:100% 50%;"></div>
<div class="abs line" id="s03l2" style="left:1220px;top:395px;width:230px;height:3px;transform-origin:0% 50%;"></div>
<div class="abs line" id="s03l3" style="left:470px;top:705px;width:230px;height:3px;transform-origin:100% 50%;"></div>
<div class="abs line" id="s03l4" style="left:1220px;top:705px;width:230px;height:3px;transform-origin:0% 50%;"></div>
<div class="abs serif lab" id="s03w1" style="left:100px;top:352px;width:360px;text-align:right;">History</div>
<div class="abs serif lab" id="s03w2" style="left:1460px;top:352px;width:360px;">Identity</div>
<div class="abs serif lab" id="s03w3" style="left:100px;top:662px;width:360px;text-align:right;">Beliefs</div>
<div class="abs serif lab" id="s03w4" style="left:1460px;top:662px;width:400px;line-height:1.05;">Cultural<br/>heritage</div>
<div class="abs" id="s03f" style="left:0;width:1920px;top:900px;text-align:center;font-size:44px;color:#b9ad99;">…of the communities that create them</div>
'''

# ---------- S04
SC['s04'] = f'''
<div class="abs serif" id="s04h" style="left:940px;top:100px;font-size:62px;width:900px;line-height:1.1;">A visitor in Ambalangoda</div>
<div class="abs phone" id="s04ph" style="left:360px;top:80px;width:440px;height:920px;">
  <div class="screen" style="position:absolute;left:20px;top:20px;width:400px;height:880px;border-radius:44px;overflow:hidden;background:#0b0b0b;">
    <img id="s04v1" class="abs" src="assets/img/deva.jpg" style="left:-150px;top:90px;width:700px;height:700px;opacity:0;"/>
    <img id="s04v2" class="abs" src="assets/img/maru.jpg" style="left:-150px;top:90px;width:700px;height:700px;opacity:0;"/>
    <img id="s04v3" class="abs" src="assets/img/ginijala.jpg" style="left:-150px;top:90px;width:700px;height:700px;opacity:0;"/>
    <div class="abs" id="s04fb" style="left:80px;top:300px;width:240px;height:240px;border:3px solid #ffd54a;border-radius:10px;opacity:0;"></div>
    <div class="abs" style="left:0;top:0;width:400px;height:90px;background:rgba(0,0,0,.55);"></div>
    <div class="abs" style="left:24px;top:36px;font-size:24px;color:#fff;font-weight:600;">PHOTO</div>
    <div class="abs" style="left:0;top:790px;width:400px;height:90px;background:rgba(0,0,0,.55);"></div>
    <div class="abs" id="s04sh" style="left:164px;top:800px;width:72px;height:72px;border-radius:50%;border:5px solid #fff;"><div style="position:absolute;inset:6px;border-radius:50%;background:#fff;"></div></div>
    <div class="abs" id="s04fl" style="left:0;top:0;width:400px;height:880px;background:#fff;opacity:0;"></div>
  </div>
</div>
<div class="abs card loc" id="s04c1" style="left:940px;top:270px;width:880px;height:200px;"><img src="assets/img/deva.jpg" alt=""/><div class="lt serif">Museum</div></div>
<div class="abs card loc" id="s04c2" style="left:940px;top:500px;width:880px;height:200px;"><img src="assets/img/maru.jpg" alt=""/><div class="lt serif">Cultural centre</div></div>
<div class="abs card loc" id="s04c3" style="left:940px;top:730px;width:880px;height:200px;"><img src="assets/img/ginijala.jpg" alt=""/><div class="lt serif">Local shop</div></div>
'''

# ---------- S05
thumbs = ''.join(f'<div class="abs card up" id="s05t{i+1}" style="left:{190+i*190}px;top:300px;width:170px;height:170px;"><img src="assets/img/{n}.jpg" alt=""/><div class="ck">✓</div></div>' for i, n in enumerate(['deva', 'maru', 'ginijala']))
res = ''.join(f'<div class="abs card gen6" id="s05r{i+1}" style="left:{880+(i%3)*290}px;top:{300+(i//3)*290}px;width:270px;height:270px;"><img src="assets/img/ai{i+1}.jpg" alt=""/></div>' for i in range(6))
SC['s05'] = f'''
<div class="abs win" id="s05w0" style="left:130px;top:100px;width:1660px;height:880px;">
  <div class="bar"><span class="d" style="background:#ff5f57"></span><span class="d" style="background:#febc2e"></span><span class="d" style="background:#28c840"></span><div class="url">generative-ai.example</div></div>
  <div class="abs" style="left:40px;top:84px;font-size:34px;font-weight:700;color:#3fd0c9;">✦ Generative AI</div>
</div>
<div class="abs" style="left:190px;top:235px;font-size:28px;color:#8fa;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:#7fd8d3;">Reference photos</div>
<div class="abs drop" id="s05d" style="left:170px;top:280px;width:600px;height:210px;"><span id="s05dt">Drop photographs here</span></div>
{thumbs}
<div class="abs" style="left:190px;top:540px;font-size:28px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:#7fd8d3;">Prompt</div>
<div class="abs prompt" id="s05p" style="left:170px;top:585px;width:600px;height:150px;"><span id="s05pt"></span><span class="caret">|</span></div>
<div class="abs gbtn" id="s05g" style="left:170px;top:775px;width:600px;height:90px;">Generate</div>
<div class="abs" id="s05prog" style="left:170px;top:880px;width:600px;height:8px;background:#1c2a2a;border-radius:4px;"><div id="s05pf" style="width:0;height:8px;background:#3fd0c9;border-radius:4px;"></div></div>
{res}
<div class="abs" id="s05cap" style="left:880px;top:880px;font-size:26px;color:#8aa;">AI-generated designs · illustration</div>
{cursor('s05c')}
'''

# ---------- S06
bars = ''.join(f'<div class="abs cb" id="cb{i}" style="left:{70+[0,40,40,80,80,40,0,40,80,40,0][i]}px;top:{130+i*46}px;width:{[300,520,380,610,450,340,260,560,400,480,220][i]}px;background:{["#e8a33d","#3fd0c9","#e0503f","#8fd3a1","#b9a2ff","#3fd0c9","#e8a33d","#8fd3a1","#e0503f","#3fd0c9","#e8a33d"][i]};"></div>' for i in range(11))
prods = ''.join(f'<div class="abs card prod" id="s06p{i+1}" style="left:{190+(i%3)*330}px;top:{280+(i//3)*340}px;width:300px;height:310px;"><img src="assets/img/ai{i+1}.jpg" alt=""/><div class="pr"><span>Design #{i+1}</span><b>${[39,29,45,35,29,49][i]}</b></div></div>' for i in range(6))
SC['s06'] = f'''
<div id="s06A">
  <div class="abs win dark" id="s06e" style="left:160px;top:140px;width:1000px;height:760px;"><div class="bar"><span class="d" style="background:#ff5f57"></span><span class="d" style="background:#febc2e"></span><span class="d" style="background:#28c840"></span><div class="url">app-builder · new project</div></div>{bars}</div>
  <div class="abs phone" id="s06ph" style="left:1360px;top:140px;width:340px;height:700px;"><div style="position:absolute;left:14px;top:14px;width:312px;height:672px;border-radius:36px;background:#14110f;overflow:hidden;">
    <div class="abs" style="left:20px;top:30px;font-size:26px;font-weight:700;color:#3fd0c9;">MaskGen</div>
    <img class="abs pv" id="pv1" src="assets/img/ai1.jpg" style="left:20px;top:90px;width:128px;height:128px;border-radius:14px;"/><img class="abs pv" id="pv2" src="assets/img/ai2.jpg" style="left:164px;top:90px;width:128px;height:128px;border-radius:14px;"/>
    <img class="abs pv" id="pv3" src="assets/img/ai3.jpg" style="left:20px;top:234px;width:128px;height:128px;border-radius:14px;"/><img class="abs pv" id="pv4" src="assets/img/ai4.jpg" style="left:164px;top:234px;width:128px;height:128px;border-radius:14px;"/>
    <img class="abs pv" id="pv5" src="assets/img/ai5.jpg" style="left:20px;top:378px;width:128px;height:128px;border-radius:14px;"/><img class="abs pv" id="pv6" src="assets/img/ai6.jpg" style="left:164px;top:378px;width:128px;height:128px;border-radius:14px;"/>
  </div></div>
  <div class="abs serif" id="s06at" style="left:160px;top:935px;font-size:44px;">The person develops an application…</div>
</div>
<div id="s06B">
  <div class="abs win" id="s06s" style="left:130px;top:100px;width:1660px;height:880px;"><div class="bar"><span class="d" style="background:#ff5f57"></span><span class="d" style="background:#febc2e"></span><span class="d" style="background:#28c840"></span><div class="url">maskgen-market.example</div></div>
    <div class="abs" style="left:40px;top:84px;font-size:40px;font-weight:800;color:#3fd0c9;">MaskGen <span style="color:#f3ead8;font-weight:500;">Market</span></div></div>
  {prods}
  <div class="abs card earn" id="s06er" style="left:1230px;top:250px;width:500px;height:300px;"><div class="eyebrow" style="position:absolute;left:36px;top:36px;">Earnings</div><div class="serif" id="s06n" style="position:absolute;left:36px;top:96px;font-size:110px;color:#8fd3a1;">$0</div><div id="s06sales" style="position:absolute;left:36px;top:230px;font-size:30px;color:#b9ad99;">0 sales</div></div>
  <div class="abs card toast" id="s06to" style="left:1230px;top:600px;width:500px;height:110px;"><span style="font-size:40px;">🛒</span><span id="s06tt" style="margin-left:20px;">New sale · $39</span></div>
  <div class="abs" style="left:1230px;top:860px;font-size:24px;color:#8a7f70;">Illustrative scenario</div>
  <div class="abs buy" id="s06b1" style="left:240px;top:490px;width:200px;height:64px;">Buy</div>
</div>
{cursor('s06c')}
'''

# ---------- S07
faint = ''.join(f'<img class="abs fq" id="fq{i+1}" src="assets/img/ai{i+1}.jpg" style="left:{[60,1500,260,1380,640,1020][i]}px;top:{[80,120,780,760,40,840][i]}px;width:{[330,360,300,330,260,260][i]}px;height:{[330,360,300,330,260,260][i]}px;border-radius:24px;opacity:0;"/>' for i in range(6))
SC['s07'] = f'''
{faint}
<div class="abs eyebrow" id="s07e" style="left:0;width:1920px;top:170px;text-align:center;font-size:34px;">But here is the important question</div>
<div class="abs serif" id="s07q1" style="left:160px;width:1600px;top:300px;text-align:center;font-size:92px;line-height:1.1;">Who <span class="hl" id="s07h1">owns the rights</span> to these AI-generated designs?</div>
<div class="abs serif" id="s07q2" style="left:160px;width:1600px;top:640px;text-align:center;font-size:78px;line-height:1.1;">…and who <span class="hl" id="s07h2">deserves recognition</span> for the cultural knowledge behind them?</div>
'''

# ---------- S08
SC['s08'] = f'''
<div class="abs panel cool" id="s08L" style="left:90px;top:130px;width:820px;height:800px;"></div>
<div class="abs serif ph2" id="s08Lt" style="left:140px;top:170px;font-size:60px;color:#7fd8d3;">The individual</div>
<div class="abs gen" id="s08Li" style="left:370px;top:290px;">{person('#3fd0c9','#0f4a4a',150)}</div>
{chip('s08a','Developed the prompts',160,560,640,'cool')}
{chip('s08b','Created the application',160,680,640,'cool')}
<div class="abs panel warm" id="s08R" style="left:1010px;top:130px;width:820px;height:800px;"></div>
<div class="abs serif ph2" id="s08Rt" style="left:1060px;top:170px;font-size:60px;color:#e8a33d;">Generations of mask makers</div>
{''.join(f'<div class="abs gen" id="s08g{i}" style="left:{1070+i*140}px;top:{300+[0,0,15,45,70][i]}px;">{person(["#e8a33d","#d9873a","#cf6f3a","#c75a3a","#c0453a"][i], "#6b2b1d", [110,110,100,90,80][i])}</div>' for i in range(5))}
<div class="abs orb" id="s08orb" style="left:0;top:0;opacity:0;"></div>
{chip('s08c','Cultural knowledge',1060,530,720,'amberc')}
{chip('s08d','Artistic techniques',1060,630,720,'amberc')}
{chip('s08e','Traditional designs',1060,730,720,'amberc')}
<div class="abs" id="s08how" style="left:910px;top:490px;width:100px;text-align:center;font-size:26px;color:#b9ad99;letter-spacing:.1em;">BUT</div>
'''

# ---------- S09
SC['s09'] = f'''
{chip('s09a','Knowledge',110,250,560,'amberc')}
{chip('s09b','Skills',110,430,560,'amberc')}
{chip('s09c','Cultural contributions',110,610,560,'amberc')}
<div class="abs line" id="s09l1" style="left:690px;top:290px;width:210px;height:3px;transform-origin:0 50%;"></div>
<div class="abs line" id="s09l2" style="left:690px;top:470px;width:210px;height:3px;transform-origin:0 50%;"></div>
<div class="abs line" id="s09l3" style="left:690px;top:650px;width:210px;height:3px;transform-origin:0 50%;"></div>
<div class="abs aibox" id="s09ai" style="left:900px;top:240px;width:420px;height:470px;"><div class="serif" style="font-size:60px;color:#7fd8d3;">AI system</div><div id="s09sub" style="font-size:34px;color:#b9ad99;margin-top:18px;text-align:center;">learns from traditional designs</div></div>
<div class="abs line" id="s09l4" style="left:1330px;top:470px;width:80px;height:3px;transform-origin:0 50%;"></div>
{''.join(f'<img class="abs card ot" id="s09o{i+1}" src="assets/img/ai{i+1}.jpg" style="left:{1430+(i%2)*190}px;top:{250+(i//2)*180}px;width:170px;height:170px;"/>' for i in range(4))}
{''.join(f'<div class="abs card dash" id="s09d{i+1}" style="left:{1430+(i%2)*190}px;top:{250+(i//2)*180}px;width:170px;height:170px;opacity:0;"></div>' for i in range(4))}
<div class="abs serif" id="s09m" style="left:0;width:1920px;top:850px;text-align:center;font-size:62px;">Not the same traditional designs to learn from</div>
'''

# ---------- S10
SC['s10'] = f'''
<div class="abs panel cool" id="s10L" style="left:90px;top:120px;width:820px;height:820px;"></div>
<div class="abs serif" id="s10Lt" style="left:140px;top:160px;font-size:56px;color:#7fd8d3;">The person using the AI</div>
<div class="abs eyebrow" id="s10l1" style="left:140px;top:300px;">Financial benefits</div>
<div class="abs serif" id="s10n1" style="left:140px;top:350px;font-size:150px;color:#8fd3a1;">$0</div>
<div class="abs eyebrow" id="s10l2" style="left:140px;top:600px;">Public recognition</div>
<div class="abs serif" id="s10n2" style="left:140px;top:650px;font-size:150px;color:#7fd8d3;">0</div>
<div class="abs" id="s10f" style="left:146px;top:820px;font-size:40px;color:#7fd8d3;">followers</div>
<div class="abs panel warm" id="s10R" style="left:1010px;top:120px;width:820px;height:820px;"></div>
<div class="abs serif" id="s10Rt" style="left:1060px;top:160px;font-size:56px;color:#e8a33d;line-height:1.1;width:740px;">Indigenous and local communities</div>
<div class="abs eyebrow" id="s10r1" style="left:1060px;top:400px;">Credit</div>
<div class="abs serif" id="s10x1" style="left:1060px;top:450px;font-size:130px;color:#8a7f70;">✕ <span style="font-size:60px;">none</span></div>
<div class="abs eyebrow" id="s10r2" style="left:1060px;top:650px;">Compensation</div>
<div class="abs serif" id="s10x2" style="left:1060px;top:700px;font-size:130px;color:#8a7f70;">✕ <span style="font-size:60px;">none</span></div>
<div class="abs" style="left:100px;top:980px;font-size:24px;color:#8a7f70;">Illustrative scenario</div>
'''

# ---------- S11
SC['s11'] = f'''
<div class="abs serif" id="s11h" style="left:0;width:1920px;top:50px;text-align:center;font-size:76px;">A legal and ethical concern</div>
<div class="abs" id="s11sh" style="left:150px;top:260px;opacity:0;">{SHIELD}</div>
<div class="abs card" id="s11m" style="left:260px;top:410px;width:300px;height:300px;"><img src="assets/img/ginijala.jpg" alt=""/></div>
<div class="abs serif" id="s11q" style="left:900px;top:215px;width:900px;font-size:50px;line-height:1.15;color:#f3ead8;">How can we protect traditional cultural expressions from…</div>
{chip('s11a','Unauthorised use',900,430,820,'red')}
{chip('s11b','Exploitation',900,550,820,'red')}
{chip('s11c','Commercialisation',900,670,820,'red')}
{chip('s11d','…through generative AI',900,820,820,'cool')}
'''

# ---------- S12
SC['s12'] = f'''
<div class="abs serif" id="s12h" style="left:130px;top:100px;font-size:86px;">The law</div>
<svg class="abs" id="s12sv" style="left:90px;top:230px;" width="900" height="760" viewBox="0 0 900 760">
  <rect x="436" y="170" width="28" height="520" fill="#8a7f70"/><rect x="300" y="690" width="300" height="26" rx="8" fill="#8a7f70"/>
  <g id="s12beam"><rect x="90" y="156" width="720" height="22" rx="11" fill="#e8a33d"/><circle cx="450" cy="167" r="22" fill="#f3ead8"/></g>
  <g id="s12pl"><line x1="120" y1="178" x2="60" y2="420" stroke="#b9ad99" stroke-width="3"/><line x1="120" y1="178" x2="240" y2="420" stroke="#b9ad99" stroke-width="3"/><path d="M40 420 H260 Q250 500 150 510 Q50 500 40 420Z" fill="#e8a33d" opacity=".9"/><text x="150" y="470" text-anchor="middle" font-size="24" font-weight="700" fill="#2b1410">Communities</text></g>
  <g id="s12pr"><line x1="780" y1="178" x2="660" y2="420" stroke="#b9ad99" stroke-width="3"/><line x1="780" y1="178" x2="840" y2="420" stroke="#b9ad99" stroke-width="3"/><path d="M640 420 H860 Q850 500 750 510 Q650 500 640 420Z" fill="#3fd0c9" opacity=".9"/><text x="750" y="470" text-anchor="middle" font-size="24" font-weight="700" fill="#06302f">Benefits</text></g>
</svg>
<div class="abs serif" id="s12c" style="left:1060px;top:240px;font-size:56px;width:760px;line-height:1.1;">Communities preserving cultural traditions</div>
{chip('s12a','Appropriate recognition',1060,470,720,'amberc')}
{chip('s12b','A fair share of the benefits',1060,600,720,'amberc')}
'''

# ---------- S13
mos = ''.join(f'<img class="abs" id="mo{i}" src="assets/img/{n}.jpg" style="left:{i*275}px;top:{[0,540,0,540,0,540,0][i]}px;width:275px;height:540px;object-fit:cover;opacity:0;"/>' for i, n in enumerate(['naga', 'bihiri', 'abuta', 'deva', 'maru', 'ginijala', 'kana']))
SC['s13'] = f'''
{mos}
<div class="abs" id="s13v" style="left:0;top:0;width:1920px;height:1080px;background:rgba(10,7,6,.78);"></div>
<div class="abs eyebrow" id="s13e" style="left:0;width:1920px;top:200px;text-align:center;font-size:34px;">My research</div>
<div class="abs serif" id="s13t1" style="left:160px;width:1600px;top:290px;text-align:center;font-size:104px;line-height:1.05;">Safeguarding Traditional Cultural Expressions</div>
<div class="abs serif" id="s13t2" style="left:160px;width:1600px;top:520px;text-align:center;font-size:84px;line-height:1.05;color:#7fd8d3;">in the Age of Generative AI</div>
<div class="abs" id="s13s" style="left:0;width:1920px;top:720px;text-align:center;font-size:46px;color:#b9ad99;">A comparative legal analysis of</div>
<div class="abs pill" id="s13p1" style="left:600px;top:800px;width:340px;">Sri Lanka</div>
<div class="abs pill" id="s13p2" style="left:980px;top:800px;width:340px;">China</div>
'''

CSS = '''
* { margin:0; padding:0; box-sizing:border-box; }
html, body { margin:0; width:1920px; height:1080px; overflow:hidden; background:#0d0a09; }
#root { position:relative; width:100%; height:100%; background:radial-gradient(ellipse at 50% 35%, #261612 0%, #0d0a09 72%); color:#f3ead8; font-family:sans-serif; overflow:hidden; }
.scene { position:absolute; inset:0; }
.wrap { position:absolute; inset:0; }
.abs { position:absolute; }
.serif { font-family:serif; font-weight:700; letter-spacing:-0.02em; }
.eyebrow { font-size:28px; letter-spacing:.2em; text-transform:uppercase; color:#b9ad99; font-weight:600; }
.card { border-radius:26px; overflow:hidden; box-shadow:0 26px 70px rgba(0,0,0,.55); }
.card img { display:block; width:100%; height:100%; object-fit:cover; }
.chip { display:flex; align-items:center; padding:0 32px; height:84px; border-radius:18px; font-size:40px; font-weight:600; border:3px solid #e8a33d; background:rgba(232,163,61,.10); }
.chip.cool { border-color:#3fd0c9; background:rgba(63,208,201,.10); }
.chip.red { border-color:#e0503f; background:rgba(224,80,63,.14); }
.tile { background:#1a1210; border:2px solid rgba(255,255,255,.12); }
.tile .tl { position:absolute; left:0; right:0; bottom:0; padding:70px 26px 24px; font-size:36px; font-weight:700; font-family:serif; background:linear-gradient(transparent, rgba(0,0,0,.8)); line-height:1.1; }
.tile .ic { position:absolute; left:0; right:0; top:60px; text-align:center; }
.tile.dashed { border:3px dashed #e8a33d; background:rgba(232,163,61,.05); box-shadow:none; }
.pinc { background:rgba(255,255,255,.05); border:2px solid rgba(232,163,61,.5); }
.glow { background:radial-gradient(circle, rgba(232,163,61,.35), rgba(232,163,61,0) 65%); }
.line { background:#e8a33d; opacity:.8; }
.lab { font-size:70px; color:#e8a33d; }
.strike { position:relative; color:#8a7f70; }
.strike::after { content:''; position:absolute; left:0; top:54%; height:6px; background:#e0503f; width:var(--sw,0%); }
.orb { width:44px; height:44px; border-radius:50%; background:radial-gradient(circle,#fff6d8,#e8a33d 60%,rgba(232,163,61,0)); box-shadow:0 0 40px 12px rgba(232,163,61,.7); }
.phone { background:#050505; border-radius:64px; border:3px solid #3a342e; box-shadow:0 40px 90px rgba(0,0,0,.65); }
.loc .lt { position:absolute; left:240px; top:60px; font-size:64px; }
.loc img { width:200px; position:absolute; left:0; top:0; height:200px; }
.loc { background:rgba(255,255,255,.06); border:2px solid rgba(255,255,255,.12); }
.win { background:#16201f; border-radius:22px; border:2px solid #2d3d3b; box-shadow:0 40px 100px rgba(0,0,0,.6); overflow:hidden; }
.win.dark { background:#14110f; border-color:#3a342e; }
.win .bar { position:absolute; left:0; top:0; right:0; height:62px; background:#0f1716; display:flex; align-items:center; padding-left:24px; }
.win.dark .bar { background:#0f0c0a; }
.win .d { width:16px; height:16px; border-radius:50%; margin-right:10px; display:inline-block; }
.win .url { margin-left:30px; background:#1f2c2b; border-radius:10px; padding:8px 24px; font-size:22px; color:#9fb; }
.drop { border:3px dashed #3fd0c9; border-radius:22px; background:rgba(63,208,201,.06); display:flex; align-items:center; justify-content:center; font-size:30px; color:#7fd8d3; }
.up { border:3px solid #3fd0c9; }
.up .ck { position:absolute; right:8px; top:8px; width:38px; height:38px; border-radius:50%; background:#3fd0c9; color:#06302f; font-weight:800; font-size:26px; display:flex; align-items:center; justify-content:center; }
.prompt { background:#0f1716; border:2px solid #2d4a47; border-radius:18px; padding:22px 26px; font-size:34px; line-height:1.3; color:#e6fffd; }
.caret { color:#3fd0c9; }
.gbtn { background:linear-gradient(90deg,#2fb8b0,#3fd0c9); color:#06302f; font-size:38px; font-weight:800; border-radius:18px; display:flex; align-items:center; justify-content:center; }
.cursor { width:46px; height:46px; }
.ripple { position:absolute; left:-18px; top:-18px; width:60px; height:60px; border-radius:50%; border:4px solid #fff; opacity:0; }
.cb { height:22px; border-radius:11px; opacity:0; }
.prod { background:#1a1210; border:2px solid rgba(255,255,255,.1); }
.prod .pr { position:absolute; left:0; right:0; bottom:0; height:64px; background:rgba(0,0,0,.72); display:flex; justify-content:space-between; align-items:center; padding:0 20px; font-size:26px; }
.prod .pr b { color:#8fd3a1; font-size:32px; }
.earn { background:#16201f; border:2px solid #2d4a47; }
.toast { background:#1b2b1f; border:2px solid #3b7a4a; display:flex; align-items:center; padding-left:30px; font-size:36px; font-weight:700; }
.buy { background:#3fd0c9; color:#06302f; border-radius:14px; font-size:34px; font-weight:800; display:flex; align-items:center; justify-content:center; opacity:0; }
.hl { color:#e8a33d; }
.panel { border-radius:34px; }
.panel.cool { background:rgba(63,208,201,.06); border:3px solid rgba(63,208,201,.5); }
.panel.warm { background:rgba(232,163,61,.06); border:3px solid rgba(232,163,61,.5); }
.aibox { border:3px solid #3fd0c9; border-radius:30px; background:rgba(63,208,201,.08); display:flex; flex-direction:column; align-items:center; justify-content:center; }
.dash { border:3px dashed #6b5d4d; background:rgba(255,255,255,.03); box-shadow:none; }
.pill { height:96px; border-radius:48px; border:3px solid #e8a33d; display:flex; align-items:center; justify-content:center; font-size:48px; font-weight:700; font-family:serif; background:rgba(232,163,61,.12); }
'''

# ---------- JS
JS = r'''
const ST = %%ST%%; const DUR = %%DUR%%; const VO = %%VO%%;
const tl = gsap.timeline({ paused: true });
const EO = "power3.out";
const T = (k, t) => ST[k] + t;
const I = (sel, k, t, o = {}) => tl.fromTo(sel, { opacity: 0, y: o.y ?? 24, x: o.x ?? 0, scale: o.s ?? 1 }, { opacity: 1, y: 0, x: 0, scale: 1, duration: o.d ?? 0.5, ease: o.e ?? EO }, T(k, t));
const O = (sel, k, t, d = 0.4) => tl.to(sel, { opacity: 0, duration: d, ease: "power1.in" }, T(k, t));
const typeText = (sel, text, k, t, d) => { const o = { p: 0 }; tl.to(o, { p: 1, duration: d, ease: "none", onUpdate: () => { document.querySelector(sel).textContent = text.slice(0, Math.round(o.p * text.length)); } }, T(k, t)); };
const count = (sel, to, k, t, d, fmt) => { const o = { v: 0 }; tl.to(o, { v: to, duration: d, ease: "power2.out", onUpdate: () => { document.querySelector(sel).textContent = fmt(o.v); } }, T(k, t)); };
const cur = (id, k, t, x, y, d = 0.7, first = null) => { if (first) tl.fromTo(id, { x: first[0], y: first[1], opacity: 0 }, { x, y, opacity: 1, duration: d, ease: "power2.inOut" }, T(k, t)); else tl.to(id, { x, y, duration: d, ease: "power2.inOut" }, T(k, t)); };
const click = (id, k, t) => { tl.to(id, { scale: 0.88, duration: 0.08, yoyo: true, repeat: 1 }, T(k, t)); tl.fromTo(id + "-r", { scale: 0.3, opacity: 0.8 }, { scale: 1.4, opacity: 0, duration: 0.5, ease: "power1.out" }, T(k, t)); };

// scene fades
Object.keys(ST).forEach((k) => { tl.fromTo("#" + k + "w", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "none" }, ST[k]); tl.to("#" + k + "w", { opacity: 0, duration: 0.3, ease: "none" }, ST[k] + DUR[k] - 0.3); });

// ===== S01 — generations & kinds of tradition
I("#s01t", "s01", 0.3, { d: 0.7 });
for (let i = 0; i < 5; i++) I("#g" + i, "s01", 0.9 + i * 0.35, { y: 40, s: 0.85 });
const gx = [170, 515, 860, 1205, 1550].map((x, i) => x + [75, 75, 70, 60, 50][i] - 22);
const gy = [300, 300, 315, 345, 380];
tl.fromTo("#s01orb", { x: gx[0], y: gy[0], opacity: 0 }, { opacity: 1, duration: 0.4 }, T("s01", 2.6));
for (let i = 1; i < 5; i++) tl.to("#s01orb", { x: gx[i], y: gy[i], duration: 1.1, ease: "power1.inOut" }, T("s01", 3.0 + (i - 1) * 1.55));
I("#s01a", "s01", 3.6, { y: 20 }); I("#s01b", "s01", 5.2, { y: 20 }); I("#s01c", "s01", 6.2, { y: 20 });
tl.to("#s01orb", { opacity: 0, duration: 0.5 }, T("s01", 9.3));
I("#s01m", "s01", 10.4, { y: 50 }); I("#s01f", "s01", 12.5, { y: 50 }); I("#s01h", "s01", 13.7, { y: 50 }); I("#s01x", "s01", 15.4, { y: 50 });

// ===== S02 — Ambalangoda
I("#s02e", "s02", 0.3);
I("#s02p", "s02", 1.5, { x: -50, d: 0.8 });
I("#s02i1", "s02", 0.8, { y: 60, d: 0.9 }); I("#s02i2", "s02", 1.4, { y: 60, d: 0.9 }); I("#s02i3", "s02", 2.0, { y: 60, d: 0.9 });
tl.fromTo("#s02i1", { rotation: -5 }, { rotation: -3, duration: 12, ease: "none" }, T("s02", 0.8));
tl.fromTo("#s02i2", { rotation: 4 }, { rotation: 2, duration: 12, ease: "none" }, T("s02", 1.4));
tl.fromTo("#s02i3", { rotation: -2 }, { rotation: -4, duration: 12, ease: "none" }, T("s02", 2.0));
I("#s02h", "s02", 6.2);
I("#s02a", "s02", 9.6, { x: -40 }); I("#s02b", "s02", 11.5, { x: -40 }); I("#s02c", "s02", 12.4, { x: -40 });

// ===== S03 — more than art
I("#s03h", "s03", 0.2, { d: 0.7 });
tl.to("#s03s", { "--sw": "100%", duration: 0.5, ease: "power2.out" }, T("s03", 2.5));
I("#s03g", "s03", 2.7, { s: 0.8, d: 1.0 }); I("#s03m", "s03", 2.7, { s: 0.92, d: 0.8 });
[["#s03l1", "#s03w1", 3.5], ["#s03l2", "#s03w2", 4.85], ["#s03l3", "#s03w3", 5.7], ["#s03l4", "#s03w4", 6.45]].forEach(([l, w, t]) => {
  tl.fromTo(l, { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 0.8, duration: 0.35, ease: EO }, T("s03", t));
  I(w, "s03", t + 0.1, { y: 14, d: 0.45 });
});
I("#s03f", "s03", 7.5);
tl.fromTo("#s03m", { scale: 1 }, { scale: 1.05, duration: 6.5, ease: "none" }, T("s03", 2.9));

// ===== S04 — the visitor photographs
I("#s04h", "s04", 0.5, { d: 0.7 });
I("#s04ph", "s04", 0.9, { y: 120, d: 0.9 });
tl.fromTo("#s04v1", { opacity: 0 }, { opacity: 1, duration: 0.5 }, T("s04", 3.1));
tl.fromTo("#s04fb", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.5, ease: EO }, T("s04", 4.0));
const shot = (n, t, card) => {
  tl.fromTo("#s04fl", { opacity: 0 }, { opacity: 0.95, duration: 0.07, yoyo: true, repeat: 1 }, T("s04", t));
  tl.fromTo("#s04sh", { scale: 1 }, { scale: 0.86, duration: 0.08, yoyo: true, repeat: 1 }, T("s04", t));
  I(card, "s04", t + 0.25, { x: 60 });
};
shot(1, 6.0, "#s04c1");
tl.to("#s04v1", { opacity: 0, duration: 0.01 }, T("s04", 7.0)); tl.fromTo("#s04v2", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T("s04", 7.0));
shot(2, 7.7, "#s04c2");
tl.to("#s04v2", { opacity: 0, duration: 0.01 }, T("s04", 8.4)); tl.fromTo("#s04v3", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T("s04", 8.4));
shot(3, 9.0, "#s04c3");

// ===== S05 — uploads to generative AI
I("#s05w0", "s05", 0.2, { y: 40, d: 0.7 });
tl.fromTo("#s05d", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T("s05", 0.9));
[["#s05t1", 1.9], ["#s05t2", 2.6], ["#s05t3", 3.3]].forEach(([s, t]) => tl.fromTo(s, { opacity: 0, x: -400, y: 260, scale: 1.4 }, { opacity: 1, x: 0, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, T("s05", t)));
tl.to("#s05dt", { opacity: 0, duration: 0.3 }, T("s05", 1.7));
tl.fromTo("#s05p", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T("s05", 4.3));
typeText("#s05pt", "Generate new traditional mask designs", "s05", 4.8, 1.5);
I("#s05g", "s05", 4.5, { y: 14 });
cur("#s05c", "s05", 5.2, 440, 800, 0.8, [1100, 400]);
click("#s05c", "s05", 6.2);
tl.fromTo("#s05pf", { width: 0 }, { width: 600, duration: 0.9, ease: "power1.inOut" }, T("s05", 6.3));
for (let i = 1; i <= 6; i++) tl.fromTo("#s05r" + i, { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, T("s05", 7.1 + (i - 1) * 0.18));
I("#s05cap", "s05", 8.0);
tl.to("#s05c", { opacity: 0, duration: 0.3 }, T("s05", 6.9));

// ===== S06 — app and sales
I("#s06e", "s06", 0.2, { y: 40, d: 0.7 }); I("#s06ph", "s06", 0.6, { y: 60, d: 0.8 }); I("#s06at", "s06", 0.4);
for (let i = 0; i < 11; i++) tl.fromTo("#cb" + i, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: EO }, T("s06", 0.8 + i * 0.27));
for (let i = 1; i <= 6; i++) tl.fromTo("#pv" + i, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3 }, T("s06", 1.4 + i * 0.35));
tl.to("#s06A", { opacity: 0, duration: 0.35 }, T("s06", 3.95));
tl.fromTo("#s06B", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T("s06", 4.0));
for (let i = 1; i <= 6; i++) tl.fromTo("#s06p" + i, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: EO }, T("s06", 4.3 + i * 0.12));
I("#s06er", "s06", 5.0);
tl.fromTo("#s06b1", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T("s06", 5.1));
cur("#s06c", "s06", 5.2, 330, 520, 0.7, [900, 800]);
click("#s06c", "s06", 6.0);
tl.fromTo("#s06to", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: EO }, T("s06", 6.1));
tl.to("#s06b1", { opacity: 0, duration: 0.2 }, T("s06", 6.2));
count("#s06n", 2450, "s06", 6.1, 2.0, v => "$" + Math.round(v).toLocaleString("en-US"));
count("#s06sales", 63, "s06", 6.1, 2.0, v => Math.round(v) + " sales");
tl.to("#s06to", { opacity: 0, duration: 0.4 }, T("s06", 7.6));
tl.to("#s06c", { opacity: 0, duration: 0.3 }, T("s06", 6.8));

// ===== S07 — the question
for (let i = 1; i <= 6; i++) tl.fromTo("#fq" + i, { opacity: 0 }, { opacity: 0.09, duration: 1.0 }, T("s07", 0.2 + i * 0.15));
typeText("#s07e", "But here is the important question", "s07", 0.1, 1.7);
tl.fromTo("#s07e", { opacity: 0 }, { opacity: 1, duration: 0.2 }, T("s07", 0.05));
I("#s07q1", "s07", 2.45, { y: 30, d: 0.7 });
tl.fromTo("#s07h1", { color: "#f3ead8" }, { color: "#e8a33d", duration: 0.4 }, T("s07", 3.2));
I("#s07q2", "s07", 5.95, { y: 30, d: 0.7 });
tl.fromTo("#s07h2", { color: "#f3ead8" }, { color: "#e8a33d", duration: 0.4 }, T("s07", 6.8));

// ===== S08 — individual vs generations
I("#s08L", "s08", 0.1, { x: -40 }); I("#s08Lt", "s08", 0.3); I("#s08Li", "s08", 0.8, { s: 0.85 });
I("#s08a", "s08", 3.9, { x: -40 }); I("#s08b", "s08", 5.7, { x: -40 });
I("#s08how", "s08", 7.6, { y: 10 }); tl.to("#s08how", { opacity: 0, duration: 0.5 }, T("s08", 9.2));
I("#s08R", "s08", 6.9, { x: 40 }); I("#s08Rt", "s08", 7.1);
for (let i = 0; i < 5; i++) I("#s08g" + i, "s08", 7.6 + i * 0.25, { y: 30, s: 0.85 });
I("#s08c", "s08", 8.2, { x: 40 }); I("#s08d", "s08", 9.5, { x: 40 }); I("#s08e", "s08", 10.7, { x: 40 });
const hx = [1070, 1210, 1350, 1490, 1630].map(x => x + 40), hy = [320, 320, 335, 365, 385];
tl.fromTo("#s08orb", { x: hx[0], y: hy[0], opacity: 0 }, { opacity: 1, duration: 0.3 }, T("s08", 12.6));
for (let i = 1; i < 5; i++) tl.to("#s08orb", { x: hx[i], y: hy[i], duration: 0.8, ease: "power1.inOut" }, T("s08", 12.9 + (i - 1) * 0.9));

// ===== S09 — without them, nothing to learn from
[["#s09a", 0.2], ["#s09b", 0.5], ["#s09c", 0.8]].forEach(([s, t]) => I(s, "s09", t - 0.15, { x: -40 }));
["#s09l1", "#s09l2", "#s09l3", "#s09l4"].forEach((l, i) => tl.fromTo(l, { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 0.8, duration: 0.4, ease: EO }, T("s09", 0.5 + i * 0.12)));
I("#s09ai", "s09", 0.4, { s: 0.9 });
for (let i = 1; i <= 4; i++) I("#s09o" + i, "s09", 0.7 + i * 0.1, { s: 0.8 });
// removal, in step with the narration: knowledge, skills, cultural contributions
[["#s09a", "#s09l1", 1.0], ["#s09b", "#s09l2", 1.9], ["#s09c", "#s09l3", 3.5]].forEach(([c, l, t]) => { tl.to(c, { opacity: 0.12, x: -30, duration: 0.5 }, T("s09", t)); tl.to(l, { opacity: 0, duration: 0.4 }, T("s09", t)); });
tl.to("#s09ai", { opacity: 0.45, duration: 0.6 }, T("s09", 4.1));
tl.to("#s09sub", { opacity: 0, duration: 0.3 }, T("s09", 4.1));
for (let i = 1; i <= 4; i++) { tl.to("#s09o" + i, { opacity: 0, duration: 0.5 }, T("s09", 4.2 + i * 0.1)); tl.to("#s09d" + i, { opacity: 1, duration: 0.5 }, T("s09", 4.2 + i * 0.1)); }
I("#s09m", "s09", 5.0, { y: 20 });

// ===== S10 — who benefits
I("#s10L", "s10", 0.0, { x: -40 }); I("#s10Lt", "s10", 0.3);
I("#s10l1", "s10", 1.9); I("#s10n1", "s10", 2.0);
count("#s10n1", 4820, "s10", 2.1, 2.0, v => "$" + Math.round(v).toLocaleString("en-US"));
I("#s10l2", "s10", 4.2); I("#s10n2", "s10", 4.3); I("#s10f", "s10", 4.4);
count("#s10n2", 12400, "s10", 4.3, 1.4, v => Math.round(v).toLocaleString("en-US"));
I("#s10R", "s10", 6.0, { x: 40 }); I("#s10Rt", "s10", 6.2, { d: 0.7 });
I("#s10r1", "s10", 11.7); I("#s10x1", "s10", 11.9, { s: 0.7, e: "back.out(2)" });
I("#s10r2", "s10", 13.2); I("#s10x2", "s10", 13.4, { s: 0.7, e: "back.out(2)" });

// ===== S11 — legal and ethical concern
I("#s11h", "s11", 0.3, { d: 0.7 });
tl.fromTo("#s11sh", { opacity: 0, scale: 0.85, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.8, ease: EO }, T("s11", 1.0));
I("#s11m", "s11", 1.4, { s: 0.9 });
I("#s11q", "s11", 3.9, { y: 20, d: 0.7 });
I("#s11a", "s11", 6.6, { x: 60, e: "power3.out" }); I("#s11b", "s11", 8.3, { x: 60 }); I("#s11c", "s11", 9.5, { x: 60 });
I("#s11d", "s11", 11.0, { y: 20 });
[6.9, 8.6, 9.8].forEach(t => tl.fromTo("#s11sh", { scale: 1 }, { scale: 1.04, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, T("s11", t)));

// ===== S12 — what the law should ensure
I("#s12h", "s12", 1.3, { d: 0.7 });
I("#s12sv", "s12", 1.8, { y: 30, d: 0.8 });
tl.fromTo("#s12beam", { rotation: 12, svgOrigin: "450 167" }, { rotation: 12, svgOrigin: "450 167", duration: 0.01 }, T("s12", 0));
tl.fromTo("#s12pl", { y: -68 }, { y: -68, duration: 0.01 }, T("s12", 0)); tl.fromTo("#s12pr", { y: 68 }, { y: 68, duration: 0.01 }, T("s12", 0));
I("#s12c", "s12", 3.0, { x: 40 });
I("#s12a", "s12", 6.7, { x: 40 }); I("#s12b", "s12", 8.9, { x: 40 });
tl.to("#s12beam", { rotation: 0, svgOrigin: "450 167", duration: 1.8, ease: "power2.inOut" }, T("s12", 9.0));
tl.to("#s12pl", { y: 0, duration: 1.8, ease: "power2.inOut" }, T("s12", 9.0)); tl.to("#s12pr", { y: 0, duration: 1.8, ease: "power2.inOut" }, T("s12", 9.0));

// ===== S13 — the research
for (let i = 0; i < 7; i++) tl.fromTo("#mo" + i, { opacity: 0 }, { opacity: 0.55, duration: 1.0 }, T("s13", 0.1 + i * 0.12));
I("#s13e", "s13", 0.5);
I("#s13t1", "s13", 3.4, { y: 40, d: 0.9, e: "expo.out" });
I("#s13t2", "s13", 7.4, { y: 40, d: 0.8 });
I("#s13s", "s13", 9.8);
I("#s13p1", "s13", 11.8, { s: 0.85 }); I("#s13p2", "s13", 12.5, { s: 0.85 });

window.__timelines["main"] = tl;
tl.seek(0);
'''

audio = []
n = 0
def aud(id_, src, start, dur, vol, extra=''):
    global n
    n += 1
    audio.append(f'<audio id="{id_}" src="{src}" data-start="{start}" data-duration="{dur}" data-track-index="{n+2}" data-volume="{vol}" {extra}></audio>')
aud('music', 'assets/music/bed.mp3', 0, TOTAL, 0.16, 'data-fade-in="1.5" data-fade-out="3"')
for k in keys:
    aud('vo-' + k, f'assets/vo/{k}.wav', round(ST[k] + 0.05, 3), vo[k], 1)
def sfx(id_, f, k, t, vol, d):
    aud(id_, f'assets/sfx/{f}.ogg', round(ST[k] + t, 3), d, vol)
for i, t in enumerate([6.0, 7.7, 9.0]): sfx(f'sx-shot{i}', 'click', 's04', t, 0.6, 0.06)
sfx('sx-gen', 'click', 's05', 6.2, 0.6, 0.06); sfx('sx-buy', 'click', 's06', 6.0, 0.6, 0.06); sfx('sx-sale', 'bong', 's06', 6.1, 0.5, 0.12)
sfx('sx-q1', 'bong', 's07', 2.45, 0.5, 0.12); sfx('sx-q2', 'bong', 's07', 5.95, 0.5, 0.12)
sfx('sx-title', 'hit', 's13', 3.4, 0.45, 0.54)

scenes = ''
for k in keys:
    scenes += f'<div id="{k}" class="scene clip" data-start="{ST[k]}" data-duration="{DUR[k]}" data-track-index="0"><div class="wrap" id="{k}w">{SC[k]}</div></div>\n'

js = JS.replace('%%ST%%', json.dumps(ST)).replace('%%DUR%%', json.dumps(DUR)).replace('%%VO%%', json.dumps(vo))
html = f'''<!doctype html>
<html lang="en" data-resolution="landscape">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
<script src="assets/vendor/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{scenes}
{chr(10).join(audio)}
</div>
<script>{js}</script>
</body></html>'''
open('index.html', 'w').write(html)
print('total', TOTAL, ST)
