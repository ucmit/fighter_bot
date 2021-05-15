import os, requests, glob
from PIL import Image

imgs = {
    "vs_bg": "./img/vs_bg.png",
    "vs_bg_animated": "./img/vs_animated/frame_*.jpg"
}

async def vs_create(url1:str, url2:str):
    vs_bg = Image.open(  os.path.join(imgs["vs_bg"])  )

    size = (250, 250)

    f1 = Image.open(   requests.get(url1,  stream=True).raw     ).resize(size)
    f2 = Image.open(   requests.get(url2,  stream=True).raw     ).resize(size)

    pos1 = (  vs_bg.width//2 - f1.width*2  ,  vs_bg.height//2  - f1.height//2 )
    pos2 = (  vs_bg.width//2 + f2.width    ,  vs_bg.height//2  - f2.height//2 )

    vs_bg.paste( f1,  pos1  )
    vs_bg.paste( f2,  pos2  )

    vs_bg.save(  os.path.join("./img", "result.png") )

async def vs_create_animated(url1:str, url2:str):
    bg_size = (852, 480)
    vs_bg, *vs = [Image.open(f).resize(bg_size) for f in sorted(glob.glob(imgs["vs_bg_animated"]))]

    size = (75, 75)
    f1 = Image.open(   requests.get(url1,  stream=True).raw     ).resize(size)
    f2 = Image.open(   requests.get(url2,  stream=True).raw     ).resize(size)

    pos1 = (  vs_bg.width//2 - f1.width*2  ,  vs_bg.height//2  - f1.height//2 )
    pos2 = (  vs_bg.width//2 + f2.width    ,  vs_bg.height//2  - f2.height//2 )

    vs_bg.paste( f1,  pos1  )
    vs_bg.paste( f2,  pos2  )

    for im in vs:
        im.paste( f1,  pos1  )
        im.paste( f2,  pos2  )

    vs_bg.save(fp=os.path.join("./img", "result.gif"), format='GIF', append_images=vs, save_all=True, duration=0.03, loop=0)