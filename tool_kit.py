# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pycurl
from StringIO import StringIO
import time
from stem import Signal
from stem.control import Controller
import os
import random

#-----------------------------------------------------------------------------#
#                          def of work_path                                   #
#-----------------------------------------------------------------------------#
path_log="loginit/"

#-----------------------------------------------------------------------------#
#                          create folder(s)                                   #
#-----------------------------------------------------------------------------#
def create_path() :
    print "Verifying internal paths", "\n"
    path_list = ["errors/", "log/", "loginit/"]    
    for i in path_list :        
        if os.path.exists(i) :
            pass
        else :
            print i, "... now Created"
            os.mkdir(i)
    print "\n"

#-----------------------------------------------------------------------------#
#                               dispatch                                      #
#-----------------------------------------------------------------------------#
def dispatch(textfilename, listename, ratio=100) :
    print "#-----------------------------------------------------------------#"
    print "dispatch links in sub_lists"
    compteur0 = 0
    fichier = open(textfilename, "w")
    list_init =[]
    nbr_lot = int(float(len(listename)) / float(ratio))
    if nbr_lot < float(len(listename)) / float(ratio) :
        nbr_total_lot = nbr_lot + 1
    else :
        nbr_total_lot = nbr_lot
    for x in range(len(listename)) :
        list0 = []
        for i in listename :
            compteur0 += 1
            if compteur0 > ratio :
                compteur0 = 0
                break
            else :
                list0.append(i)
                fichier.write(i + "\n")
                listename.remove(i)
        list_init.append(list0)
    compteur1 = 0
    list_list = []
    for z in list_init :
        compteur1 += 1
        if len(z) != 0 :
            list_list.append(z)
        else :
            pass
    print len(list_list), "ensembles(s) de listes traitees pour" , len(list_init), "liens "
    print "#-----------------------------------------------------------------#"
    print "\n"
    return list_list

#-----------------------------------------------------------------------------#
#                                 Curl                                        #
#-----------------------------------------------------------------------------#
def curl(url) :
    m = pycurl.CurlMulti()
    m.handles = []
    for i in url :
        c = pycurl.Curl()
        c.body = StringIO()
        c.http_code = -1
        m.handles.append(c)
        c.setopt(pycurl.URL, str(i))
        c.setopt(pycurl.WRITEFUNCTION, c.body.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.NOSIGNAL, 1)
        c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64) Ubuntu/12.04 Chromium/14.0.835.202')
        c.setopt(pycurl.HTTPHEADER, ['User-agent: %s' % 'Mozilla/5.0 (X11; Linux x86_64) Ubuntu/12.04 Chromium/14.0.835.202 Data Mining and Research'])
        #---------------------------------------------------------------------#
        #                    PROTECTION WITH TOR AND DNS :                    #
        #---------------------------------------------------------------------#
        #you must have TOR installed on your machine to be able to use DNS to 
        #get data without being banned by host server.
        
        #c.setopt(pycurl.PROXY, '127.0.0.1')
        #c.setopt(pycurl.PROXYPORT, 9050)
        #c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        #---------------------------------------------------------------------#
        #                          ...                                        #
        #---------------------------------------------------------------------#
        c.setopt(pycurl.REFERER, 'http://www.google.co.uk/') #http://www.google.co.in/
        m.add_handle(c)
    num_handles = len(m.handles)
    while 1 :
        ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM :
            break
    while num_handles :
        m.select(1.0)
        while 1 :
            ret, num_handles = m.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM :
                break
    for c in m.handles :
        c.close()
    m.close()
    return m.handles

