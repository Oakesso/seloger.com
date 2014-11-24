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
#                               Developpments                                 #
#-----------------------------------------------------------------------------#

# 1 en cas d'interuption brusque du programme il doit etre capable de repartir 
#du meme endroit de lecture.

# 2 detection de tor on le lance si n'existe pas, sinon on ne fait rien.

# 3 barre de progression du processus.

#----- "ok done " ---- : gerer plusieurs sites pour recuperer l adress ip.

# 4 notification des erreurs de programme dans un fichier externe pour corriger.
# 5 recuperer les donnees grace la variable "url" pour completer les donnees 
#   et mettre en place mesure du temps de presence des annonces. 
# 6 recuperer les photos pour eliminer les meubles et reconsruire une surface 
#   vide afin de pouvoir se projeter dans l appartement.
# 7 ajouter mongodb
# 8 trouver un server web python/unix "Amazon, autre..."

# 9 randomiser les url lors du dispatch des url pour quelles soient shufflisees 
#dans le dispacth.

# 10 pour le redemarage du programme (chaque fois que cela est programme dans 
#les fonctions "phase_x()") mettre en place un systeme de verification que
#tor soit bien un processus existant sinon lancer le programme.

# 11 faire un processus qui au bout d un temps qu une boucle n est pas fini on 
#coupe le processus tor (ce qui provoque le redemarage du programme).

# 12 tester un changement aleatoire de user agent et httpheader de la fonction
#"curl()". Cela peut peut etre jouer sur la reconnaissance par le site (si 
#il identifie par cookies)

# 13 tester si le different nombre de url choisit dans la fonction "dispatch()"
#avec le "ratio" permet de jouer avec les limites mise par le site (niveau de
#donnees telechageable par le site pour un user identifie).

# site/ blog django / wordpress
#sujet d ecriture / tutoriel ce que je fais / passion le meilleur.
#trouver des applications utiles.
#voir les urls suivantes : 
#http://django-dynamic-scraper.readthedocs.org/en/latest/getting_started.html
#http://doc.scrapy.org/en/latest/intro/tutorial.html
#http://doc.scrapy.org/en/latest/intro/install.html#intro-install


#-----------------------------------------------------------------------------#
#                          creation des dosssiers                             #
#-----------------------------------------------------------------------------#

#cette fonction permet de verifier que les dossier dont on a besoin dans le 
#cadre du programme pour y ecrire des fichiers existent bien. Si ils n'existent 
#pas on le creer.

def create_path() :
    
    print "Verifying internal paths", "\n"
    
    #on met dans une lsite l ensemble des dossiers a verifier.
    
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

#il s agit du fichier permettant de transformer un paquet d url en plusieurs lot
#en fonction d un ratio, puis il est ainsi exploiter par un autre fichier pour
#eviter les goulots d etranglements en cas de traitement global de tout les
#fichier downloader par "CurlMulti".

#-----------------------------------------------------------------------------#

def dispatch(textfilename, listename, ratio=100) :

    print "#-----------------------------------------------------------------#"
    print "dispatch des liens en sous listes"
    compteur0 = 0

    #on ouvre le fichier texte "textfilename" pour y ecrire les urls.

    fichier = open(textfilename, "w")
    list_init =[]
    nbr_lot = int(float(len(listename)) / float(ratio))

    #on determine le nbre de lot dans la liste par une variable.

    if nbr_lot < float(len(listename)) / float(ratio) :
        nbr_total_lot = nbr_lot + 1
    else :
        nbr_total_lot = nbr_lot

    #on alimente une liste par des sous lots de liste de valeur ratio en nombre
    #d items.

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

                #list0 est la liste qui contient les elements i qui vient ce
                #dernier de sp4.lsit_init qui est la liste des urls a traiter.
                #list_init est la liste qui va contenir toutes les listes "list0".
                #dans la boucle précédente on enlève chaque element i qui
                #appartient deja a la liste "list_init" puis on relance le processus
                #jusqu'a la fin de la boucle.

        list_init.append(list0)

        #on charge list0 dans list_init a la fin de cette boucle.
        #on met une liste dans une autre liste.

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

#il s agit de la fonction "CurlMulti" qui recupere les objets de "url".
# "url" est une liste d'urls. si 1 url mettre dans une liste url = ["monurl"] a
#definir avant d'appliquer la fonction.
#ici on fait passer le telechargement des items par Curl via Tor afin que l'adresse
#ip utiliser ne soit pas spammer, par contre cela entraine un ralentissement reseau.

#-----------------------------------------------------------------------------#

def curl(url) :
    
