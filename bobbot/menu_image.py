from PIL import Image, ImageDraw, ImageFont
import platform
import urllib.request as req

def pillow_image(pic, name, where, submenu, kcal):
    if platform.system() == 'Darwin':  # when mac
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows':  # when windows
        font = 'malgun.ttf'
    elif platform.system() == 'Linux':
        '''
        !wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf"
        !mv malgun.ttf /usr/share/fonts/truetype/
        import matplotlib.font_manager as fm 
        fm._rebuild() 
        '''
        font = 'malgun.ttf'
    try:
        imageFont = ImageFont.truetype(font, 20, encoding="UTF-8")
    except:
        imageFont = ImageFont.load_default()
    img = Image.open(pic)
    img = img.resize((300, 300), Image.Resampling.BILINEAR)
    draw = ImageDraw.Draw(img)
    texts = [name, where, f"{kcal}kcal"]
    y = 220
    for txt in texts:
        draw.text((5, y), txt, font=imageFont, align="left", fill="red")
        y += 25
    img.save(pic)

def menu_image_download(dict: dict):
    if 'photo' not in dict.keys() or dict['photo'] is None:
        return 'No photos in the dict'
    elif 'name' not in dict.keys() or dict['name'] is None:
        raise 'invalidName'
    else:
        req.urlretrieve(dict['photo'], f"{dict['name']}.png")
        pillow_image(f"{dict['name']}.png", dict['name'], dict['where'], dict['submenu'], dict['kcal'])

