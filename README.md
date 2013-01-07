Intro
=====

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

Invocation
==========

There are two modes: 

* ThunderBird+FiltaQuilla+imap_tagger
* Standalone

First mode will use "run file" function of FiltaQuilla invoking imap_tagger with config name (section name) and Message-id header contents. This mode doesn't use "subject" match string as Message ID has been already provided.

Second mode is "automatic" - it will search through the mailbox for Subject line matches first, then will attempt running regexp agains body of the message (that excludes headers etc.) and on successfull match - will apply provided tag (FLAG in IMAP parlance).

