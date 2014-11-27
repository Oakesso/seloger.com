# -*- coding: utf-8 -*-


#-----------------------------------------------------------------------------#
#                            Import Librairies                                #
#-----------------------------------------------------------------------------#
from BeautifulSoup import BeautifulSoup
import pycurl
from StringIO import StringIO
import time
from stem import Signal
from stem.control import Controller
import pandas as pd
import os
import random

#-----------------------------------------------------------------------------#
#                          creation des dosssiers                             #
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
    print "dispatch des liens en sous listes"
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
#              Recuperation des donnees qui contient l ip adress              #
#-----------------------------------------------------------------------------#
def read_ipadress(path_log="loginit/") :
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
        print "url : ", url,
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h2')[0].text
            s1 = s1.replace("IP Address :", "")
    elif url == "http://www.mon-ip.com" :
        print "url : ", url,
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('span', {'class' : 'clip'})[0].text        
    elif url == "http://www.adresseip.com" :
        print "url : ", url,
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h2', {'class' : 'title'})[0].text
            s1 = s1.replace("Votre Adresse IP est :", "")
    elif url == "http://www.whatsmyip.net" :
        print "url : ", url,     
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('h1', {'class' : 'ip'})[0]
            s1 = s1.findAll('input')[0]['value']
    elif url == "http://my-ip.heroku.com" :
        print "url : ", url,
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.text        
    elif url == "http://www.geobytes.com/phpdemo.php" :
        print "url : ", url,
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('b')[0].text      
    elif url == "http://checkip.dyndns.com" :
        print "url : ", url,
        pool = curl([url])
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.text
            s1 = s1.replace("Current IP CheckCurrent IP Address: ", "")
    elif url == "http://www.myglobalip.com" :
        print "url : ", url,
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
def change_ipadress(passphrase="Femmes125", sleep=1) :
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(passphrase)
        controller.signal(Signal.NEWNYM)  
    #we wait here but you can eventually skip this part or set it in place to
    #gain controle over time.
    time.sleep(sleep)
                
#-----------------------------------------------------------------------------#
#                          Tries to read the ip adress                        #
#-----------------------------------------------------------------------------#
def try_read_ipadress() :
    try :
        print read_ipadress()
    except :
        #---------------------------------------------------------------------#
        #                    first launch of read_ipadress                    #
        #---------------------------------------------------------------------#
        print "1st time read_ipadress failed to launch"
        print "re start 1 read_ipadress"
        print "\n"
        try :
            print read_ipadress()
        except :
            #-----------------------------------------------------------------#
            #               second launch of read_ipadress                    #
            #-----------------------------------------------------------------#
            print "2nd time read_ipadress failed to launch"
            print "re start 2 read_ipadress"
            print "\n"   
            try :
                print read_ipadress()
            except :
                #-------------------------------------------------------------#
                #                   third launch of read_ipadress             #
                #-------------------------------------------------------------#
                print "3rd time read_ipadress failed to launch"
                print "re start 3 read_ipadress"
                print "\n"
                print read_ipadress()    
#-----------------------------------------------------------------------------#
#                          Re-new the ip adress                               #
#-----------------------------------------------------------------------------#
def oldnew_ipadress(ip_adress=read_ipadress()) :
    print "Old : "
    try_read_ipadress()
    change_ipadress()    
    print "New : "
    try_read_ipadress()
    print "\n"
#dev : securite aller chercher l adresse ip de retour sur un autre site
    
#-----------------------------------------------------------------------------#
#        Recuperation des urls pour chacunes pages qui contient               # 
#                      les vers les urls des villes.                          #
#-----------------------------------------------------------------------------#

