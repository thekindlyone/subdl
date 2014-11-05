import os,sys,hashlib
from os.path import join,getsize,splitext,dirname
import requests
import itertools
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

def get_page(url,headers,max_attempts):
    for i in xrange(max_attempts):
        r = requests.get(url,headers=headers)
        if r.status_code == 200 :
            return r.content
    print r.status_code
    return False

def getsubs(md5):
    headers={'User-Agent':'SubDB/1.0 (subdl/0.1; http://thekindlyone.info)'}
    url="http://api.thesubdb.com/?action=download&hash="+md5+"&language=en"
    try:
        content=get_page(url,headers,5)
    except:
        e = sys.exc_info()[0]
        return False,e
    if content:
        return True,content
    else :
        return False,"Subs Not Found"

def writesubs(name,subs):
    with open(srtify(name),'w') as f:
        f.write(subs)

def fetch_files(cwd):
    for root,dirs,files in os.walk(cwd):
        for name in files:
            if splitext(name)[-1] in movie_exts and srtify(name) not in files:
                yield join(root, name)   
    

cwd="."
if len(sys.argv)>1:
    cwd=sys.argv[1]
done,skipped=0,0
for name in fetch_files(cwd):
    print "processing ",name
    status,content=getsubs(getHash(name))
    if not status:
        skipped+=1
        print "Skipped. Reason: ",content
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



