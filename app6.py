 #!/usr/bin/env python3
"""
This script writes the embedded HTML UI to a temporary file and opens it
in the default web browser so you can view the dashboard locally.
"""
import tempfile
import webbrowser
from pathlib import Path

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Water Quality Analysis Dashboard</title>
    <style>
        :root{
            --bg1:#001428; /* deep navy */
            --bg2:#001f4d; /* darker blue */
            --neon:#00e6ff; /* neon cyan */
            --glass: rgba(255,255,255,0.04);
        }
        html,body{height:100%;margin:0;font-family:Arial, Helvetica, sans-serif;color:#e6f7ff}
        body{
            background: radial-gradient(1200px 600px at 10% 10%, rgba(0,230,255,0.03), transparent),
                                    linear-gradient(180deg,var(--bg1),var(--bg2));
            display:flex;align-items:center;justify-content:center;padding:40px;
            overflow:auto;
        }
        .wave { position:fixed;inset:0;z-index:0;pointer-events:none;opacity:0.18;background: repeating-linear-gradient(90deg, rgba(0,230,255,0.02) 0 6px, transparent 6px 12px); mix-blend-mode:screen; animation:flow 10s linear infinite }
        .wave-svg{position:fixed;left:0;right:0;bottom:0;height:36vh;pointer-events:none;z-index:0;opacity:0.75}
        .wave-svg svg{width:200%;height:100%;display:block}
        .wave1{fill:rgba(0,230,255,0.10);transform:translate3d(0,0,0);animation:moveWave 8s linear infinite}
        .wave2{fill:rgba(0,180,255,0.08);transform:translate3d(0,0,0);animation:moveWave 12s linear infinite reverse}
        .wave3{fill:rgba(0,120,255,0.06);transform:translate3d(0,0,0);animation:moveWave 18s linear infinite}
        @keyframes moveWave{from{transform:translateX(0)}to{transform:translateX(-25%)}}
        @keyframes flow{from{background-position:0 0}to{background-position:1000px 0}}

        .card{position:relative;z-index:1;max-width:940px;width:100%;background:linear-gradient(180deg,rgba(255,255,255,0.02),rgba(255,255,255,0.01));border-radius:14px;padding:28px;border:1px solid rgba(0,230,255,0.12);box-shadow:0 8px 40px rgba(0,0,0,0.6)}
        .title-board{background:linear-gradient(90deg, rgba(0,230,255,0.06), rgba(0,120,255,0.03));padding:18px;border-radius:8px;border:1px solid rgba(0,230,255,0.12);display:flex;align-items:center;justify-content:center}
        .title-board h1{margin:0;font-size:28px;color:var(--neon);font-weight:800;letter-spacing:1px;text-transform:uppercase}
        .subtitle{margin-top:18px;font-size:13px;text-align:center;color:#cfeeff;text-transform:uppercase;letter-spacing:0.6px}
        .controls{display:flex;gap:18px;margin-top:20px;justify-content:space-between}
        .control{flex:1;background:var(--glass);padding:14px;border-radius:10px;border:1px solid rgba(0,0,0,0.2);display:flex;flex-direction:column;align-items:center}
        .label{font-size:12px;color:#bfeeff;margin-bottom:8px;text-align:center}
        .value-row{display:flex;align-items:center;gap:8px}
        .btn{background:transparent;border:1px solid rgba(0,230,255,0.12);color:var(--neon);width:36px;height:36px;border-radius:8px;font-size:18px;cursor:pointer}
        .num{width:110px;padding:8px 12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);background:rgba(0,0,0,0.12);color:#eaffff;text-align:center;font-size:18px}
        .hint{font-size:12px;color:#99ddff;margin-top:8px}
        .actions{display:flex;gap:12px;align-items:center;justify-content:center;margin-top:20px}
        .primary{background:linear-gradient(90deg,var(--neon),#4dd6ff);border:none;color:#042;cursor:pointer;padding:12px 18px;border-radius:10px;font-weight:700}
        .result{margin-top:20px;padding:14px;border-radius:10px;background:rgba(0,0,0,0.12);display:flex;justify-content:space-between;align-items:center}
        .status{font-weight:800;color:var(--neon);font-size:16px}
        .confidence{font-size:14px;color:#bfefff}
        footer.small{margin-top:12px;text-align:center;color:#9fdfff;font-size:12px}
        @media(max-width:760px){.controls{flex-direction:column}.num{width:100%}}
    </style>
</head>
<body>
    <div class="wave" aria-hidden="true"></div>
    <div class="wave-svg" aria-hidden="true">
        <svg viewBox="0 0 1200 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
            <path class="wave1" d="M0,120 C150,200 350,40 600,100 C850,160 1050,40 1200,90 L1200,200 L0,200 Z"></path>
            <path class="wave2" d="M0,140 C180,80 360,200 600,150 C840,100 1020,220 1200,140 L1200,200 L0,200 Z"></path>
            <path class="wave3" d="M0,160 C160,120 420,20 600,140 C780,260 1040,80 1200,160 L1200,200 L0,200 Z"></path>
        </svg>
    </div>

    <section id="landing" style="min-height:100vh;display:flex;align-items:center;justify-content:center;z-index:2;">
        <div style="text-align:center;max-width:900px;padding:40px;border-radius:14px;">
            <div style="background:linear-gradient(90deg, rgba(0,230,255,0.04), rgba(0,120,255,0.02));padding:28px;border-radius:12px;border:1px solid rgba(0,230,255,0.12);">
                <img id="landingLogo" src="IMG-20260216-WA0013.jpg" alt="AQUA SIGHT logo" style="width:180px;height:auto;display:block;margin:0 auto 12px auto;border-radius:8px;object-fit:cover;"/>
                <h1 style="margin:0;font-size:56px;letter-spacing:6px;color:var(--neon);text-transform:uppercase;font-weight:900;">AQUA SIGHT AI</h1>
                <p style="margin:14px 0 0;color:#cfeeff;font-size:16px;letter-spacing:1px;text-transform:uppercase">Water Quality Analysis Dashboard</p>
                <p style="color:#9fdfff;margin-top:10px;">Detect water quality using local sensor inputs and AI predictions.</p>
                <div style="margin-top:20px;">
                    <button onclick="startApp()" style="background:linear-gradient(90deg,var(--neon),#4dd6ff);border:none;color:#042;cursor:pointer;padding:14px 22px;border-radius:12px;font-weight:800;font-size:16px">Get Started</button>
                </div>
            </div>
        </div>
    </section>

    <main class="card" id="dashboard" style="display:none;">
        <div class="title-board">
            <h1>Water Quality Analysis Dashboard</h1>
        </div>

        <div class="subtitle">ENTER THE PARAMETERS RECORDED BY YOUR LOCAL SENSORS BELOW</div>

        <section class="controls" aria-label="sensor inputs">
            <div class="control" id="ph-card">
                <div class="label">pH Level</div>
                <div class="value-row">
                    <button class="btn" aria-label="decrease pH" onclick="adjust('ph', -0.1)">−</button>
                    <input id="ph" class="num" type="number" step="0.1" value="7.0" aria-label="pH value"/>
                    <button class="btn" aria-label="increase pH" onclick="adjust('ph', 0.1)">+</button>
                </div>
                <div class="hint">Decimal precision (1 place)</div>
            </div>

            <div class="control" id="turbidity-card">
                <div class="label">Turbidity (NTU)</div>
                <div class="value-row">
                    <button class="btn" aria-label="decrease turbidity" onclick="adjust('turbidity', -0.1)">−</button>
                    <input id="turbidity" class="num" type="number" step="0.1" value="5.0" aria-label="turbidity value"/>
                    <button class="btn" aria-label="increase turbidity" onclick="adjust('turbidity', 0.1)">+</button>
                </div>
                <div class="hint">Lower is generally better</div>
            </div>

            <div class="control" id="temp-card">
                <div class="label">Temperature (°C)</div>
                <div class="value-row">
                    <button class="btn" aria-label="decrease temperature" onclick="adjust('temp', -0.1)">−</button>
                    <input id="temp" class="num" type="number" step="0.1" value="25.0" aria-label="temperature value"/>
                    <button class="btn" aria-label="increase temperature" onclick="adjust('temp', 0.1)">+</button>
                </div>
                <div class="hint">Sensor reading in Celsius</div>
            </div>
        </section>

        <div class="actions">
            <button class="primary" id="runBtn" onclick="runPrediction()">Run AI Prediction</button>
            <div style="color:#9feeff;font-size:13px">Model: WaterSense v1 (simulated)</div>
        </div>

        <div class="result" aria-live="polite">
            <div>
                <div style="font-size:12px;color:#bfefff">STATUS:</div>
                <div class="status" id="status">—</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:12px;color:#bfefff">Model Confidence</div>
                <div class="confidence" id="confidence">—</div>
            </div>
        </div>

        <footer class="small">Tip: adjust values using the buttons or type directly.</footer>
    </main>

    <script>
        function startApp(){
            document.getElementById('landing').style.display = 'none';
            const dash = document.getElementById('dashboard');
            dash.style.display = 'block';
            window.scrollTo(0,0);
        }

        function clamp(v,min,max){return Math.min(max,Math.max(min,v))}
        function to1(v){return Math.round(v*10)/10}
        function adjust(id,delta){
            const el=document.getElementById(id);
            let val=parseFloat(el.value||0);
            val = to1(val + delta);
            if(id==='ph') val = clamp(val,0,14);
            if(id==='turbidity') val = Math.max(0,to1(val));
            if(id==='temp') val = to1(val);
            el.value = val.toFixed(1);
        }

        function runPrediction(){
            const ph = parseFloat(document.getElementById('ph').value)||0;
            const turb = parseFloat(document.getElementById('turbidity').value)||0;
            const temp = parseFloat(document.getElementById('temp').value)||0;

            let phScore = 0;
            if(ph>=6.5 && ph<=8.5) phScore=1;
            else phScore = Math.max(0,1 - Math.abs(ph - (ph<6.5?6.5:8.5))/4);

            let turbScore = clamp(1 - (turb/100), 0, 1);

            let tempDist = 0;
            if(temp>=20 && temp<=25) tempDist = 0;
            else tempDist = Math.min(10, Math.abs(temp - (temp<20?20:25)));
            let tempScore = clamp(1 - (tempDist/10), 0, 1);

            const overall = (phScore + turbScore + tempScore)/3;

            let status = 'Poor';
            if(overall >= 0.75) status = 'Good';
            else if(overall >= 0.5) status = 'Moderate';

            const confidence = Math.round(clamp(overall * 100 + (Math.random()*8-4), 0, 100));

            document.getElementById('status').textContent = status;
            document.getElementById('confidence').textContent = confidence + '%';

            const statusEl = document.getElementById('status');
            if(status==='Good') statusEl.style.color = '#7CFC00';
            else if(status==='Moderate') statusEl.style.color = '#FFD700';
            else statusEl.style.color = ' #FF6B6B';
        }
    </script>
</body>
</html>
'''

def main():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    tmp.write(HTML.encode('utf-8'))
    tmp.flush()
    tmp.close()
    uri = Path(tmp.name).as_uri()
    print('Opening dashboard at', uri)
    webbrowser.open(uri)

if __name__ == '__main__':
    main()
