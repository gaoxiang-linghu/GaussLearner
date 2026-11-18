#!/usr/bin/env python3
"""Export the supplied manuscript's figures, captions and tables to a static page.
Requires poppler (pdftoppm), Pillow, and the local manuscript. No build on hosting.
"""
import argparse, html, json, re, subprocess, tempfile
from pathlib import Path
from PIL import Image
SITE = Path(__file__).resolve().parents[1]
PAPER = Path(argparse.ArgumentParser().parse_known_args()[1][0]) if len(__import__('sys').argv)>1 else SITE.parent/'Paper/arxiv_camera_v1'
FIGS = {
 'teaser': 'teaser/teaser_vector_1108_charts_view_clean.pdf',
 'paradigm': 'method_compare/paradigm_1105_outlined.pdf',
 'framework': 'overview_white_bg_2_compatible.pdf',
 'cl3d-comparison': 'comparison/comparison_main.pdf',
 'other-comparison': 'comparison/comparison_detailed.pdf',
 'adaptation-preservation': 'changed_unchanged_1031.pdf',
 'extra-cl3d-1': 'supplementary/cl3d_1.pdf',
 'extra-cl3d-2': 'supplementary/cl3d_2.pdf',
 'extra-clsplats': 'supplementary/CLSplats.pdf',
 'extra-wat-1': 'supplementary/WAT_1.pdf',
 'extra-wat-2': 'supplementary/WAT_2.pdf',
}
def group(s, start):
 assert s[start]=='{'
 depth=1
 for i in range(start+1,len(s)):
  if s[i]=='{' and s[i-1]!='\\': depth+=1
  if s[i]=='}' and s[i-1]!='\\': depth-=1
  if depth==0:return s[start+1:i],i+1
 raise ValueError('Unbalanced LaTeX')
def plain(s):
 s=re.sub(r'%[^\n]*','',s)
 s=s.replace('\\method{}','GaussLearner').replace('\\method','GaussLearner')
 s=re.sub(r'\\(?:cite|label)\{[^}]*\}', '', s)
 s=re.sub(r'\\ref\{[^}]*\}', '',s)
 s=s.replace('~',' ').replace('\\ ',' ').replace('\\,',' ').replace('\\!','')
 s=s.replace('\\uparrow','↑').replace('\\downarrow','↓').replace('\\&','&')
 s=s.replace('\\textsc{GaussLearner}', 'GaussLearner')
 s=re.sub(r'\\textcolor\{[^}]*\}\{\\scriptsize[^}]*\}', '',s)
 s=re.sub(r'\\(?:textbf|underline|emph|mbox|textsc)\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\(?:textbf|underline|emph|mbox|textsc)\{([^{}]*)\}',r'\1',s)
 s=s.replace('$','').replace('\\text','').replace('{','').replace('}','')
 return re.sub(r'\s+',' ',s).strip()
sources='\n'.join((PAPER/f).read_text() for f in ['main.tex','sec/1_intro.tex','sec/3_method.tex','sec/4_experiments.tex','sec/X_suppl.tex'])
def caption(file):
 needle='{figures/'+file+'}'
 start=sources.index(needle)+len(needle)
 m=re.search(r'\\caption(?:of\{figure\})?\{',sources[start:])
 s,_=group(sources,start+m.end()-1)
 return plain(s)