#    print "Curl is waiting for data ... ", "\n"

    #phase initialisation des curl multi.

    m = pycurl.CurlMulti()
    m.handles = []
    
    for i in url :

        #on enleve au fur et a mesure les elements de la liste quand il arrive
        #puis sont utilisés.on travail sous pycurl maintenant pour debuter
        #la recolte de l'url et son stockage.
        #creation de l'objet Curl

        c = pycurl.Curl()

        #creation de l'objet qui stockera la page web avec StringIO

        c.body = StringIO()
        c.http_code = -1
        m.handles.append(c)

        #mise en place des option curl
        #on indique l'url a Curl

        c.setopt(pycurl.URL, str(i))
        c.setopt(pycurl.WRITEFUNCTION, c.body.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.NOSIGNAL, 1)
        c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64) Ubuntu/12.04 Chromium/14.0.835.202')
        c.setopt(pycurl.HTTPHEADER, ['User-agent: %s' % 'Mozilla/5.0 (X11; Linux x86_64) Ubuntu/12.04 Chromium/14.0.835.202 Data Mining and Research'])

        #---------------------------------------------------------------------#
        #                    PROTECTION AVEC TOR ET DNS :                     #
        #---------------------------------------------------------------------#
        
        #attention le port ci dessous est le numero 9150 et pas 9151
        
        c.setopt(pycurl.PROXY, '127.0.0.1')
        c.setopt(pycurl.PROXYPORT, 9050)
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)

        #---------------------------------------------------------------------#
        #                    Reprise de la suite ...                          #
        #---------------------------------------------------------------------#
        
        c.setopt(pycurl.REFERER, 'http://www.google.co.uk/') #http://www.google.co.in/
        m.add_handle(c)
    num_handles = len(m.handles)
    
    #mise en activité

    while 1 :
        ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM :
            break

    #prendre les données.

    while num_handles :
        m.select(1.0)
        while 1 :
            ret, num_handles = m.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM :
                break
            
#    print "Ok, Curl gets data"

    #fermer les handles.

    for c in m.handles :
        c.close()
    m.close()
    return m.handles

#-----------------------------------------------------------------------------#
#              Recuperation des donnees qui contient l ip adress              #
#-----------------------------------------------------------------------------#

def read_ipadress(path_log="loginit/") :
    
    #cette url permet d'acceder à l'ensemble de la page de départ du site
    #sur laquelle se trouve la majorité des liens qui pourront nous interesser
    #par la suite.

    #cette url permet d'acceder à l'ensemble de la page de départ du site
    #sur laquelle se trouve la majorité des liens qui pourront nous interesser
    #par la suite.

    ip_url = ["http://www.my-ip-address.net", "http://www.mon-ip.com",
              "http://www.adresseip.com", "http://my-ip.heroku.com",
              "http://www.whatsmyip.net", "http://www.geobytes.com/phpdemo.php",
              "http://checkip.dyndns.com", "http://www.myglobalip.com"]
              
    #autres sites a integrer voir fichier "tor_auto_renew_ipadress.py"

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

    #on utilise random afin de choisir au hasard un elements parmis la liste 
    #d url de "ip_url". On le met entre crochet car ensuite "curl" lit une url
    #ou serie d urls entre crochet (une liste)
    
    url = random.choice(ip_url)
    
    if url == "http://www.my-ip-address.net" :
        
        print "url : ", url,
        
        pool = curl([url])

        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
    
            s1 = soup1.findAll('h2')[0].text
            s1 = s1.replace("IP Address :", "")
            
    elif url == "http://www.mon-ip.com" :
        
        print "url : ", url,
            
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
    
            s1 = soup1.findAll('span', {'class' : 'clip'})[0].text        
            
    elif url == "http://www.adresseip.com" :
        
        print "url : ", url,
        
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
    
            s1 = soup1.findAll('h2', {'class' : 'title'})[0].text
            s1 = s1.replace("Votre Adresse IP est :", "")
           
    elif url == "http://www.whatsmyip.net" :
        
        print "url : ", url,     
        
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)

            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
    
            s1 = soup1.findAll('h1', {'class' : 'ip'})[0]
            s1 = s1.findAll('input')[0]['value']
            
    elif url == "http://my-ip.heroku.com" :
        
        print "url : ", url,
            
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
    
            #on obtient le texte directement depuis la page qui est sans 
            #structure.
    
            s1 = soup1.text        

    elif url == "http://www.geobytes.com/phpdemo.php" :
        
        print "url : ", url,
            
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
            
            #on obtient le texte directement depuis la page qui est sans 
            #structure.
    
            s1 = soup1.findAll('b')[0].text      

    elif url == "http://checkip.dyndns.com" :
        
        print "url : ", url,
            
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
            
            #on obtient le texte directement depuis la page qui est sans 
            #structure.
    
            s1 = soup1.text
            s1 = s1.replace("Current IP CheckCurrent IP Address: ", "")
            
    elif url == "http://www.myglobalip.com" :
        
        print "url : ", url,
            
        pool = curl([url])
        
        for c in pool :
            
            #on recupere les url qui n ont pas fonctionner lors du proccessus :
            
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #on recherche tous les liens du contenu dans le conteneur "li" 
            #dont la class = switch_style du css il y a d'autres liens dans 
            #les autres conteneur. on se place dans le css numero 1 "li" 
            #dont la class = "switch_style".
            
            #on obtient le texte directement depuis la page qui est sans 
            #structure.
    
            s1 = soup1.findAll('h3')
            s1 = s1[0].findAll('span', {'class' :'ip'})
            s1 = s1[0].text
                      
    else :
        print "Problem"
    
    #on retounrne la valeur de s1 qui contient le texte concernant l adresse ip
    #on pourra ainsi imprimer la valeur rendu par la fonction ailleurs dans le 
    #programme.
    
    ip_adress = s1
    
    return ip_adress

