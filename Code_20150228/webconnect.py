# -*- coding: utf-8 -*-
"""
Spyder Editor

Code réalisé par Theodore T. Stanton
Pour toute question, mail à theodorestanton@gmail.com
Meetup Paris Coders Beginners le 28/02/2015
"""
# essai d'une autre librairie qui fonctionne avec le navigateur par défaut
# import webbrowser
# webbrowser.open('www.leboncoin.fr')

import urllib2
#les trois instructions ci apres ont été copiés collées d'un tuto sur stackoverflow
response = urllib2.urlopen('http://finance.yahoo.com/q?s=AAPL')
headers = response.info()
data = response.read()

''' data contient le code source intégral de la page web du bon coin '''

# data est un objet de type string (instruction vérifiable avec type(data))
# cherchons maintenant à récupérer le cours de l'action AAPl (Apple) en direct
# le marché étant fermé, nous servons que le cours de cloture aujourd'hui est de 128.46
# Vérifions que cette info est dispo en clair dans le code

# réponse oui c est le cas on le retrouve après deux instrutions dans le code source
# la première fait référence à time_rtq_ticker qui doit signifier quote en real time
# suivi de span id = yfs_184_aapl qui doit être le code interne du site pour l'action AAPL
# on peut donc décomposer le string data pour récupérer cette info
# peut on récupérer l'horaire du cours pour incrémenter une base de données?
# oui aussi <span class="time_rtq"> <span id="yfs_t53_aapl">Feb 27, 4:00PM EST</span></span>

def cours_RT (codesourceYahooFinance) :
    rt_quote = codesourceYahooFinance.split('<span>')
    '''print "rt quote : "
    print "----------"
    print rt_quote[5]'''
    #parcoursons mon rt_quote pour trouver la table de rt_quote
    j= len(rt_quote)
    #print str(type(j))
    #print 'la taille du tableau est :', str(j)
    while j<>0 :
        #on cherche time_rtq_ticker ou time_rtq
        #print ("on est dans la loop, niveau", str(j))
        n=rt_quote[j-1].find('time_rtq_ticker')
        if n <> -1 : #-1 est le retour oar défaut de find si aucun résultat
            #on a trouvé la cotation en temps réel
            #print "trouve !!", rt_quote[j-1]
            #stockons la valeur à partir du string
            #rt_quote_level2=rt_quote[j-1].split('<span class="time_rtq_ticker">')
            #print rt_quote_level2
            # on triche et on récupère les 30 valeurs derrières l'index c'est moche mais efficace
            rt_quote_level2=rt_quote[j-1][n+17:n+65] #+17 nous place derrière le span, 65 nous met large
            # risque dans le code car on ne connait pas la taille du cours ici en centaine mais p ê en millions
            # print str(rt_quote_level2) 
            '''good ca fonctionne je vois le cours'''
            # je cherche le symbole > qui se positionne avant le cours
            k= rt_quote_level2.find('>')
            l= rt_quote_level2.find('<',k)
            res1=rt_quote_level2[k+1:l]
            
        m=rt_quote[j-1].find('time_rtq">') #je complète pour pas avoir le même résultat que précédemment
        if m <> -1 : #-1 est le retour oar défaut de find si aucun résultat
            #pareil mais on récupère l'horaire de la cotation
            rt_quote_level3=rt_quote[j-1][m+17:m+65] #+17 nous place derrière le span, 65 nous met large
            #print str(rt_quote_level3)
            k= rt_quote_level3.find('>')
            l= rt_quote_level3.find('<',k)
            res2=rt_quote_level3[k+1:l]
            #print str(res2)
        j=j-1   
    return [res1,res2]
    
''' Code Basique pour exploiter les résultats '''    
x=cours_RT(data)    
print "le cours est de %s, au %s" % (x[0],x[1])
#print "programme terminé !"

''' Points de départs pour la fois suivante :
-------------------------------------------------------------------------------------------------------------
1/ Transformer la date en un format exploitable pour historiser en base de données
2/ Adapterle code à une liste évolutive pour récupérer les 40 valeurs du CAC 40 
3/ Prévoir une fréquence de sauvegarde (minute par minute, 15 min par 15 min)
4/ Créér un fichier executable qui tourne soit sur un site soit en local sur une machine (genre windows script)
5/ Créer un rendu graphique (évolution d'un cours ou plusieurs cours, tableau de variation)
6/ Point maths : comparer l'évolution des différents actions avec l'indice CAC 40
7/ Anonymiser les requetes web au départ pour ne pas être tracké par son IP
'''