manifest=[]
manifest_path = SITE/'assets/figures/manifest.json'
previous = {f['id']: f for f in json.loads(manifest_path.read_text())} if manifest_path.exists() else {}
for name,file in FIGS.items():
 out=SITE/'assets/figures'/f'{name}.webp'
 if not out.exists() or previous.get(name, {}).get('render_box') != 'CropBox':
  with tempfile.TemporaryDirectory() as td:
   prefix=Path(td)/'figure'
   # graphicsx uses the PDF's CropBox; preserve that same authored crop on the web.
   subprocess.run(['pdftoppm','-f','1','-singlefile','-cropbox','-scale-to','2400','-png',str(PAPER/'figures'/file),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
   with Image.open(str(prefix)+'.png') as im: im.convert('RGB').save(out,'WEBP',quality=92,method=6)
 with Image.open(out) as im:w,h=im.size
 manifest.append({'id':name,'source':'figures/'+file,'output':str(out.relative_to(SITE)),'caption':caption(file),'width':w,'height':h,'render_box':'CropBox'})
(SITE/'assets/figures/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
byid={v['id']:v for v in manifest}
def figure(name,cls=''):
 f=byid[name]
 return f'''<figure class="paper-figure {cls}"><a class="figure-link" href="{f['output']}" data-lightbox aria-label="Enlarge figure: {html.escape(f['caption'].split('.')[0])}"><img src="{f['output']}" width="{f['width']}" height="{f['height']}" loading="lazy" decoding="async" alt="{html.escape(f['caption'])}"></a><figcaption>{html.escape(f['caption'])}</figcaption></figure>'''
exp=(PAPER/'sec/4_experiments.tex').read_text()
def table(label,scenes):
 # Tables retain numerical values, bold and underline from the manuscript.
 pos=exp.index('\\label{'+label+'}')
 end=exp.index('\\end{table',pos)
 block=exp[pos:end]
 body=block[block.index('\\midrule')+len('\\midrule'):block.index('\\bottomrule')]
 rows=[]
 for raw in body.split('\\\\'):
  raw=raw.replace('\\midrule','').strip()
  if not raw or '&' not in raw:continue
  cells=raw.split('&')
  values=[]
  for cell in cells:
   text=html.escape(plain(cell))
   if '\\textbf' in cell: text='<strong>'+text+'</strong>'
   elif '\\underline' in cell: text='<u>'+text+'</u>'
   values.append(text)
  assert len(values)==1+len(scenes)*2,(label,values)
  ours=' class="ours"' if 'GaussLearner' in values[0] else ''
  rows.append('<tr'+ours+'><th scope="row">'+values[0]+'</th>'+''.join('<td>'+v+'</td>' for v in values[1:])+'</tr>')
 title={'tab:clbench-main':'Novel-view synthesis results on CL-3D. For each scene, results are averaged equally across evaluated states. Higher is better for PSNR and SSIM. Best results are bold, and second-best results are underlined.','tab:clsplats-results':'Novel-view synthesis results on CL-Splats. State 1 results are reported. Best results are bold, and second-best results are underlined.','tab:wat-results':'Novel-view synthesis results on WAT. For each scene, results are averaged equally across states 1–4. Best results are bold, and second-best results are underlined.'}[label]
 return '<div class="table-scroll" tabindex="0" role="region" aria-label="'+html.escape(title.split('.')[0])+'"><table><caption>'+title+'</caption><thead><tr><th rowspan="2" scope="col">Method</th>'+''.join('<th colspan="2" scope="colgroup">'+v+'</th>' for v in scenes)+'</tr><tr>'+''.join('<th scope="col">PSNR ↑</th><th scope="col">SSIM ↑</th>' for v in scenes)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
abstract=(PAPER/'sec/0_abstract.tex').read_text().split('\\begin{abstract}')[1].split('\\end{abstract}')[0]
citation='''@misc{linghu2026gausslearner,
  title  = {GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners},
  author = {Gaoxiang Linghu and Haonan Zhou and Xuanhe Liu and Weili Xu and
            Kaiyue Zhou and Jun Xiao and Gaoang Wang},
  year   = {2026}
}'''
(SITE/'citation.bib').write_text(citation+'\n')
page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners</title>
<meta name="description" content="GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners. Gaoxiang Linghu, Haonan Zhou, Xuanhe Liu, Weili Xu, Kaiyue Zhou, Jun Xiao, and Gaoang Wang.">
<meta property="og:type" content="website"><meta property="og:title" content="GaussLearner"><meta property="og:description" content="3D Gaussian Primitives as Self-Regulating Continual Learners"><meta property="og:image" content="https://gaoxiang-linghu.github.io/GaussLearner/assets/figures/teaser.webp"><meta property="og:url" content="https://gaoxiang-linghu.github.io/GaussLearner/">
<meta name="theme-color" content="#142238"><link rel="canonical" href="https://gaoxiang-linghu.github.io/GaussLearner/"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css?v=2"><script src="script.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="hero"><div class="container hero-inner">
<h1><span class="project-name">GaussLearner</span><span class="paper-title">3D Gaussian Primitives as<br class="desktop-break"> Self-Regulating Continual Learners</span></h1>
<div class="authors"><span>Gaoxiang Linghu<sup>1</sup></span><span>Haonan Zhou<sup>1</sup></span><span>Xuanhe Liu<sup>1</sup></span><span>Weili Xu<sup>1</sup></span><span>Kaiyue Zhou<sup>2,*</sup></span><span>Jun Xiao<sup>1</sup></span><span><a href="https://cvnext.github.io/" target="_blank" rel="noopener noreferrer">Gaoang Wang</a><sup>1,*</sup></span></div>
<div class="affiliations"><span><sup>1</sup>Zhejiang University</span><span><sup>2</sup>Chengdu Minto Tech</span></div>
<p class="corresponding">* Corresponding authors</p>
<div class="resources" aria-label="Project resources"><button class="resource" type="button" disabled title="Paper link will be added after the arXiv release"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6M9 16h6"/></svg>Paper <span class="badge">Coming Soon</span></button><button class="resource" type="button" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-14-2 18"/></svg>Code <span class="badge">Coming Soon</span></button></div>
</div></header>
<main id="main">
<section class="container video-section" aria-label="GaussLearner video"><video class="main-video" controls playsinline preload="none" poster="assets/video/poster.webp" aria-label="GaussLearner project video"><source src="assets/video/GaussLearner_public.mp4" type="video/mp4">Your browser does not support HTML video.</video></section>
<section class="container teaser-section" aria-label="Teaser">'''+figure('teaser')+'''</section>
<section class="section abstract-section"><div class="text-container"><h2>Abstract</h2><p>'''+html.escape(plain(abstract))+'''</p></div></section>
<section class="section container" aria-labelledby="method-heading"><h2 id="method-heading">Method</h2><div class="narrow-figure">'''+figure('paradigm')+'''</div>'''+figure('framework')+'''</section>
<section class="section tinted" aria-labelledby="qualitative-heading"><div class="container"><h2 id="qualitative-heading">Qualitative Results</h2>'''+figure('cl3d-comparison')+figure('other-comparison')+'''
<details class="additional"><summary>Additional Qualitative Comparisons</summary><div class="additional-content">'''+''.join(figure(n) for n in ['extra-cl3d-1','extra-cl3d-2','extra-clsplats','extra-wat-1','extra-wat-2'])+'''</div></details></div></section>
<section class="section container" aria-labelledby="quantitative-heading"><h2 id="quantitative-heading">Quantitative Results</h2>'''+table('tab:clbench-main',['ClubRoom','FloorLounge','Fridge','OfficeHub','StudyNook','ApartmentRoom'])+table('tab:clsplats-results',['Cupboard','Desk','Room','Shelf'])+table('tab:wat-results',['Breville','Car','Grill','Mac'])+'''<div class="narrow-figure">'''+figure('adaptation-preservation')+'''</div></section>
<section class="section citation-section"><div class="text-container"><div class="citation-heading"><h2>Citation</h2><button id="copy-citation" type="button">Copy BibTeX</button></div><pre><code id="bibtex">'''+html.escape(citation)+'''</code></pre><p id="copy-status" role="status" aria-live="polite"></p></div></section>
</main><dialog id="figure-dialog" aria-label="Enlarged paper figure"><button id="close-figure" type="button" aria-label="Close enlarged figure">×</button><img id="dialog-image" alt=""></dialog>
</body></html>'''
(SITE/'index.html').write_text(page)
print('Exported',len(manifest),'figures and 3 manuscript tables.')