#-----------------------------------------------------------------------------#
#                             New IP Adress                                   #
#-----------------------------------------------------------------------------#

#permet grace au module stem "Signal" de changer en tor l'adresse ip 
#des que la fonction est appelee. 
    
def change_ipadress(passphrase="Femmes125", sleep=1) :

    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(passphrase)
        controller.signal(Signal.NEWNYM)  
    
    #on fait patienter une seconde
    
    time.sleep(sleep)
                
#-----------------------------------------------------------------------------#
#                          Try to read the ip adress                          #
#-----------------------------------------------------------------------------#

def try_read_ipadress() :
    
    try :
        print read_ipadress()
    except :

        #---------------------------------------------------------------------#
        #                    1er re lancement de read_ipadress                #
        #---------------------------------------------------------------------#
                
        print "1st time read_ipadress failed to launch"
        print "re start 1 read_ipadress"
        print "\n"
        
        try :
            print read_ipadress()
        except :

            #-----------------------------------------------------------------#
            #                   2eme re lancement de read_ipadress            #
            #-----------------------------------------------------------------#
        
            print "2nd time read_ipadress failed to launch"
            print "re start 2 read_ipadress"
            print "\n"   

            try :
                print read_ipadress()
            except :
    
                #-------------------------------------------------------------#
                #                   3eme re lancement de read_ipadress        #
                #-------------------------------------------------------------#
            
                print "3rd time read_ipadress failed to launch"
                print "re start 3 read_ipadress"
                print "\n"
                
                print read_ipadress()    
                                
#-----------------------------------------------------------------------------#
#                          Re-new the ip adress                               #
#-----------------------------------------------------------------------------#

#on creer une fonction unique qui ira chercher quelle est l adresse ip actuelle
#puis qui change l etat de tor pour renouveller l ip et enfin, va lire a nouveau
#l adress ip sur le meme site. 

def oldnew_ipadress(ip_adress=read_ipadress()) :
    
#    print "Changing ip address ... ",
        
    #nous renouvellons l adresse ip et on relance la fonction jusqu a deux fois 
    #en cas de necessite :
        
    #-------------------------------------------------------------------------#
    #                           partie 1 de oldnew_ipadress                   #
    #-------------------------------------------------------------------------# 
    
    #affichage de l adresse ip actuelle

    print "Old : "
    
    #on lance la fonction "try_read_ipadress()" qui tente par trois fois de
    #de lancer le programme si le lancement fait defaut.
    
    try_read_ipadress()

    #-------------------------------------------------------------------------#
    #                           partie 2 de oldnew_ipadress                   #
    #-------------------------------------------------------------------------# 
    
    #changement de l adress ip via thor. Il est a noter que l on pourrait se 
    #debarraser de la 1ere fois du redemarage de "read_ip()". Il a ete utiliser
    #au debut pour verifier le bon changement d adresse entre les deux etats de 
    #tor avant le lancement du signal et apres la nouvelle ip prise.
                
    change_ipadress()    
        
    #-------------------------------------------------------------------------#
    #                           partie 3 de oldnew_ipadress                   #
    #-------------------------------------------------------------------------#  
    
    #affichage de l adresse ip nouvelle.

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

