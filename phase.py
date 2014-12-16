# -*- coding: utf-8 -*-

from data_crawl import function_2, function_3, function_4
from tool_kit import url_todo

def phase2(path_log) :
    try :
        function_2()
    except :
        print "#------------------------------------#"
        print "phase 2 : 1st time function_1 failed to launch, re start of function"
        print "\n"
        try :
            function_2()
        except :
            print "#------------------------------------#"
            print "phase 2 : 2nd time function_1 failed to launch, re start of function"
            print "\n"
            function_2()

def phase3(path_log) :
    function_3()

def phase4(path_log) :
    try :
        function_4()
    except :
        print "#------------------------------------#"
        print "phase 4 : 1st time function_1 failed to launch, re start of function"
        print "\n"
        url_todo(path_log)
        try :
            function_4()
        except :
            print "#------------------------------------#"
            print "phase 4 : 2nd time function_1 failed to launch, re start of function"
            print "\n"
            url_todo(path_log)
            function_4()
