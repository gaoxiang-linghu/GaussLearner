#!/usr/bin/env python3
"""Replace only the four-second title card; preserve the source soundtrack/content."""
import json, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
site=Path(__file__).resolve().parents[1]
root=site.parent
out=root/'outputs/video/video_publicity'
out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
im=Image.new('RGB',(1920,1080),'#ffffff');d=ImageDraw.Draw(im)
def center(text,y,size,fill='#293441',heavy=False):
 f=ImageFont.truetype(bold if heavy else font,size)
 d.text((960,y),text,font=f,anchor='mt',fill=fill)
center('GaussLearner',150,96,'#3479ad',True)
center('3D Gaussian Primitives as',285,52)
center('Self-Regulating Continual Learners',355,52)
center('Gaoxiang Linghu¹   Haonan Zhou¹   Xuanhe Liu¹   Weili Xu¹',490,33)
center('Kaiyue Zhou²*   Jun Xiao¹   Gaoang Wang¹*',550,33)
center('¹ Zhejiang University     ² Chengdu Minto Tech',644,31)
center('* Corresponding authors',696,23,'#626c78')
card=out/'title_public.png';im.save(card)
im.save(site/'assets/video/poster.webp','WEBP',quality=94)
src=root/'outputs/video/sup_submission/GaussLearner_full.mp4'
video=out/'GaussLearner_public.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-i',str(card),'-i',str(src),'-filter_complex','[0:v]trim=duration=4,setpts=PTS-STARTPTS,format=yuv420p,setsar=1[title];[1:v]trim=start=4,setpts=PTS-STARTPTS,setsar=1[body];[title][body]concat=n=2:v=1:a=0[v]','-map','[v]','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','19','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-map_metadata','-1','-metadata','title=GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners','-movflags','+faststart',str(video)],check=True)
shutil.copy2(video,site/'assets/video'/video.name)
shutil.copy2(root/'outputs/video/sup_submission/MUSIC_CREDITS.txt',out/'MUSIC_CREDITS.txt')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
(out/'verification.json').write_text(json.dumps(probe,indent=2)+'\n')
(out/'README.txt').write_text('Publicity video derived from sup_submission/GaussLearner_full.mp4.\nOnly the first 4-second title card is replaced with the full author list, affiliations.\nAll comparison frames, narration, ending credits and the original soundtrack are preserved.\nAsset sources and provenance are documented in GaussLearner/ASSETS.md.\nMusic attribution is included in the original ending card and MUSIC_CREDITS.txt.\n')
print('Publicity video ready:',video)