#def function_1(path_log="loginit/") :
#
#    #on lance la fonction create_path avant afin de verifier si tous les 
#    #dossier necessaire a l execution du programme existent sinon on les 
#    #crees.
#
#    create_path()    
#    
#    #cette url permet d'acceder à l'ensemble de la page de départ du site
#    #sur laquelle se trouve la majorité des liens qui pourront nous interesser
#    #par la suite.
#
#    url = ["http://www.seloger.com/immobilier/tout/immo-paris-75/"]
#
#    pool = curl(url)
#
#    #nous renouvellons l adresse ip:
#        
#    oldnew_ipadress() 
#    
#    #on ouvre un fichier en ecriture afin d y sauver des donnees :
#        
#    backup_file1 = open(path_log + "backup_file1.txt", "w")
#    
#    for c in pool :
#        
#        #on recupere les url qui n ont pas fonctionner lors du proccessus :
#                
#        data = c.body.getvalue()
#        
#        #utilisation de BeautifulSoup
#        #on met dans BeautifulSoup le contenu de la page web
#
#        soup1 = BeautifulSoup(data)
#        
#        #on recherche tous les liens du contenu dans le conteneur "li" 
#        #dont la class = switch_style du css il y a d'autres liens dans 
#        #les autres conteneur. on se place dans le css numero 1 "li" 
#        #dont la class = "switch_style".
#
#        s1 = soup1.findAll('div', {'class' : 'content_infos'})
#        s1 = s1[1].findAll('li')
#        print "len(s1) : ", len(s1)
#        print "\n"
#        
#        for i in range(len(s1)) : 
#            
#            url = s1[i].findAll('a')[0]['href']
#            
#            #on calcul le dernier element de la derniere partie separer par "/"
#            #et contenant "immo-"
#            
#            len_url = len(url.split("/"))
#            
#            #on utilise len_url pour garder la partie ou le numero de 
#            #departement est ecrit.
#            
#            len_departement = len(url.split("/")[len_url-2].split("-"))
#            
#            #on recupere ainsi le numero du departement en utilisant maintenant 
#            #len_departement.
#            
#            departement = url.split("/")[len_url-2].split("-")[len_departement-1]
#            
#            #on recupere le nombre d annonce qui est un texte que l on recupere 
#            #par la methode "string".
#            
#            nbr_annonce = s1[i].findAll('b')[0].string
#            
#            #on recupere le quartier a la aide du titre.
#            
#            quartier_niv1 = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "")
#
#            print i, departement, nbr_annonce, quartier_niv1, url
#            backup_file1.write(departement + ";" + nbr_annonce + ";" + quartier_niv1 + ";" + url + ";")
#            backup_file1.write("\n")
#            
##            break
#            
#    #on ferme le fichier :
#        
#    backup_file1.close()
#    print "\n"
              
#-----------------------------------------------------------------------------#
#        Recuperation des urls des annonces pour chacun des liens             #
#                            de types differents                              #
#-----------------------------------------------------------------------------#
def function_2(path_log="loginit/", file_name="backup_file1.txt") :
    create_path()
    url = ["http://www.seloger.com/immobilier/tout/immo-paris-1er-75/", 
           "http://www.seloger.com/immobilier/tout/immo-paris-2eme-75/", 
           "http://www.seloger.com/immobilier/tout/immo-paris-3eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-4eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-5eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-6eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-7eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-8eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-9eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-10eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-11eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-12eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-13eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-14eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-15eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-16eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-17eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-18eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-19eme-75/",
           "http://www.seloger.com/immobilier/tout/immo-paris-20eme-75/"]    
    url_liste = dispatch(path_log + "dispatch1.txt", url)
    backup_file2 = open(path_log + "backup_file2.txt", "w")
    for url in url_liste :
        pool = curl(url)
        oldnew_ipadress()
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('div', {'class' : 'content_infos othergroupsite'})
            s1 = s1[0].findAll('li')
            print "len(s1) : ", len(s1)        
            print "\n"
            som_nbr_annonce = 0
            som_list = []
            for i in range(len(s1)) : 
                url = s1[i].findAll('a')[0]['href']
                len_url = len(url.split("/"))
                len_departement = len(url.split("/")[len_url-4].split("-"))
                departement = url.split("/")[len_url-4].split("-")[len_departement-1]
                type_bien1 = url.split("/")[len_url-3].replace("bien-", "")
                nbr_annonce = s1[i].findAll('b')[0].string
                if nbr_annonce != None :
                    pass
                else :
                    nbr_annonce = 0                
                som_nbr_annonce = float(som_nbr_annonce) + float(nbr_annonce)
                som_list.append(float(som_nbr_annonce))
                nbr_piece = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "").replace(type_bien1, "").strip().split(" ")[2]
                if nbr_piece == "studio" :
                    nbr_piece = '1'
                else :
                    pass
                type_transaction = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "").replace(type_bien1, "").strip().split(" ")[0]
                print i, str(som_nbr_annonce), departement, str(nbr_annonce), type_transaction, type_bien1, nbr_piece, url
                backup_file2.write(departement + ";" + str(nbr_annonce)+ ";" + type_transaction + ";" + type_bien1 + ";" + nbr_piece + ";" + url + ";")
                backup_file2.write("\n")
    backup_file2.close()
    print "\n"
    
