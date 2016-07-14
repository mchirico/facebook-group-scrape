#!/usr/bin/env python2
import pandas as pd
import numpy as np
import datetime
import glob

from shutil import copy

import errno
import os


import random
random.seed(datetime.datetime.now())

import tokenf
TMPDIR=tokenf.TMPDIR
DATADIR=tokenf.DATADIR


def Mkdir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass





def emptyData():
    if os.path.isdir(TMPDIR+'/msg.csv'):
        return
    if os.path.isdir(DATADIR+'/post.csv'):
        return    

    m = pd.read_csv(TMPDIR+"/msg.csv",
                names=[0, 1, 2, 3, 4, 5, 6],
                dtype='str', quotechar='"',header=None)

    m.drop_duplicates(inplace=True)


    c = pd.read_csv(TMPDIR+"/comments.csv",
                names=[0, 1, 2, 3, 4, 5, 6],
                dtype='str', quotechar='"',header=None)


    c.drop_duplicates(inplace=True)


    l = pd.read_csv(TMPDIR+"/likes.csv",
                names=[0, 1, 2, 3, 4],
                dtype='str', quotechar='"',header=None)                                      

    l.drop_duplicates(inplace=True)


    mem = pd.read_csv(TMPDIR+"/members.csv",
                names=[0, 1, 2],
                dtype='str', quotechar='"',header=None)


    mem['gid']=tokenf.FACEBOOK_GROUP

    mem.drop_duplicates(inplace=True)


    ll=l[l[1]=='x']
    like_count=ll[[0,1]].groupby([0]).count().reset_index()
    like_count.columns=[0,'like']
    like_count.head()

    m=pd.merge(m, like_count, how='left',left_on=[0], right_on=[0])

    # Column changes
    m.columns = ['pid','id','name','timeStamp','shares','url','msg','likes']
    l.columns = ['pid','cid','response','id','name']
    c.columns = ['pid','cid','timeStamp','id','name','rid','msg']
    mem.columns= ['id','name','url','gid']

    m['gid']=m['pid'].apply(lambda x: x.split('_')[0])
    l['gid']=l['pid'].apply(lambda x: x.split('_')[0])
    c['gid']=c['pid'].apply(lambda x: x.split('_')[0])



    m['timeStamp']=pd.DatetimeIndex(m.timeStamp)
    c['timeStamp']=pd.DatetimeIndex(c.timeStamp)
    m['timeStamp']= m.timeStamp.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    c['timeStamp']= c.timeStamp.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))

    mem.drop_duplicates(inplace=True)

    m.drop_duplicates(subset=['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes'],inplace=True)
    c.drop_duplicates(subset=['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg'],inplace=True)
    l.drop_duplicates(subset=['gid','pid', 'cid', 'response', 'id', 'name'],inplace=True)


    m.timeStamp=pd.DatetimeIndex(m.timeStamp)
    m.sort_values(by='timeStamp',ascending=False)
    m.drop_duplicates(subset=['gid','pid', 'id', 'name', 'timeStamp',  'url', 'msg'],inplace=True,keep='last')


    m[['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes']].to_csv(TMPDIR+"/post.csv",index=False,header=True)
    c[['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg']].to_csv(TMPDIR+"/comment.csv",index=False,header=True)
    l[['gid','pid', 'cid', 'response', 'id', 'name']].to_csv(TMPDIR+"/like.csv",index=False,header=True)

    mem[['gid', 'id', 'name', 'url']].to_csv(TMPDIR+"/member.csv",index=False,header=True)

# No header
    m[['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes']].to_csv(TMPDIR+"/postNH.csv",index=False,header=False)
    l[['gid','pid', 'cid', 'response', 'id', 'name']].to_csv(TMPDIR+"/likeNH.csv",index=False,header=False)
    c[['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg']].to_csv(TMPDIR+"/commentNH.csv",index=False,header=False)
    mem[['gid', 'id', 'name', 'url']].to_csv(TMPDIR+"/memberNH.csv",index=False,header=False)

    # Copy everything
    for file in glob.glob(TMPDIR+'/*.csv'):
        copy(file,DATADIR)