#    #en generale le 1er fichier "backup_file1.txt" ne doit pas trop changer
#
#    backup_file1 = open(path_log + file_name, "r").readlines()
#    
#    url = []
#    
#    for i in range(len(backup_file1)) :
#        a = backup_file1[i].split(";")[3].strip()
#        url.append(a)
    
    #on dispatch les url en plus petits lots afin de les traiter au fur et a 
    #mesure et ne pas les traiter en lot entier sinon on perd en efficacite.
    
    url_liste = dispatch(path_log + "dispatch1.txt", url)
    
    #on lance la 1ere loop afin de parcourir la liste des urls qui ont ete 
    #dispatchee en petits groupe (pour des raisons de securite). 
    
    #on ouvre un fichier en ecriture afin d y sauver des donnees :
            
    backup_file2 = open(path_log + "backup_file2.txt", "w")
                                                       
    for url in url_liste :
        
        #cette url permet d'acceder à l'ensemble de la page de départ du site
        #sur laquelle se trouve la majorité des liens qui pourront nous interesser
        #par la suite.
    
        pool = curl(url)
        
        #nous renouvellons l adresse ip apres avoir telecharger des donnes
        #par curl:
    
        oldnew_ipadress()
             
        for c in pool :
           
            data = c.body.getvalue()
            
            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
    
            #on recherche tous les liens du contenu dans le conteneur "li" dont la class = switch_style du css
            #il y a d'autres liens dans les autres conteneur.
            #on se place dans le css numero 1 "li" dont la class = "switch_style"
    
            s1 = soup1.findAll('div', {'class' : 'content_infos othergroupsite'})
            s1 = s1[0].findAll('li')
            print "len(s1) : ", len(s1)        
            print "\n"
            
            som_nbr_annonce = 0
            
            som_list = []
            
            for i in range(len(s1)) : 
                
                url = s1[i].findAll('a')[0]['href']
                
                #on calcul le dernier element de la derniere partie separer par "/"
                #et contenant "immo-"
                
                len_url = len(url.split("/"))
                
                #on utilise len_url pour garder la partie ou le numero de departement est ecrit.
                
                len_departement = len(url.split("/")[len_url-4].split("-"))
                
                #on recupere ainsi le numero du departement en utilisant maintenant 
                #len_departement.
                departement = url.split("/")[len_url-4].split("-")[len_departement-1]
                
                #on recupere le type de bien1:
                    
                type_bien1 = url.split("/")[len_url-3].replace("bien-", "")
                
                #on recupere le nombre d annonce qui est un texte que l on recupere 
                #par la methode "string". 
                
                nbr_annonce = s1[i].findAll('b')[0].string
                
                #on change la valeur de nbr_annonce car parfois il prend la valeur "None"
                #qui ne peutre etre traduit en numeric / float pour le comptage dans la suite.
                
                if nbr_annonce != None :
                    pass
                else :
                    nbr_annonce = 0                
                    
                som_nbr_annonce = float(som_nbr_annonce) + float(nbr_annonce)
                som_list.append(float(som_nbr_annonce))
                
                #on recupere le type_bien2 a la aide du titre.
                
                nbr_piece = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "").replace(type_bien1, "").strip().split(" ")[2]
                
                if nbr_piece == "studio" :
                    nbr_piece = '1'
                else :
                    pass
    
                #on recupere le quartier a la aide du titre.
                
                type_transaction = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "").replace(type_bien1, "").strip().split(" ")[0]
                
                print i, str(som_nbr_annonce), departement, str(nbr_annonce), type_transaction, type_bien1, nbr_piece, url
                
                #on ecrit les donnees dans le fichier ".txt".
                
                backup_file2.write(departement + ";" + str(nbr_annonce)+ ";" + type_transaction + ";" + type_bien1 + ";" + nbr_piece + ";" + url + ";")
                
                backup_file2.write("\n")
    
    #        break
                
    #on ferme le fichier :
        
    backup_file2.close()
    print "\n"
    
#-----------------------------------------------------------------------------#
#           Recuperation du nombre de pages et url a parcourir                #
#-----------------------------------------------------------------------------#

def function_3(path_log="loginit/") :
    
    #ici pour chacune des urls on multiplie par 50 (35 maintenant) les pages existantes 
    #qui ont la meme racine mais change en fin de chaine. 
    #on fait cela car il est trop long d'avoir une méthode pour calculer 
    #justement le nombre de page a parcourir.
    #Ici 50 sera le nombre maximum de fonction creer (elles vont de l url initiale
    #jusqu'a l url initiale + la chaine "?ANNONCEpg=" + les nombre de 2 a 51).
    
    #Attention dans cette fonction le nombre de page qui est recolte semble varier 
    #a chaque DL du programme par exemple on trouve entre deux tentative pour 
    #l url "http://www.seloger.com/immobilier/achat/immo-paris-16eme-75/bien-appartement/type-2-pieces/"
    #une 1ere fois "580 items" puis "579 items" alors qu avec une connection 
    #browser on voit le nombre a "588 items"

    backup_file = open(path_log + "backup_file2.txt", "r").readlines()
    print "len(backup_file) : ", len(backup_file)
    print "\n"

    urls_parcours = open(path_log + "urls_parcours.txt", "w")
    
    urls_list = []
    
    for i in range(len(backup_file)) :
        
