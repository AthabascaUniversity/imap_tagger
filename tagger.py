"""
Usage: tagger.py [section [message-id ...]]
"""
import ConfigParser
import imaplib
import sys
import os
import re
# import argparse


def connect(server,user,passwd):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(user, passwd)
    return mail

def test_and_tag(mail,uid,re_filter,tag):
    print "====> ", uid,
    s_result,subj_struc = mail.uid('fetch',uid,'(BODY.PEEK[HEADER.FIELDS (SUBJECT)] FLAGS)')
    subj=subj_struc[0][1][:-4]
    # print subj_struc
    result,body = mail.uid('fetch',uid,'(BODY.PEEK[TEXT])')
    match=False
    # print subj
    for ll in body:
        for l in ll:
            # print l
            if re_filter.search(l):
                match=True
                # print l
                print tag, subj
                result,data=mail.uid('STORE',uid,'+FLAGS', '({tag})'.format(tag=tag))
                # result,data=mail.uid('STORE',uid,'-FLAGS', '(\Seen)')
                break
        if match:
            break
    if not match:
        print ""

    return match

if __name__ == '__main__':

    cp=ConfigParser.ConfigParser()
    cp.read(['tagger.cfg', os.path.expanduser('~/.tagger.cfg')])
    defaults=cp.defaults()

    if len(sys.argv)>1:
        section=sys.argv[1]
    else:
        section=defaults['default']

    server=cp.get(section,'host')
    username=cp.get(section,'username')
    passwd=cp.get(section,'password')
    folders=cp.get(section,'folders').split(',')
    subject=cp.get(section,'subject')
    exp=cp.get(section,'regexp')
    tag=cp.get(section,'tag')
    # print "Config: ",section
    # print "Tag: ",tag
    re_filter=re.compile(exp)

    mail=connect(server,username,passwd)
    # (code,items)=mail.list()
    # for item in items:
        # print item
    # Out: list of "folders" aka labels in gmail.
    for folder in folders:
        mail.select(folder) # connect to inbox.
        if len(sys.argv)>2:
            for mid in sys.argv[2:]:
                result,uids_list = mail.uid('search','(NOT DELETED HEADER Message-id "{mid}")'.format(mid=mid))
                uids=uids_list[0].split()
                for uid in uids:
                    # print uid
                    test_and_tag(mail,uid,re_filter,tag)
        else:
            result,uids_list = mail.uid('search','(NOT DELETED HEADER Subject "{subject}")'.format(subject=subject))
            # print uids
            uids=uids_list[0].split()
            for uid in uids:
                # print uid
                test_and_tag(mail,uid,re_filter,tag)