def dataExists():    

    m = pd.read_csv(DATADIR+"/msg.csv",
                names=[0, 1, 2, 3, 4, 5, 6],
                dtype='str', quotechar='"',header=None)


    m_delta = pd.read_csv(TMPDIR+"/msg.csv",
                names=[0, 1, 2, 3, 4, 5, 6],
                dtype='str', quotechar='"',header=None)   
                      
    m=pd.concat([m,m_delta])
    m.drop_duplicates(inplace=True)



    c = pd.read_csv(DATADIR+"/comments.csv",
                names=[0, 1, 2, 3, 4, 5, 6],
                dtype='str', quotechar='"',header=None)


    c_delta = pd.read_csv(TMPDIR+"/comments.csv",
                names=[0, 1, 2, 3, 4, 5, 6],
                dtype='str', quotechar='"',header=None)

    c=pd.concat([c,c_delta])
    c.drop_duplicates(inplace=True)



    l = pd.read_csv(DATADIR+"/likes.csv",
                names=[0, 1, 2, 3, 4],
                dtype='str', quotechar='"',header=None)
    
    l_delta = pd.read_csv(TMPDIR+"/likes.csv",
                names=[0, 1, 2, 3, 4],
                dtype='str', quotechar='"',header=None)

    l=pd.concat([l,l_delta])
    l.drop_duplicates(inplace=True)

    mem = pd.read_csv(DATADIR+"/members.csv",
                names=[0, 1, 2],
                dtype='str', quotechar='"',header=None)


    mem['gid']=tokenf.FACEBOOK_GROUP

    mem_delta = pd.read_csv(TMPDIR+"/members.csv",
                names=[0, 1, 2],
                dtype='str', quotechar='"',header=None)                                                                                                                            

    mem_delta['gid']=tokenf.FACEBOOK_GROUP
    mem=pd.concat([mem,mem_delta])
    mem.drop_duplicates(inplace=True)


    ll=l[l[1]=='x']
    like_count=ll[[0,1]].groupby([0]).count().reset_index()
    like_count.columns=[0,'like']
    like_count.head()

    m=pd.merge(m, like_count, how='left',left_on=[0], right_on=[0])



    m.columns = ['pid','id','name','timeStamp','shares','url','msg','likes']
    l.columns = ['pid','cid','response','id','name']
    c.columns = ['pid','cid','timeStamp','id','name','rid','msg']
    mem.columns= ['id','name','url','gid']

    m['gid']=m['pid'].apply(lambda x: x.split('_')[0])
    l['gid']=l['pid'].apply(lambda x: x.split('_')[0])
    c['gid']=c['pid'].apply(lambda x: x.split('_')[0])



    m['timeStamp']=pd.DatetimeIndex(m.timeStamp)
    c['timeStamp']=pd.DatetimeIndex(c.timeStamp)
    m['timeStamp']= m.timeStamp.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    c['timeStamp']= c.timeStamp.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))



    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    #['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes']
    m_delta = pd.read_csv(DATADIR+"/post.csv",
                      header=0,names=['gid','pid', 'id','name', 'timeStamp', 'shares', 'url', 'msg', 'likes'],
                      dtype={'gid':str,'pid':str,'id':str,'name':str,'timeStamp':datetime.datetime,'shares':str,
                             'url':str,'msg':str,'likes':str},
                                     parse_dates=['timeStamp'],date_parser=dateparse)
                      
    m=pd.concat([m,m_delta])
    m.drop_duplicates(inplace=True)


    l_delta = pd.read_csv(TMPDIR+"/like.csv",
                      header=0,names=['gid','pid','cid','response', 'id','name'],
                      dtype={'gid':str,'pid':str,'cid':str,'response':str,'id':str,'name':str})


    l=pd.concat([l,l_delta])
    l.drop_duplicates(inplace=True)


    c_delta = pd.read_csv(TMPDIR+"/comment.csv",
                      header=0,names=['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg'],
                      dtype={'gid':str,'pid':str,'cid':str,'timeStamp':datetime.datetime,'id':str,
                             'name':str,'rid':str,'msg':str},
                                     parse_dates=['timeStamp'],date_parser=dateparse)
                      

    c=pd.concat([c,c_delta])
    c.drop_duplicates(inplace=True)

    mem_delta = pd.read_csv(TMPDIR+"/member.csv",
                      header=0,names=['gid','id', 'name', 'url'],
                      dtype={'gid':str,'id':str,'name':str,'url':str})

                        
    mem=pd.concat([mem,mem_delta])
    mem.drop_duplicates(inplace=True)




    m.drop_duplicates(subset=['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes'],inplace=True)
    c.drop_duplicates(subset=['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg'],inplace=True)
    l.drop_duplicates(subset=['gid','pid', 'cid', 'response', 'id', 'name'],inplace=True)


    m.timeStamp=pd.DatetimeIndex(m.timeStamp)
    m.sort_values(by='timeStamp',ascending=False)
    m.drop_duplicates(subset=['gid','pid', 'id', 'name', 'timeStamp',  'url', 'msg'],inplace=True,keep='last')





    m[['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes']].to_csv(DATADIR+"/post.csv",index=False,header=True)
    c[['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg']].to_csv(DATADIR+"/comment.csv",index=False,header=True)
    l[['gid','pid', 'cid', 'response', 'id', 'name']].to_csv(DATADIR+"/like.csv",index=False,header=True)

    mem[['gid', 'id', 'name', 'url']].to_csv(DATADIR+"/member.csv",index=False,header=True)


    m[['gid','pid', 'id', 'name', 'timeStamp', 'shares', 'url', 'msg','likes']].to_csv(DATADIR+"/postNH.csv",index=False,header=False)
    l[['gid','pid', 'cid', 'response', 'id', 'name']].to_csv(DATADIR+"/likeNH.csv",index=False,header=False)
    c[['gid','pid', 'cid', 'timeStamp', 'id', 'name', 'rid', 'msg']].to_csv(DATADIR+"/commentNH.csv",index=False,header=False)
    mem[['gid', 'id', 'name', 'url']].to_csv(DATADIR+"/memberNH.csv",index=False,header=False)




def process():    
    if not os.path.isdir(DATADIR):
        Mkdir(DATADIR)
    emptyData()
    dataExists()


if __name__ == '__main__':
        process()    
