from urllib.request import urlopen
import re, os, json

with open('config.json',mode='r',encoding='utf-8') as f:
    conf = json.load(f)

def preDir():
    tomake = [conf['wbase'],os.path.join(conf['wbase'],conf['weather']['imgcache']),conf['rssbase']]
    for rss in conf['rss']:
        tomake.append(os.path.join(conf['rssbase'],rss['imgcache']))
    for i in tomake:
        try:
            os.mkdir(i)
        except Exception as err:
            pass

def getWeather():
    with urlopen(conf['weather']['uri']) as page:
        with open(os.path.join(conf['wbase'],conf['weather']['cache']),'wb') as f:
            f.write(page.read())
    with urlopen(conf['weather']['imguri']) as page:
        regex = re.compile("\"\./.*?\"")
        links = regex.findall(page.read().decode())
        for i in range(0,3):
            links[i] = conf['weather']['base']+links[i][2:-1]
        for i in range(0,3):
            with open(os.path.join(conf['wbase'],conf['weather']['imgcache'],"%d.png"%i),"wb") as f:
                with urlopen(links[i]) as img:
                    f.write(img.read())

#clear cache
def clearAssets():
    for rss in conf['rss']:
        ls = os.listdir(os.path.join(conf['rssbase'],rss['imgcache']))
        for i in ls:
            os.remove(os.path.join(conf['rssbase'],rss['imgcache'], i))


def getRSS():
    for rss in conf['rss']:
        with urlopen(rss['uri']) as page:
            thispage = page.read().decode()
            for imgsrc in re.findall('<[imgIMG]+.*?[srcSRC]+=[\'\"](.*?)[\'\"].*?>', thispage):
                try:
                    print('Raw src',imgsrc)
                    imgpath = os.path.join(conf['rssbase'],rss['imgcache'],imgsrc.split('?')[0].split('/')[-1])
                    src=imgsrc
                    if src[0] == '/':
                        src = rss['base'] + src
                
                    print('Converted',src)
                    print('Local',imgpath)
                    if not '.' in imgpath:
                        raise(Exception())
                    with open(imgpath, 'wb') as f:
                        f.write(urlopen(src).read())
                    
                    thispage = thispage.replace(imgsrc,os.path.join(conf['cdir'],imgpath)
)
                except Exception as err:
                    print('Skip')
            with open(os.path.join(conf['rssbase'],rss['cache']),mode='w',encoding='utf-8') as f:
                f.write(thispage)

if __name__ == "__main__":
    preDir()
    print('Dir Prepared')
    clearAssets()
    print('Assets Cleared')
    getWeather()
    print('Weather Got')
    getRSS()
    print("Done.")
