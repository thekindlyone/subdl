import os,sys,hashlib
from os.path import join,getsize,splitext,dirname
import requests
movie_exts=[".avi",".mp4",".mkv",".mpg",".mpeg",".mov",".rm",".vob",".wmv",".flv",".3gp"]

def getHash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def srtify(fn):
    return splitext(fn)[0]+'.srt'

def getsubs(md5):
    headers={'User-Agent':'SubDB/1.0 (subdl/0.1; http://github.com/thekindlyone/subdl)'}
    url="http://api.thesubdb.com/?action=download&hash="+md5+"&language=en"
    try:
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            return True,r.content
        else:
            return False,r.status_code
    except:
        e = sys.exc_info()[0]
        return False,e


def writesubs(name,subs):
    with open(srtify(name),'w') as f:
        f.write(subs)

def fetch_files(cwd):
    for root,dirs,files in os.walk(cwd):
        for name in files:
            if splitext(name)[-1] in movie_exts and srtify(name) not in files:
                yield join(root, name)       


def main():
    cwd="."
    if len(sys.argv)>1:
        cwd=sys.argv[1]
    done,skipped=0,0
    weirderrors=False
    for name in fetch_files(cwd):
        print "processing ",name
        status,content=getsubs(getHash(name))       

        if not status:
            skipped+=1
            print "Skipped. Reason: ",content
            if len(str(content))>4:
                weirderrors=True
            continue
        else:
            writesubs(name,content)
            print 'subs written'
            done+=1
    print '''
    ******************************
    REPORT
    Done {} files
    Skipped {} files
    Total {} files processed
    ******************************
    '''.format(done,skipped,done+skipped)
    if not weirderrors:
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())