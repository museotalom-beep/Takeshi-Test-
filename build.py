"""Create a portable HTML game with every campaign photograph, script, and style embedded."""
from pathlib import Path
import base64, json, re
root=Path(__file__).parent
art={p.stem:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (root/'public/images').glob('*.png')}
required={'dunes','family','adventure','premium','camp','sunset'}
assert required <= art.keys(), f'Missing campaign photographs: {required-art.keys()}'
css=(root/'style.css').read_text()
for name,data in art.items():
    css=css.replace("url('public/images/"+name+".png')", 'var(--photo-'+name+')')
engine=(root/'engine.js').read_text().replace('export ', '')
app=(root/'app.js').read_text()
app=re.sub(r'^import .*?;\n','',app,count=1)
app=re.sub(r'src="public/images/\$\{(.*?)\}\.png"',lambda m:'src="${ART_DATA['+m[1]+']}"',app)
app=re.sub(r'src="public/images/([a-z]+)\.png"',lambda m:'src="${ART_DATA.'+m[1]+'}"',app)
script='const ART_DATA='+json.dumps(art)+';\n'+'''Object.entries(ART_DATA).forEach(([id,url])=>document.documentElement.style.setProperty('--photo-'+id,'url("'+url+'")'));\n'''+engine+'\n'+app
html=(root/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>').replace('<script type="module" src="app.js"></script>','<script type="module">'+script+'</script>')
(root/'dist').mkdir(exist_ok=True)
output=root/'dist/campaign-arena.html';output.write_text(html)
(root/'dist/campaign-arena-realistic.html').write_text(html)
print(f'Built {output.name}: {output.stat().st_size:,} bytes. No external dependencies.')