#        print "i : ", i, backup_file[i]
        
        url = backup_file[i].split(";")[5]
        nbr = float(backup_file[i].split(";")[1])
        
        nbr_page_init = nbr/10
        partie_entiere = int(str(nbr_page_init).split(".")[0])
        apres_dec = int(str(nbr_page_init).split(".")[1])
        
        #dans le cas ou on a "0" on a la page de l url d origine a parcourir
        if apres_dec == 0 :
            nbr_page = partie_entiere
        #dans le cas ou on a "> 0" on a la page de l url d origine a parcourir, 
        #puis la suivante.
        elif apres_dec > 0 :
            nbr_page = partie_entiere + 1
        #dans le cas ou on a "> 0" on a la page de l url d origine a parcourir, 
        #puis les suivantes.
        else :
            print "Probleme nbr_page"                
        
        print "nbr : ", nbr
        print "url : ", url
        print nbr, nbr_page_init, "nous donne :", nbr_page, "page(s)", "\n"
        
        #deux condition se presentent alors :
        #soit on a une page de 10 ou moins d items soit plus d une page 
        #de 10 item ou moins. 
        
        #On tente le coup si on a "0" comme valeur de "nbr_page" car defois c'est 
        #le cas. On prend en charge le "0" ainsi car juste avant quand une url est
        #indiquee on considere que cela veut dire qu il y a une page au moins 
        #existante.
        
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
                #on construit les autres urls et on les ecrits 
                #dans le fichier:                        
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

    #parametrage de la date a afficher par la suite :

