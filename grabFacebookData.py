#!/usr/bin/env python2
"""
Created by mchirico@gmail.com




"""
from __future__ import print_function

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os

#import sys
#sys.path.append('./lib')



try:
    import subprocess
except ImportError:
    pass

try:
    import shlex
except ImportError:
    pass


import os,time,sys,signal,getopt,re,glob
import urllib
import urllib2

import json
import datetime

# Global


import tokenf
TOKEN=tokenf.TOKEN

TMPDIR=tokenf.TMPDIR
DATADIR=tokenf.DATADIR

BEAR="Bearer %s" % (TOKEN)




#FACEBOOK_GROUP=tokenf.FACEBOOK_GROUP["Unofficial Cheltenham Township, PA"]
FACEBOOK_GROUP=tokenf.FACEBOOK_GROUP




import errno
def Mkdir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass


class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        print("redirect:",newurl)





Mkdir(TMPDIR)
Mkdir(DATADIR)

        
f_msg=open(TMPDIR+'/msg.csv','w')
f_msg.close()
f_likes=open(TMPDIR+'/likes.csv','w')
f_likes.close()

f_comments=open(TMPDIR+'/comments.csv','w')
f_comments.close()
f_comments=open(TMPDIR+'/comments.csv','a')


f_msg=open(TMPDIR+'/msg.csv','a')
f_likes=open(TMPDIR+'/likes.csv','a')

        
def parseJ(k):
    if 'data' not in k:
        return
    m=k['data']
    for i in m:
        id=i['id']
        from_id=i['from']['id']
        name=i['from']['name']
        name=re.sub("[^A-Za-z0-9\)\; \(\@\:\+\-\=\?\#\=\./\&]+", '',name)
        created_time=i['created_time']
        if 'message' in i:
            msg=re.sub("[^A-Za-z0-9\)\,\; \(\@\:\+\'\,\-\=\?\n!\#\=\./\&]+", '',i['message'])
            msg=msg.replace("'",'{APOST}')
            msg=msg.replace(",",'{COMMA}')
            msg=msg.replace("\n",'{RET}')
            permalink_url=i['permalink_url']
            shares='0'
            if 'shares' in i:
                shares=i['shares']['count']
            f_msg.write(id+','+from_id+','+name+','+created_time+','+str(shares)+','+permalink_url+',"'+msg+'"\n')
        if 'reactions' in i:
            Reactions=i['reactions']['data']
            for j in Reactions:
                rtype=j['type']
                rname=j['name']
                rname=re.sub("[^A-Za-z0-9\)\; \(\@\:\+\-\=\?\#\=\./\&]+", '',rname)
                rid=j['id']
                f_likes.write(id+',x,'+rtype+','+rid+','+rname+'\n')
        if 'comments' in i:
            Comments=i['comments']['data']
            for j in Comments:
                cid=j['id']
                ctime=j['created_time']
                cname=j['from']['name']
                cname=re.sub("[^A-Za-z0-9\)\; \(\@\:\+\,\-\=\?\n!\#\=\./\&]+", '',cname)
                cfrom_id=j['from']['id']
                if 'message' not in j:
                    continue
                cmsg=re.sub("[^A-Za-z0-9\)\,\; \(\@\:\+\'\,\-\=\?\n!\#\=\./\&]+", '',j['message'])
                cmsg=cmsg.replace("'",'{APOST}')
                cmsg=cmsg.replace(",",'{COMMA}')
                cmsg=cmsg.replace("\n",'{RET}')
                f_comments.write(id+','+cid+','+ctime+','+cfrom_id+','+cname+',,'+cmsg+'\n')
                if 'comments' in j:
                    Comments_on_comments = j['comments']['data']
                    for p in Comments_on_comments:
                        ccmsg=p['message']
                        ccid=p['id']
                        ccmsg=re.sub("[^A-Za-z0-9\)\,\; \(\@\:\+\'\,\-\=\?\n!\#\=\./\&]+", '',ccmsg)
                        ccmsg=ccmsg.replace("'",'{APOST}')
                        ccmsg=ccmsg.replace(",",'{COMMA}')
                        ccmsg=ccmsg.replace("\n",'{RET}')
                        if 'from' in p:
                            if 'id' in p['from']:
                                ccid=p['from']['id']
                                ctime=p['created_time']
                        f_comments.write(id+','+cid+','+ctime+','+cfrom_id+','+cname+','+ccid+',"'+ccmsg+'"\n')
                if 'likes' in j and 'data' in j['likes']:
                    Clikes=j['likes']['data']
                    for a in Clikes:
                        name=a['name']
                        name=re.sub("[^A-Za-z0-9\)\; \(\@\:\+\-\=\?\n!\#\=\./\&]+", '',name)
                        f_likes.write(id+','+cid+',LIKES,'+a['id']+','+name+'\n')

            
            



