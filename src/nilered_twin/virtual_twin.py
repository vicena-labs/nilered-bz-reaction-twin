"""Shareable, browser-based visualization for the abstract BZ twin.

The renderer turns the normalized 1-D reaction-diffusion field into an animated
vessel cross-section and a synchronized model trace. It deliberately does not
claim that the rendered colors are measured concentrations or calibrated video
pixels.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import numpy as np

DEFAULT_SOURCE_VIDEO = "https://www.youtube.com/watch?v=LL3kVtc-4vY"


def build_virtual_twin_data(
    well_mixed: dict[str, Any],
    spatial: dict[str, Any],
    *,
    n_frames: int = 121,
    source_video_url: str = DEFAULT_SOURCE_VIDEO,
) -> dict[str, Any]:
    """Create compact JSON-ready data for the interactive visual twin."""
    if n_frames < 2:
        raise ValueError("n_frames must be at least 2")
    times = np.asarray(spatial["time"], dtype=float)
    positions = np.asarray(spatial["position"], dtype=float)
    field = np.asarray(spatial["state"], dtype=float)[0]
    if field.shape != (positions.size, times.size):
        raise ValueError("spatial x-field must have shape (n_positions, n_times)")
    frame_indices = np.unique(np.linspace(0, times.size - 1, n_frames).round().astype(int))
    well_time = np.asarray(well_mixed["time"], dtype=float)
    well_signal = np.asarray(well_mixed["state"], dtype=float)[0]
    field_min = float(min(field.min(), well_signal.min()))
    field_max = float(max(field.max(), well_signal.max()))
    scale = field_max - field_min
    if scale <= 0:
        raise ValueError("spatial x-field must vary for visualization")
    field_norm = (field - field_min) / scale
    center_index = positions.size // 2
    center_signal = field[center_index]
    center_norm = (center_signal - field_min) / scale
    well_signal_norm = (well_signal - field_min) / scale
    return {
        "schema_version": "0.2.0",
        "title": "NileRed BZ Virtual Twin",
        "source_video_url": source_video_url,
        "calibration_status": "not_calibrated_to_source_video",
        "units": {
            "time": "dimensionless model time",
            "position": "dimensionless 1-D model position",
            "signal": "normalized abstract x proxy",
        },
        "times": np.round(times[frame_indices], 6).tolist(),
        "positions": np.round(positions, 6).tolist(),
        "field": np.round(field_norm[:, frame_indices].T, 6).tolist(),
        "center_signal": np.round(center_norm[frame_indices], 6).tolist(),
        "well_mixed_time": np.round(well_time[:: max(1, well_time.size // 1200)], 6).tolist(),
        "well_mixed_signal": np.round(well_signal_norm[:: max(1, well_signal_norm.size // 1200)], 6).tolist(),
        "metrics": {
            "well_mixed_peak_count": int(well_mixed["peak_count"]),
            "well_mixed_mean_period": float(well_mixed["mean_period"]),
            "well_mixed_period_std": float(well_mixed["period_std"]),
            "spatial_solver_success": bool(spatial["solver_success"]),
            "spatial_max_std": float(spatial["max_spatial_std"]),
            "spatial_final_std": float(spatial["final_spatial_std"]),
        },
    }


_HTML_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NileRed BZ Virtual Twin</title>
<style>
:root { color-scheme: dark; --bg:#0b1020; --panel:#121a2e; --line:#283653; --text:#eaf0ff; --muted:#aab7d4; --accent:#64d8cb; }
* { box-sizing:border-box; }
body { margin:0; padding:24px; background:radial-gradient(circle at 20% 0%,#182548 0,#0b1020 45%); color:var(--text); font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif; }
main { max-width:1320px; margin:auto; }
h1 { margin:.2rem 0 .3rem; font-size:clamp(1.6rem,3vw,2.5rem); }
h2 { font-size:1rem; margin:.2rem 0 .8rem; }
p { color:var(--muted); }
a { color:var(--accent); }
.badge { display:inline-block; border:1px solid #8d6b33; background:#2b2110; color:#ffd98d; border-radius:999px; padding:4px 10px; font-size:.78rem; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:18px; }
.panel { background:rgba(18,26,46,.92); border:1px solid var(--line); border-radius:16px; padding:16px; box-shadow:0 12px 40px #0003; }
canvas { width:100%; height:auto; display:block; background:#0a0e19; border-radius:10px; border:1px solid #25314d; }
.controls { display:flex; flex-wrap:wrap; align-items:center; gap:10px; margin-top:12px; }
button, select { color:var(--text); background:#1b2947; border:1px solid #3c527d; border-radius:8px; padding:8px 12px; cursor:pointer; }
button:hover { border-color:var(--accent); }
input[type=range] { flex:1; min-width:180px; accent-color:var(--accent); }
.small { font-size:.84rem; color:var(--muted); }
.status { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:12px; }
.stat { border:1px solid var(--line); border-radius:10px; padding:8px; background:#0d1528; }
.stat b { display:block; color:var(--text); font-size:1rem; }
.callout { border-left:3px solid var(--accent); padding:8px 12px; background:#102637; color:#d9f7f2; }
@media (max-width:850px) { .grid { grid-template-columns:1fr; } .status { grid-template-columns:1fr; } body { padding:12px; } }
</style>
</head>
<body>
<main>
  <span class="badge">MODELLED LAYER — NOT CALIBRATED TO VIDEO</span>
  <h1>NileRed BZ Virtual Twin</h1>
  <p>Interactive visualization of the normalized Oregonator reaction–diffusion model. The vessel colors are an abstract x-state proxy, not measured concentrations or camera pixels.</p>
  <div class="callout"><b>How to use:</b> press Play, drag the timeline, and compare the animated vessel field with the model signal. The source video is provided for context; synchronization and quantitative comparison are intentionally not claimed yet.</div>
  <div class="grid">
    <section class="panel">
      <h2>Source video context</h2>
      <iframe id="sourceVideo" style="width:100%;aspect-ratio:16/9;border:0;border-radius:10px;background:#080b14" title="NileRed source video" allowfullscreen></iframe>
      <p class="small">External YouTube embed. The repository does not copy or redistribute the video.</p>
    </section>
    <section class="panel">
      <h2>Virtual vessel cross-section</h2>
      <canvas id="vessel" width="700" height="420" aria-label="Animated virtual vessel"></canvas>
      <div class="controls">
        <button id="play">Play</button><button id="reset">Reset</button>
        <label class="small" for="speed">Speed</label><select id="speed"><option value="1">1×</option><option value="2">2×</option><option value="0.5">0.5×</option></select>
      </div>
    </section>
  </div>
  <section class="panel" style="margin-top:16px">
    <h2>Model signal and timeline</h2>
    <canvas id="trace" width="1200" height="300" aria-label="Model signal plot"></canvas>
    <div class="controls"><input id="timeline" type="range" min="0" max="0" value="0" step="1" aria-label="Model timeline"><span id="timeLabel" class="small"></span></div>
    <div class="status">
      <div class="stat"><span class="small">Well-mixed peaks</span><b id="peaks"></b></div>
      <div class="stat"><span class="small">Mean period</span><b id="period"></b></div>
      <div class="stat"><span class="small">Spatial solver</span><b id="solver"></b></div>
    </div>
  </section>
  <section class="panel" style="margin-top:16px">
    <h2>Scientific status</h2>
    <p><b>What this demonstrates:</b> a reproducible animated rendering of the current abstract kinetics model, including spatial variation and a synchronized model trace.</p>
    <p><b>What remains:</b> calibrated video extraction, physical vessel dimensions, verified experimental conditions, and approved molecular structures. Those are required before this can be called a quantitatively validated experiment twin.</p>
    <p class="small">Source video: <a id="sourceLink" target="_blank" rel="noopener"></a></p>
  </section>
</main>
<script id="twin-data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('twin-data').textContent);
const vessel = document.getElementById('vessel'), trace = document.getElementById('trace');
const vctx = vessel.getContext('2d'), tctx = trace.getContext('2d');
const timeline = document.getElementById('timeline'), timeLabel = document.getElementById('timeLabel');
const play = document.getElementById('play'), reset = document.getElementById('reset'), speed = document.getElementById('speed');
const sourceUrl = D.source_video_url;
document.getElementById('sourceVideo').src = sourceUrl.replace('watch?v=', 'embed/');
document.getElementById('sourceLink').href = sourceUrl; document.getElementById('sourceLink').textContent = sourceUrl;
document.getElementById('peaks').textContent = D.metrics.well_mixed_peak_count;
document.getElementById('period').textContent = D.metrics.well_mixed_mean_period.toFixed(3) + ' model units';
document.getElementById('solver').textContent = D.metrics.spatial_solver_success ? 'success' : 'failed';
timeline.max = D.times.length - 1;
let frame = 0, running = false, last = 0, accumulator = 0;
function color(v) { const hue = 220 - 220 * Math.max(0, Math.min(1, v)); return `hsl(${hue}, 84%, 56%)`; }
function roundedRect(ctx,x,y,w,h,r) { ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
function drawVessel() {
  const w=vessel.width,h=vessel.height; vctx.clearRect(0,0,w,h);
  vctx.fillStyle='#070b14'; vctx.fillRect(0,0,w,h);
  const x=95,y=45,vw=w-190,vh=h-110;
  vctx.fillStyle='#b9d7ef22'; vctx.strokeStyle='#a7c9e8'; vctx.lineWidth=5; roundedRect(vctx,x,y,vw,vh,30); vctx.fill(); vctx.stroke();
  const f=D.field[frame], innerX=x+10, innerY=y+10, innerW=vw-20, innerH=vh-20, stripH=innerH/f.length;
  for (let i=0;i<f.length;i++) { vctx.fillStyle=color(f[i]); vctx.fillRect(innerX,innerY+i*stripH,innerW,stripH+1); }
  vctx.fillStyle='#eaf0ff'; vctx.font='600 18px system-ui'; vctx.fillText('virtual vessel', x, h-34);
  vctx.font='14px system-ui'; vctx.fillStyle='#aab7d4'; vctx.fillText('color = normalized abstract x proxy', x, h-14);
  vctx.fillStyle='#eaf0ff'; vctx.fillText('position', 16, y+vh/2); vctx.save(); vctx.translate(35,y+vh/2); vctx.rotate(-Math.PI/2); vctx.fillText('1-D position',0,0); vctx.restore();
  vctx.fillStyle='#64d8cb'; vctx.font='700 16px system-ui'; vctx.fillText('t = '+Number(D.times[frame]).toFixed(2), w-170, 28);
}
function plotLine(ctx, data, x,y,w,h, colorValue) { ctx.beginPath(); data.forEach((v,i)=>{ const px=x+i*(w/(data.length-1)); const py=y+h-(v*h); if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py); }); ctx.strokeStyle=colorValue;ctx.lineWidth=3;ctx.stroke(); }
function drawTrace() {
  const w=trace.width,h=trace.height; tctx.clearRect(0,0,w,h); tctx.fillStyle='#070b14';tctx.fillRect(0,0,w,h);
  const x=70,y=28,pw=w-105,ph=h-75; tctx.strokeStyle='#3a4b6d';tctx.lineWidth=1;tctx.strokeRect(x,y,pw,ph);
  plotLine(tctx,D.well_mixed_signal,x,y,pw,ph,'#7da7ff');
  const marker = Number(D.times[frame]) / Number(D.well_mixed_time[D.well_mixed_time.length-1]);
  const mx=x+Math.max(0,Math.min(1,marker))*pw; tctx.strokeStyle='#64d8cb';tctx.lineWidth=3;tctx.beginPath();tctx.moveTo(mx,y);tctx.lineTo(mx,y+ph);tctx.stroke();
  tctx.fillStyle='#eaf0ff';tctx.font='600 16px system-ui';tctx.fillText('normalized model x signal',x,y-8);tctx.font='13px system-ui';tctx.fillStyle='#aab7d4';tctx.fillText('dimensionless time',x+pw/2-45,h-12);tctx.save();tctx.translate(18,y+ph/2);tctx.rotate(-Math.PI/2);tctx.fillText('normalized x proxy',0,0);tctx.restore();
}
function draw(){ drawVessel(); drawTrace(); timeLabel.textContent='frame '+(frame+1)+' / '+D.times.length+' · t = '+Number(D.times[frame]).toFixed(3)+' dimensionless model units'; timeline.value=frame; }
timeline.addEventListener('input',()=>{frame=Number(timeline.value);draw();});
play.addEventListener('click',()=>{running=!running;play.textContent=running?'Pause':'Play';if(running)requestAnimationFrame(tick);});
reset.addEventListener('click',()=>{running=false;play.textContent='Play';frame=0;draw();});
function tick(now){if(!running)return;if(!last)last=now;accumulator+=(now-last)*Number(speed.value);last=now;if(accumulator>90){frame=(frame+1)%D.times.length;accumulator=0;draw();}requestAnimationFrame(tick);}
draw();
</script>
</body>
</html>
'''


def write_virtual_twin_bundle(
    output_dir: Path,
    *,
    well_mixed: dict[str, Any],
    spatial: dict[str, Any],
    n_frames: int = 121,
    source_video_url: str = DEFAULT_SOURCE_VIDEO,
) -> dict[str, Any]:
    """Write the interactive HTML demo and its inspectable JSON data."""
    output_dir.mkdir(parents=True, exist_ok=True)
    data = build_virtual_twin_data(
        well_mixed,
        spatial,
        n_frames=n_frames,
        source_video_url=source_video_url,
    )
    data_path = output_dir / "virtual_twin_data.json"
    html_path = output_dir / "virtual_twin.html"
    data_path.write_text(json.dumps(data, indent=2) + "\n")
    html = _HTML_TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    html_path.write_text(html)
    return {
        "html": html_path.name,
        "data": data_path.name,
        "frames": len(data["times"]),
        "calibration_status": data["calibration_status"],
    }
