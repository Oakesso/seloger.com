# -*- coding: utf-8 -*-

from data_crawl import function_2, function_3, function_4
from tool_kit import url_todo

def phase2(path_log) :
    print "#------------------------------------#"
    print "#           PHASE II                 #"
    print "#------------------------------------#"
    print "\n"
    try :
        function_2()
    except :
        print "#------------------------------------#"
        print "1st time function_1 failed to launch"
        print "re start function_1"
        print "\n"
        try :
            function_2()
        except :
            print "#------------------------------------#"
            print "2nd time function_1 failed to launch"
            print "re start function_1"
            print "\n"
            function_2()

def phase3(path_log) :
    print "#------------------------------------#"
    print "#           PHASE III                #"
    print "#------------------------------------#"
    print "\n"
    function_3()

def phase4(path_log) :
    print "#------------------------------------#"
    print "#           PHASE IV                 #"
    print "#------------------------------------#"
    print "\n"
    try :
        function_4()
        print "#------------------------------------#"
        print "1st time function_1 failed to launch"
        print "re start function_1"
        print "\n"
        url_todo(path_log)
        try :
            function_4()
        except :
            print "#------------------------------------#"
            print "2nd time function_1 failed to launch"
            print "re start function_1"
            print "\n"
            url_todo(path_log)
            function_4()