def members(limit=20):
    url='https://graph.facebook.com/v2.5/'+FACEBOOK_GROUP+'/members?fields=picture,name&limit=%s&access_token=%s' % (limit,TOKEN)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {}
    headers = { 'Authorization':  BEAR}
    h = MyHTTPRedirectHandler()
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    data = urllib.urlencode(values)
    json_data = ""
    try:
        req = urllib2.build_opener(h)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()
        json_data = json.loads(the_page)
    except:
        print("Error reading data from members"+FACEBOOK_GROUP)
    return json_data


def writeMembers(k):
    if 'data' not in k:
        return
    f=open(TMPDIR+'/members.csv','w')    
    for i in k['data']:
        picture=''
        name=i['name']
        name=re.sub("[^A-Za-z0-9\)\; \(\@\:\+\-\=\?\n!\#\=\./\&]+", '',name)
        id=i['id']
        if 'picture' in i:
            picture=i['picture']['data']['url']
        f.write(str(id)+','+name+','+str(picture)+'\n')
    f.close()        
        
            


                    
# k=getJson()
# k['data'][2]['reactions']['data'][0]
# k['data'][0]['from']
# k['data'][0]['created_time']
# k['data'][0]['message']
# k['data'][0]['permalink_url']
def getJson(limit=13,since='2016-05-25',until='2016-05-26'):
    url='https://graph.facebook.com/v2.5/'+FACEBOOK_GROUP+'/feed?fields=reactions.limit(500){link,name,pic_square,type},message,name,id,created_time,permalink_url,shares,comments.limit(500){created_time,likes.limit(500),message,from,comments.limit(507){likes,message,from,created_time}},from&limit=%s&since=%s&until=%s&access_token=%s' % (limit,since,until,TOKEN)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {}
    headers = { 'Authorization':  BEAR}
    h = MyHTTPRedirectHandler()
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    data = urllib.urlencode(values)
    json_data = ""
    try:
        req = urllib2.build_opener(h)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()
        json_data = json.loads(the_page)
    except:
        print("Error reading data")
    return json_data



def signal_handler(signal, frame):
        sys.exit(0)


class LOG():
      def __init__(self,file='logfile'):
          self.file=file
      def Open(self,FILE=""):
          if FILE != "":
              self.file=FILE
          self.f=open(self.file,'w')
# Below...add your own stuff
      def SplitOpen(self,FILE):
          m=FILE.split('_')
          self.file="./result/parse."+m[1]+"."+m[-1].split('.')[0]
          self.Open()
      def Write(self,s):
          self.f.write(s+'\n')
      def Close(self):
          self.f.close()


log=LOG()




def Open(FILE):
    f=open(FILE)
    m=f.readlines()
    f.close()
    m=[i.strip().split() for i in m]
    return m




def main(N):
    writeMembers(members(limit=3000))
    if len(sys.argv) > 1: # You haven't fixed this
        return  # Take out return
        try:
            limit=int(sys.argv[1])
            k=getJson(limit=limit,since='2015-07-15',until='2015-07-31')
            parseJ(k)
        except _e:
            print(_e)
    else:
        limit=1000
#        T0=datetime.datetime(2016, 5, 28, 0, 0)
        T0=datetime.datetime(tokenf.START_YEAR, tokenf.START_MONTH, tokenf.START_DAY, 0, 0)
        while T0 < datetime.datetime.now()+datetime.timedelta(7):
            print(T0.strftime('%Y-%m-%d'))
            T1=T0+datetime.timedelta(7)
            k=getJson(limit=limit,since=T0.strftime('%Y-%m-%d'),until=T1.strftime('%Y-%m-%d'))
            parseJ(k)
            T0=T1

            




if __name__ == '__main__':
        signal.signal(signal.SIGINT, signal_handler)
        main(sys.argv)






        