#    d = str(time.strftime('%d-%m-%y_%Hh%Mmin%Ssec',time.localtime()))
    d2 = str(time.strftime('%d/%m/%y %H:%M:%S',time.localtime()))    
    d3 = str(time.strftime('%d-%m-%y',time.localtime()))

    #on lit puis on parcours le fichier qui contient les urls a
    #parcourir avec le programme.

    backup_file1 = open(path_log + file_name, "r").readlines()
    
    #initialisation de la liste qui va contenir les urls lue dans le fichier 
    #ci dessus. 
    
    url = [] 
    
    #on parcours le fichier avec cette loop pour ecrire les urls dans notre 
    #liste "url".
    
    for i in range(len(backup_file1)) :
        a = backup_file1[i].split(";")[0].strip()
        url.append(a)
    
    #on dispatch les url en plus petits lots afin de les traiter au fur et a 
    #mesure et ne pas les traiter en lot entier sinon on perd en efficacite.
    
    url_liste = dispatch(path_log + "dispatch1.txt", url)
    
    #le fichier dans lequel on indique les paquets d url traites.
    
    url_done = open(path_log + "url_done.txt", "w")
         
    #on ecrit le chemin dans lequel nous souhaitons ecrire nos log de donnees,
    #ce dossier se situe dans le repertoire d execution du fichier :
    
    path_logout = "log/"
    
    #on lance la 1ere loop afin de parcourir la liste des urls qui ont ete 
    #dispatchee en petits groupe (pour des raisons de securite). 

    compteur = 0
                                                       
    for url in url_liste :
        
        compteur += 1
        
        print compteur, "/", len(url_liste)        
        
        #on ecrit les url dans "url_done" afin de garder une trace d ou on en 
        #etait dans le processus.
        
        for i in range(len(url)) :
            url_done.write(url[i] + "\n")
        
        #cette url permet d'acceder à l'ensemble de la page de départ du site
        #sur laquelle se trouve la majorité des liens qui pourront nous interesser
        #par la suite.
    
        pool = curl(url)
        
        #nous renouvellons l adresse ip:
            
        oldnew_ipadress()
                
        #on initialise un compteur dont on se servira plus loin afin de mesurer
        #le nbre d iterations realisees.
                
        compteur1 = 0
        
        #on parcours le pool d image des pages qui ont ete traitee en ramener 
        #par la fonction "curl()".
                           
        for c in pool :
            
            compteur1 += 1
            
            print compteur1, "/", len(pool)
            
            data = c.body.getvalue()

            #utilisation de BeautifulSoup
            #on met dans BeautifulSoup le contenu de la page web
    
            soup1 = BeautifulSoup(data)
            
            #parametrage de la date a afficher par la suite :

            d = str(time.strftime('%d-%m-%y_%Hh%Mmin%Ssec',time.localtime()))
    
            #on recherche tous les liens du contenu dans le conteneur "li" dont 
            #la class = switch_style du css, il y a d'autres liens dans les 
            #autres conteneur. on se place dans le css numero 1 "li" dont la 
            #class = "switch_style".
            
            l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                    
            dico = {'TYPE_TRANSACTION' : l0, 'NOMBRE_PHOTOS' : l1 , 
                    'NOMBRE_PIECE' : l2, 'NOMBRE_M2' : l3, 'ETAGE' : l4, 
                    'BALCON' : l5, 'CUISINE' : l6, 'AUTRE' : l7,
                    'CHAMBRE(S)' : l8, 'MEUBLE' : l9, 'TYPE_CHAUFFAGE' : l10, 
                    'LOCALISATION' : l11, 'PROXIMITE' : l12, 'PRIX' : l13, 
                    'CHARGE' : l14, 'NOM_AGENCE' : l15, 'URL' : l16, 
                    'EXTRACTION_DATE' : l17}
                   
            #-----------------------------------------------------------------#
                            
            #RECHERCHE DU MOT LOCATIONS / VENTES / INVESTISSEMENT / VIAGER :
            
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
                
                #on ne peut pas ajouter la variable ici sinon elle ne sera qu une fois
                #dans le dico alors qu on la veut autant de fois qu il y a de ligne d 
                #individus. On aurait pu mettre la ligne suivante :
                
                #l0.append(transaction_type) (voir ci apres).

                           
            #-----------------------------------------------------------------#
            
            #RECHERCHE NOMBRE DE PHOTOS / PUIS AJOUT DE VARIABLE TRANSACTION_TYPE : 
            
            s1 = soup1.findAll('div', {'class' : 'annonce__visuel__pictogrammes'})
            
            for i in range(len(s1)) :
                               
                #il s avere que des fois l indication d une photo ne existe pas
                #alors on passe et on ecrit "pas de photos".
                
                if s1[i].findAll('a', {'class' : 'annonce__visuel__picto picto__photo'}) == [] :
                    nbr_photo = 0
                else :
                    nbr_photo = s1[i].findAll('a', {'class' : 'annonce__visuel__picto picto__photo'})
                    nbr_photo = nbr_photo[0]['title']
                    nbr_photo = nbr_photo.replace(" photos", "")
                    nbr_photo = int(nbr_photo)
                
                l1.append(nbr_photo)
                
                #on utilise ici la variable de la partie de parogramme avec s0 et l0
                #(voir ci dessus). on ajoute donc la variable ici.
                
                l0.append(transaction_type)
             
            #-----------------------------------------------------------------#
            
            #RECHERCHE DETAILS 1 :
            
            s2 = soup1.findAll('div', {'class' : 'annonce__detail'})
            
            for i in range(len(s2)) :
                
                details1 = s2[i].findAll('span', {'class' : 'annone__detail__param'})[0].text
                details1 = details1.replace("\xe8", "e")
                details1 = details1.replace("m\xb2", "m2")
                details1 = details1.replace("\xe9", "e")
                details1 = details1.split(",")
           
                #on initialise lea variables et on pourra ainsi les modifie par 
                #la suite si on rencontre une valeur differente.

                nbr_piece = "NA"
                nbr_m2 = "NA"
                etage = "NA"
                balcon = "NA"
                cuisine = "NA"
                autre = "NA"
                chambre = "NA"
                meuble = "NA"
                chauffage = "NA"
                
                #avec la loop on rencontre chacune des valeurs possibles et si 
                #elle est presente alors on modifie la valeur qui est a "NA".
                
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
                