#-----------------------------------------------------------------------------#
#                         GET IP ADRESS FROM WEBSITES                         #
#-----------------------------------------------------------------------------#
def read_ipadress(path_log) :
    ip_url = ["http://www.my-ip-address.net", "http://www.mon-ip.com",
              "http://www.adresseip.com", "http://my-ip.heroku.com",
              "http://www.whatsmyip.net", "http://www.geobytes.com/phpdemo.php",
              "http://checkip.dyndns.com", "http://www.myglobalip.com"]
    #if issue with those websites above you might consider some other in the list below or 
    #you could find your one.
    # http://www.myglobalip.com/
    # http://www.whereisip.net/
    # http://www.howtofindmyipaddress.com/
    # http://www.hostip.info/
    # http://www.ipchicken.com/
    # http://myip.dk/
    # http://www.showmyipaddress.com/
    # http://www.tracemyip.org/ 
    # http://www.myipnumber.com/
    # http://en.dnstools.ch/show-my-ip.html
    # http://ifconfig.me/
    # https://www.astrill.com/what-is-my-ip-address.php
    # http://www.cmyip.com/
    # http://ip-detect.net/
    # http://www.dslreports.com/whois
    # http://www.whatismybrowser.com/what-is-my-ip-address
    # http://www.showmemyip.com/
    # http://aboutmyip.com/AboutMyXApp/AboutMyIP.jsp
    # http://www.findmyip.org/
    # https://www.whatsmydns.net/whats-my-ip-address.html
    url = random.choice(ip_url)
    if url == "http://www.my-ip-address.net" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h2')[0].text
            s1 = s1.replace("IP Address :", "")
    elif url == "http://www.mon-ip.com" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('span', {'class' : 'clip'})[0].text        
    elif url == "http://www.adresseip.com" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h2', {'class' : 'title'})[0].text
            s1 = s1.replace("Votre Adresse IP est :", "")
    elif url == "http://www.whatsmyip.net" :
        print "url : ", url, "\n"    
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h1', {'class' : 'ip'})[0]
            s1 = s1.findAll('input')[0]['value']
    elif url == "http://my-ip.heroku.com" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.text        
    elif url == "http://www.geobytes.com/phpdemo.php" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('b')[0].text      
    elif url == "http://checkip.dyndns.com" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.text
            s1 = s1.replace("Current IP CheckCurrent IP Address: ", "")
    elif url == "http://www.myglobalip.com" :
        print "url : ", url, "\n"
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h3')
            s1 = s1[0].findAll('span', {'class' :'ip'})
            s1 = s1[0].text
    else :
        print "Problem"
    ip_adress = s1
    return ip_adress

#-----------------------------------------------------------------------------#
#                             New IP Adress                                   #
#-----------------------------------------------------------------------------#
#with thid and thanks to the stem module you can controle the change of your ip
#adress when this fonction bellow is called.
def change_ipadress(passphrase="yourTORpassword", sleep=1) :
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(passphrase)
        controller.signal(Signal.NEWNYM)  
    #we wait here but you can eventually skip this part or set it in place to
    #gain controle over time.
    time.sleep(sleep)
                
#-----------------------------------------------------------------------------#
#                          Tries to read the ip adress                        #
#-----------------------------------------------------------------------------#
def try_read_ipadress(path_log) :
    try :
        print read_ipadress(path_log)
    except :
        print "#------------------------------------#"
        print "1st time read_ipadress failed to launch"
        print "re start 1 read_ipadress"
        print "\n"
        try :
            print read_ipadress(path_log)
        except :
            print "#------------------------------------#"
            print "2nd time read_ipadress failed to launch"
            print "re start 2 read_ipadress"
            print "\n"   
            try :
                print read_ipadress(path_log)
            except :
                print "#------------------------------------#"
                print "3rd time read_ipadress failed to launch"
                print "re start 3 read_ipadress"
                print "\n"
                print read_ipadress(path_log) 
                
#-----------------------------------------------------------------------------#
#                          Re-new the ip adress                               #
#-----------------------------------------------------------------------------#
def oldnew_ipadress(path_log, ip_adress=read_ipadress(path_log)) :
    print "Old : "
    try_read_ipadress(path_log)
    change_ipadress()    
    print "New : "
    try_read_ipadress(path_log)
    print "\n"
#dev : securite aller chercher l adresse ip de retour sur un autre site

#-----------------------------------------------------------------------------#
#       Calculus of urls that remain to do in case of process shut down       #
#-----------------------------------------------------------------------------#
def url_todo(path_log) :
    todo = []
    done = []
    read_dispatch = open(path_log + "dispatch1.txt", "r").readlines()
    url_done = open(path_log + "url_done.txt", "r").readlines()
    for i in read_dispatch :
        a = i.replace("\n", "")
        todo.append(a)
    for i in url_done :
        b = i #.split(";")[1]
        done.append(b)
    url_todo = []
    for i in todo :
        if i in done :
            pass
        else :
            url_todo.append(i)
    print "len(url_todo) : ", len(url_todo)
    print "Restant a faire : "
    print "len(todo) - len(done) : ", len(todo) - len(done)
    url_todo_file = open(path_log + "url_todo.txt", "w")
    for i in url_todo :
        url_todo_file.write(i + "\n")