#-----------------------------------------------------------------------------#
#           Recuperation du nombre de pages et url a parcourir                #
#-----------------------------------------------------------------------------#
def function_3(path_log="loginit/") :
    backup_file = open(path_log + "backup_file2.txt", "r").readlines()
    print "len(backup_file) : ", len(backup_file)
    print "\n"
    urls_parcours = open(path_log + "urls_parcours.txt", "w")
    urls_list = []
    for i in range(len(backup_file)) :
        url = backup_file[i].split(";")[5]
        nbr = float(backup_file[i].split(";")[1])
        nbr_page_init = nbr/10
        partie_entiere = int(str(nbr_page_init).split(".")[0])
        apres_dec = int(str(nbr_page_init).split(".")[1])
        if apres_dec == 0 :
            nbr_page = partie_entiere
        elif apres_dec > 0 :
            nbr_page = partie_entiere + 1
        else :
            print "Probleme nbr_page"                
        print "nbr : ", nbr
        print "url : ", url
        print nbr, nbr_page_init, "nous donne :", nbr_page, "page(s)", "\n"
        if nbr_page == 1 or nbr_page == 0 :
            if nbr_page == 0 :
                print "Attention prise en charge du cas '0' page releve : ", "\n"
            else :
                b = url
                urls_list.append(b)
                urls_parcours.write(b + ";" + "\n")
                print b
        elif nbr_page == 2 :
            b = url
            c = url + "?ANNONCEpg=2"               
            urls_list.append(b)
            urls_list.append(c)
            urls_parcours.write(b + ";" + "\n")
            urls_parcours.write(c + ";" + "\n")
            print c
            print b
        elif nbr_page > 2 :
            for j in range(2, nbr_page) :                    
                b =  url + "?ANNONCEpg=%s" %(str(j))
                urls_list.append(b)
                urls_parcours.write(b + ";" + "\n")
                print b
        else :
            print "Problem nbr_page re construction"
    print "len(urls_list) : ", len(urls_list)
            
