imap_tagger
===========

IMAP tagger - tag you mail on IMAP server based on regexp in cases when server/clients don't support regexp filters

My initial motivation was to close the gap in Thunderbird functionality with IMAP resources:

you can't have a regexp filter for those.

This script is fairly simple and has some assumptions hardwired, however using .cfg file you 
should be able to tweak it to your liking before you get into script customization itself.

You can use one config file for many different connections/configurations: just use [sections]
to aggregate them. 

Sample config file::


    [DEFAULT]
    default=myfavorite

    [myfavorite]
    ; Account auth information:
    host=imap.some.com
    username=me@imap.com
    password=MyPasswordAtImapDotCom

    ; comma-separated list of folders to search
    folders=INBOX,SomeFolder

    ; Simple string-match filter to run for subject lines
    ; when invoked with no message-id
    subject=SimpleString
    ; RegExp to check against message body
    regexp=My.Reg.Exp.*goes.*here
    ; Tag (FLAG) to apply to message on RegExp match
    tag=MyTag

    [other_config]
    ...
    [yet_another_config]
    ...