#                print i, details1, "||", nbr_piece, nbr_m2, etage, balcon, cuisine, autre
                
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
            
            #RECHERCHE DETAILS LOCALISATION : 

            s3 = soup1.findAll('span', {'class' : 'annone__detail__localisation'})
            
            for i in range(len(s3)) :

                details2 = s3[i].findAll('span', {'class' : 'annone__detail__param'})[0].text
                details2 = details2.replace(" (Paris)", "")
                details2 = details2.replace(" ()", "")
                
                l11.append(details2)    

            #-----------------------------------------------------------------#
            
            #RECHERCHE DETAILS PROXIMITE : 

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
            
            #RECHERCHE PRIX & DETAIL CHARGE : 
            
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
                
                #on recupere le prix en nombre :
                #parfois la valeur est un string au lieu d un nombre.
                #parfois se presente le signe "Â".
                try :
                    l13.append(float(detailsx[0].replace(",", ".").replace("Â", "")))
                except :
                    l13.append(str(detailsx[0]))
                #on recupere les charges comprises ou non comprises.
                
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
                    
                    #on rajoute .strip() ici car sinon des cellule vide sont 
                    #ecrite a la place de la valeur "NA".
                    
                    l14.append(detailsx[1].strip())

                
            #-----------------------------------------------------------------#
            
            #RECHERCHE NOM AGENCE : 

            s6 = soup1.findAll('div', {'class' : 'annonce__agence'})
            
            for i in range(len(s6)) :
                
                details6 = s6[i].findAll('span', {'class' : 'annone__detail__nom'})
                
                if details6 != [] :
                    details6 = details6[0].text
                else :
                    details6 = "NA"

                l15.append(details6)                    

            #-----------------------------------------------------------------#
            
            #RECHERCHE URL : 

            s7 = soup1.findAll('div', {'class' : 'annonce__detail'})
            
            for i in range(len(s7)) :

                url_cible = s7[i].findAll('a', {'class' : 'annone__detail__title annonce__link'})
                url_cible = url_cible[0]['href']
                url_cible = url_cible.split("?")[0]

                l16.append(url_cible)                    

                #-----------------------------------#
            
                #ECRITURE DE LA DATE COMME VARIABLE : 

                l17.append(d2)

                #-----------------------------------#
                                                                
            #-----------------------------------------------------------------# 
            
            #PHASE D ECRITURE DU FICHIER :
               
            if dico['CUISINE'] == [] : 
                pass
            else : 
                
                #on utilise pandas ici porupouvoir ecrire 

                try :
                    
                    df = pd.DataFrame(dico) 
                    
                    #df.to_excel('foo.xlsx', sheet_name='Sheet1')
                    
                    #"a" pour ajout au lieu de "w" en re ecriture.
                    #on ecrit tous les log generer par cette boucle dans 
                    #un autre dossier car elles sont nombreuses. "path_logout"
                    
#                    df.to_csv(path_logout + '%s.txt' %(d), mode="a", header=True) 
                    
                    #on ecrit aussi dans un autre fichier en parallele (backup) mais
                    #avec les donnees qui s accumule dans le fichier au fur et a 
                    #mesure que les loop passent. "a" pour ajout de donnees au fichier.
                    #on enleve aussi les titres des colonnes.
                    
                    df.to_csv(path_logout + 'seloger_%s.txt' %(d3), mode="a", header=False)                
                    
                    print compteur, df
                    print "\n"
                    
                except :

                    print "ValueError : ", ValueError
                    print "dico : ", dico
                    
                    #on ecrit dans "path_log" le fichier :
                        
                    log_dico = open(path_log + "log_dico.txt", "a")
                    
                    for i in dico : 
                        print "len(dico[i])  : ", str(len(dico[i])), str(i), str(dico[i]) 
                        log_dico.write(str(len(dico[i])) + ";" + str(i) + ";" + str(dico[i]))
                        
                    log_dico.close()
        
        print "\n"
        
#            break
#   
#        break

#-----------------------------------------------------------------------------#
#             Calcul des url restants a faire en cas d interruption           #
#-----------------------------------------------------------------------------#

def url_todo(path_log="loginit/") :

    todo = []
    done = []
    
    #on lit le fichier a partir duquel les urls ont ete traite (ce qu il y avait 
    #a faire) et on lit aussi les urls qui on ete deja traite (ce qui a ete fait
    #enfin ce qui est passe dans la fonction "curl").

    #-------------------------------------------------------------------------#
    #              Lecture des fichiers et nettoyage des fichiers             #
    #-------------------------------------------------------------------------#
    
    read_dispatch = open(path_log + "dispatch1.txt", "r").readlines()
    url_done = open(path_log + "url_done.txt", "r").readlines()

    #on lit le 1er fichier :
        
    for i in read_dispatch :
        a = i.replace("\n", "")
        todo.append(a)
    
    #on lit le 2eme fichier : 
    
    for i in url_done :
        b = i #.split(";")[1]
        done.append(b)

    #-------------------------------------------------------------------------#
    #              Calcul de ce qui reste a faire comme urls                  #
    #-------------------------------------------------------------------------#
        
    #on determine la ou s est arreter le fichier dans son patrcours des urls.
    #on verifie les urls qui ont ete reconnu appartiennent a notre fichier "url
    #_done" sinon ceux qui n y appartiennent pas sont alors ceux a executer. 
    #on mets ces fichiers restant a traiter dans la liste "url_todo".
    
    url_todo = []
    
    for i in todo :
        if i in done :
            #si url de todo deja effectue
            #car dans "done" on passe.
            pass
        else :
            url_todo.append(i)
    
    print "len(url_todo) : ", len(url_todo)
    print "Restant a faire : "
    print "len(todo) - len(done) : ", len(todo) - len(done)

    #-------------------------------------------------------------------------#
    #              Ecriture des urls dans un fichier texte                    #
    #-------------------------------------------------------------------------#
            
    #on ecrit les urls dans le fichier .txt "url_todo.txt". On met bien ici "w"
    #afin que pour chaque phase ou la fonction est relancee le fichier soit re 
    #ecrit et non pas qu il y ait d ajouts de donnee. On veut que repartir d un
    #fichier "neuf". 
    
    url_todo_file = open(path_log + "url_todo.txt", "w")
    
    for i in url_todo :
        url_todo_file.write(i + "\n")