#-----------------------------------------------------------------------------#
#        Recuperation des urls des annonces pour chacun des liens             #
#-----------------------------------------------------------------------------#
def function_4(path_log="loginit/", file_name="urls_parcours.txt") :
#    d = str(time.strftime('%d-%m-%y_%Hh%Mmin%Ssec',time.localtime()))
    d2 = str(time.strftime('%d/%m/%y %H:%M:%S',time.localtime()))    
    d3 = str(time.strftime('%d-%m-%y',time.localtime()))
    backup_file1 = open(path_log + file_name, "r").readlines()
    url = [] 
    for i in range(len(backup_file1)) :
        a = backup_file1[i].split(";")[0].strip()
        url.append(a)
    url_liste = dispatch(path_log + "dispatch1.txt", url)
    url_done = open(path_log + "url_done.txt", "w")
    path_logout = "log/"
    compteur = 0
    for url in url_liste :
        compteur += 1
        print compteur, "/", len(url_liste)        
        for i in range(len(url)) :
            url_done.write(url[i] + "\n")
        pool = curl(url)
        oldnew_ipadress()
        compteur1 = 0
        for c in pool :
            compteur1 += 1
            print compteur1, "/", len(pool)
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            d = str(time.strftime('%d-%m-%y_%Hh%Mmin%Ssec',time.localtime()))
            l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
            dico = {'TYPE_TRANSACTION' : l0, 'NOMBRE_PHOTOS' : l1 , 
                    'NOMBRE_PIECE' : l2, 'NOMBRE_M2' : l3, 'ETAGE' : l4, 
                    'BALCON' : l5, 'CUISINE' : l6, 'AUTRE' : l7,
                    'CHAMBRE(S)' : l8, 'MEUBLE' : l9, 'TYPE_CHAUFFAGE' : l10, 
                    'LOCALISATION' : l11, 'PROXIMITE' : l12, 'PRIX' : l13, 
                    'CHARGE' : l14, 'NOM_AGENCE' : l15, 'URL' : l16, 
                    'EXTRACTION_DATE' : l17}
            #-----------------------------------------------------------------#
            #HERE LOOKING FOR WORDS LOCATIONS / VENTES / INVESTISSEMENT / VIAGER :
            s0 = soup1.findAll('div', {'class' : 'main'})
            for i in range(len(s0)) :
                if s0[i].findAll('span', {'class' : 'title_recherche'}) == [] :
                    transaction_type = "NA"
                else :
                    transaction_type = s0[i].findAll('span', {'class' : 'title_recherche'})
                    transaction_type = transaction_type[0].text
                    if "locations" in transaction_type :                        
                        #on re ecrit notre variable :
                        transaction_type = "LOCATION"
                    elif "ventes" in transaction_type :
                        transaction_type = "ACHAT"
                    elif "investissement" in transaction_type :
                        transaction_type = "INVESTISSEMENT"
                    elif "viager" in transaction_type :
                        transaction_type = "VIAGER"
                    else :
                        pass
            #-----------------------------------------------------------------#
            #RECHERCHE NOMBRE DE PHOTOS / PUIS AJOUT DE VARIABLE TRANSACTION_TYPE : 
            s1 = soup1.findAll('div', {'class' : 'annonce__visuel__pictogrammes'})
            for i in range(len(s1)) :
                if s1[i].findAll('a', {'class' : 'annonce__visuel__picto picto__photo'}) == [] :
                    nbr_photo = 0
                else :
                    nbr_photo = s1[i].findAll('a', {'class' : 'annonce__visuel__picto picto__photo'})
                    nbr_photo = nbr_photo[0]['title']
                    nbr_photo = nbr_photo.replace(" photos", "")
                    nbr_photo = int(nbr_photo)
                l1.append(nbr_photo)
                l0.append(transaction_type)
            #-----------------------------------------------------------------#
            s2 = soup1.findAll('div', {'class' : 'annonce__detail'})
            for i in range(len(s2)) :
                details1 = s2[i].findAll('span', {'class' : 'annone__detail__param'})[0].text
                details1 = details1.replace("\xe8", "e")
                details1 = details1.replace("m\xb2", "m2")
                details1 = details1.replace("\xe9", "e")
                details1 = details1.split(",")
                nbr_piece = "NA"
                nbr_m2 = "NA"
                etage = "NA"
                balcon = "NA"
                cuisine = "NA"
                autre = "NA"
                chambre = "NA"
                meuble = "NA"
                chauffage = "NA"
                for j in details1 :
                    if "Piece" in j :
                        if nbr_piece == "NA" :
                            nbr_piece = j.replace(" Piece", "").replace("s", "").strip()
                        else : 
                            pass
                    if "m2" in j :
                        if nbr_m2 == "NA" :
                            nbr_m2 = j.replace(" m2", "").strip()
                        else : 
                            pass
                    if "Etage" in j :
                        if etage == "NA" :
                            etage = j.replace(" Etage", "").strip()
                        else : 
                            pass
                    if "Balcon" in j :
                        if balcon == "NA" :
                            balcon = j.replace(" Balcon", "").strip()
                            balcon = j.replace("s", "").strip()
                        else : 
                            pass
                    if "cuisine" in j :
                        if cuisine == "NA" :
                            cuisine = j.replace(" cuisine", "").strip()
                        else : 
                            pass
                    if "Chambre" in j :
                        if chambre == "NA" :
                            chambre = j.replace(" Chambre", "")
                            chambre = chambre.replace("s", "").strip()
                        else :
                            pass
                    if "Meuble" in j :
                        if meuble == "NA" :
                            meuble = "YES"
                        else :
                            pass
                    if "chauffage" in j :
                        if chauffage == "NA" :
                            chauffage = j.replace("chauffage ", "")
                            chauffage = j.replace(" radiateur", "")
                        else :
                            pass
                    if "Piece" not in j and "m2" not in j and "Etage" not in j \
                    and "Balcon" not in j and "cuisine" not in j and "Chambre" not in j \
                    and "Meuble" not in j and "chauffage" not in j :
                        autre = j.strip()
                    else : 
                        pass
                l2.append(nbr_piece)
                l3.append(nbr_m2)
                l4.append(etage)
                l5.append(balcon)
                l6.append(cuisine)
                l7.append(autre)
                l8.append(chambre)
                l9.append(meuble)
                l10.append(chauffage)   
            #-----------------------------------------------------------------#
            #LOCATION : 
            s3 = soup1.findAll('span', {'class' : 'annone__detail__localisation'})
            for i in range(len(s3)) :
                details2 = s3[i].findAll('span', {'class' : 'annone__detail__param'})[0].text
                details2 = details2.replace(" (Paris)", "")
                details2 = details2.replace(" ()", "")
                l11.append(details2)    
            #-----------------------------------------------------------------#
            #NEAR LOCATION : 
            s4 = soup1.findAll('div', {'class' : 'annonce__detail'})
            for i in range(len(s4)) :
                details3 = s4[i].findAll('span', {'class' : 'annone__detail__proximite'})
                if details3 != [] :
                    details3 = details3[0].text
                    details3 = details3.replace("&#201;", "E")
                    details3 = details3.replace("&#233;", "e")
                    details3 = details3.replace("&#234;", "e")
                    details3 = details3.replace("&#235;", "e")
                    details3 = details3.replace("&#226;", "a")
                    details3 = details3.replace("&#244;", "o")
                    details3 = details3.replace("&quot", "")
                    details3 = details3.replace("&#206;", "")
                    details3 = details3.replace("&#231;", "c")
                    details3 = details3.replace("M&#176;", "Metro ")
                    details3 = details3.replace("Metro ", "")
                    details3 = details3.replace("Metro", "")
                    details3 = details3.replace("&#39;", "'")
                    details3 = details3.replace("&amp;", "et")
                    details3 = details3.replace("&#232;", "e")
                    details3 = details3.replace("/", ",")
                    details3 = details3.replace(": ", "")
                    details3 = details3.replace("metro", "") 
                    details3 = details3.replace("&#224;", "a")
                    details3 = details3.replace("&#238;", "i")
                    details3 = details3.replace("&#239;", "i")                    
                    details3 = details3.replace("Centre ville,", "")
                    details3 = details3.replace("ecole,", "")
                    details3 = details3.replace("commerces,", "")
                    details3 = details3.replace("bus,", "")
                    details3 = details3.replace("*", "")
                else :
                    details3 = "NA"
                proximite = details3
                l12.append(proximite)
            #-----------------------------------------------------------------#
            #PRICE AND DETAILS OF ADDITIVE PRICE CHARGEMENT : 
            s5 = soup1.findAll('div', {'class' : 'annonce__agence'})
            for i in range(len(s5)) :
                details4 = s5[i].findAll('span', {'class' : 'annonce__agence__prix annonce__nologo'})
                details5 = s5[i].findAll('span', {'class' : 'annonce__agence__prix '})
                if details4 != [] :
                    details4 = details4[0].text
                    details4 = details4.replace("\xa0", "")
                    details4 = details4.replace("\x80", "")
                    details4 = details4.split(" ")
                else :
                    details4 = 0
                if details5 != [] :
                    details5 = details5[0].text
                    details5 = details5.replace("\xa0", "")
                    details5 = details5.replace("\x80", "")                   
                    details5 = details5.split(" ")
                else :
                    details5 = 0
                if details4 == 0 :
                    detailsx = details5 
                elif details5 == 0 :
                    detailsx = details4
                try :
                    l13.append(float(detailsx[0].replace(",", ".").replace("Â", "")))
                except :
                    l13.append(str(detailsx[0]))
                if "FAI" in detailsx[1] :
                    new = detailsx[1].replace("FAI", "")
                    #parfois la valeur est un string au lieu d un nombre.
                    try :
                        l14.append(float(new))
                    except :
                        l14.append(new)
                elif "+" in detailsx[1] :
                    new = detailsx[1].replace("+", "")
                    l14.append(new)
                else :
                    l14.append(detailsx[1].strip())
            #-----------------------------------------------------------------#
            #REAL ESTATE AGENCY NAME : 
            s6 = soup1.findAll('div', {'class' : 'annonce__agence'})
            for i in range(len(s6)) :
                details6 = s6[i].findAll('span', {'class' : 'annone__detail__nom'})
                if details6 != [] :
                    details6 = details6[0].text
                else :
                    details6 = "NA"
                l15.append(details6)                    
            #-----------------------------------------------------------------#
            #GET THE URL TOO JUST IN CASE : 
            s7 = soup1.findAll('div', {'class' : 'annonce__detail'})
            for i in range(len(s7)) :
                url_cible = s7[i].findAll('a', {'class' : 'annone__detail__title annonce__link'})
                url_cible = url_cible[0]['href']
                url_cible = url_cible.split("?")[0]
                l16.append(url_cible)                    
                #-----------------------------------#
                #DATE : 
                l17.append(d2)
            #-----------------------------------------------------------------# 
            #WRITE THE FILE :
            if dico['CUISINE'] == [] : 
                pass
            else : 
                try :
                    df = pd.DataFrame(dico) 
                    df.to_csv(path_logout + 'seloger_%s.txt' %(d3), mode="a", header=False)                
                    print compteur, df
                    print "\n"
                except :
                    print "ValueError : ", ValueError
                    print "dico : ", dico
                    log_dico = open(path_log + "log_dico.txt", "a")
                    for i in dico : 
                        print "len(dico[i])  : ", str(len(dico[i])), str(i), str(dico[i]) 
                        log_dico.write(str(len(dico[i])) + ";" + str(i) + ";" + str(dico[i]))
                    log_dico.close()
        print "\n"

#-----------------------------------------------------------------------------#
#       Calculus of urls that remain to do in case of process shut down       #
#-----------------------------------------------------------------------------#
def url_todo(path_log="loginit/") :
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

def phase2() :
    print "#------------------------------------#"
    print "#           PHASE II                 #"
    print "#------------------------------------#"
    print "\n"
    try :
        function_2(path_log="loginit/")
    except :
        print "1st time function_1 failed to launch"
        print "re start function_1"
        print "\n"
        try :
            function_2(path_log="loginit/")
        except :
            print "2nd time function_1 failed to launch"
            print "re start function_1"
            print "\n"
            function_2(path_log="loginit/")

def phase3() :
    print "#------------------------------------#"
    print "#           PHASE III                #"
    print "#------------------------------------#"
    print "\n"
    function_3(path_log="loginit/")

def phase4() :
    print "#------------------------------------#"
    print "#           PHASE IV                 #"
    print "#------------------------------------#"
    print "\n"
    try :
        function_4(path_log="loginit/")
    except :
        print "1st time function_1 failed to launch"
        print "re start function_1"
        print "\n"
        url_todo()
        try :
            function_4(path_log="loginit/", file_name="url_todo.txt")
        except :
            print "2nd time function_1 failed to launch"
            print "re start function_1"
            print "\n"
            url_todo()
            function_4(path_log="loginit/", file_name="url_todo.txt")
            
#-----------------------------------------------------------------------------#
#                               MAIN DEVELOPMENT                              #
#-----------------------------------------------------------------------------#       
if __name__ == "__main__" :
         
#    phase1()
    phase2()
    phase3()
    phase4() 
    print "Finished"
        
#-----------------------------------------------------------------------------#
#                                   THE END                                   #
#-----------------------------------------------------------------------------#