#-----------------------------------------------------------------------------#
#                                 Phase I                                     #
#-----------------------------------------------------------------------------#

#gestion du lancement de la fonction 1, on relance la fonction jusqu'a 2 fois 
#si jamais elle echoue. 2 fois devrait suffir car il y a un renouvellement de 
#l adress ip a chaque fois.

#def phase1(path_log="loginit/") :
#    
#    print "#------------------------------------#"
#    print "#           PHASE I                  #"
#    print "#------------------------------------#"
#    print "\n"
#    
#    #on lance la fonction et on recupere list_p1.
#
#    try :
#        function_1(path_log="loginit/")
#    except :
#
#        #---------------------------------------------------------------------#
#        #                    1er re lancement de la fonction 1                #
#        #---------------------------------------------------------------------#    
#
#        print "1st time function_1 failed to launch"
#        print "re start function_1"
#        print "\n"
#        try :
#            function_1(path_log="loginit/")
#        except :
#
#            #-----------------------------------------------------------------#
#            #                   2eme re lancement de la fonction 1            #
#            #-----------------------------------------------------------------#
#
#            print "2nd time function_1 failed to launch"
#            print "re start function_1"
#            print "\n"
#            function_1(path_log="loginit/")

#-----------------------------------------------------------------------------#
#                                 Phase II                                    #
#-----------------------------------------------------------------------------#

#gestion du lancement de la fonction 1, on relance la fonction jusqu'a 2 fois 
#si jamais elle echoue. 2 fois devrait suffir car il y a un renouvellement de 
#l adress ip a chaque fois.

def phase2() :
    
    print "#------------------------------------#"
    print "#           PHASE II                 #"
    print "#------------------------------------#"
    print "\n"

    #on lance la fonction et on recupere list_p1.
    
    try :
        function_2(path_log="loginit/")
    except :

        #---------------------------------------------------------------------#
        #                    1er re lancement de la fonction 1                #
        #---------------------------------------------------------------------#
        
        print "1st time function_1 failed to launch"
        print "re start function_1"
        print "\n"
        try :
            function_2(path_log="loginit/")
        except :

            #-----------------------------------------------------------------#
            #                   2eme re lancement de la fonction 1            #
            #-----------------------------------------------------------------#
        
            print "2nd time function_1 failed to launch"
            print "re start function_1"
            print "\n"
            function_2(path_log="loginit/")

#-----------------------------------------------------------------------------#
#                                 Phase III                                   #
#-----------------------------------------------------------------------------#

#on ne relance pas cette fonction car il s agit d'une ecriture sans intervention
#de donnees externe.

def phase3() :
    
    print "#------------------------------------#"
    print "#           PHASE III                #"
    print "#------------------------------------#"
    print "\n"
    
    function_3(path_log="loginit/")


#-----------------------------------------------------------------------------#
#                                  Phase IV                                   #
#-----------------------------------------------------------------------------#

#on ne relance pas cette fonction car il s agit d'une ecriture sans intervention
#de donnees externe.

def phase4() :
    
    print "#------------------------------------#"
    print "#           PHASE IV                 #"
    print "#------------------------------------#"
    print "\n"
    
    try :
        function_4(path_log="loginit/")
    except :

        #---------------------------------------------------------------------#
        #                    1er re lancement de la fonction 1                #
        #---------------------------------------------------------------------#
                
        print "1st time function_1 failed to launch"
        print "re start function_1"
        print "\n"

        url_todo()
        try :
            function_4(path_log="loginit/", file_name="url_todo.txt")
        except :

            #-----------------------------------------------------------------#
            #                   2eme re lancement de la fonction 1            #
            #-----------------------------------------------------------------#
        
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













