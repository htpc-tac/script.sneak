'''
Created on 10.02.2011

@author: htpc-tac
'''
__scriptID__ = "script.sneak"

import xbmc,xbmcaddon,xbmcgui
import sys
import os
import traceback
from urllib import quote_plus

def runAction( mode = "0" , resolution = "0" ,year_limit = "1900", rating_limit = "R"):

        xbmc.log( "[script.sneak] - Value handed over for mode: %s" % mode, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for resolution: %s" % resolution, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for year_limit: %s" % year_limit, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for rating_limit: %s" % rating_limit, xbmc.LOGNOTICE )
            
        xbmc.executebuiltin( "Playlist.Clear" )
        vplaylist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        vplaylist.clear()
        
        # Ratings set
        if rating_limit== "PG-13":
            rating_sql = "AND movie.c12  like '%%G%%' OR movie.c12 like '%%12%%' OR movie.c12 like '%%FSK 6%%' OR movie.c12 = 'Rated '"
        elif rating_limit == "PG":
            rating_sql = "AND movie.c12  like '%%PG%%' OR movie.c12 like '%%Rated G%%' OR movie.c12 like '%%FSK 6%%' OR movie.c12 = 'Rated '"
        elif rating_limit == "G":
            rating_sql = "AND movie.c12  like '%%Rated G%%' OR movie.c12 = 'Rated '"
        else:
            rating_sql = ""
        
            
        #Resolution set    
        if resolution == "0":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, movie WHERE movie.idFile = movieview.idFile AND movieview.playcount ISNULL AND movieview.c07 >= '%s' %s ORDER BY RANDOM() LIMIT 1" % (year_limit, rating_sql)
            
        elif resolution == "1":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, streamdetails, movie WHERE streamdetails.idFile = movieview.idFile AND movie.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 576 AND movieview.c07 >= '%s' ORDER BY RANDOM() LIMIT 1" % year_limit
           
        elif resolution == "2":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, streamdetails, movie WHERE streamdetails.idFile = movieview.idFile AND movie.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 720 AND movieview.c07 >= '%s' ORDER BY RANDOM() LIMIT 1" % year_limit
            
        
        xbmc.log( "[script.sneak] - SQL Statement: %s" % sql, xbmc.LOGNOTICE )
        
        try:
            movie_title, movie_path, movie_filename, dummy  = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
            
        except:
            xbmc.log( "[script.sneak] - SQL failed: " , xbmc.LOGNOTICE )
            movie_title ="" 
            movie_path ="" 
            movie_filename =""
           
            
        
        #log sql result:
                    
        xbmc.log( "[script.sneak] - Movie Title: %s" % movie_title, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Movie Path: %s" % movie_path, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Movie Filename: %s" % movie_filename, xbmc.LOGNOTICE )
        #better format
        # ja needed for second sql call where <field> is missing sometimes?
        ja = 0
        ja = movie_title.find("<field>")
        
        xbmc.log( "[script.sneak] - Find: %s" % ja, xbmc.LOGNOTICE )
        if ja !=-1:
            dummy, movie_title = movie_title.split( "<field>" )
            dummy, movie_path = movie_path.split( "<field>" )
            dummy, movie_filename= movie_filename.split( "<field>" )
            
        #log sql result:
        xbmc.log( "[script.sneak] - Movie Title: %s" % movie_title, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Movie Path: %s" % movie_path, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Movie Filename: %s" % movie_filename, xbmc.LOGNOTICE )
        
        try:
            if mode == 1:
                #call cinema experience:
            
                xbmc.executebuiltin("RunScript(script.cinema.experience,command<li>movie_title=%s)" % ( movie_title, ))
            
            else:
                #play without cinema experience
            
                play_file = movie_path + movie_filename
                xbmc.log( "[script.sneak] - Movie String: %s" % play_file, xbmc.LOGNOTICE )
                movie_full_path = os.path.join(movie_path, movie_filename).replace("\\\\" , "\\")
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                listitem = xbmcgui.ListItem(movie_title, )
                listitem.setInfo('video', {'Title': movie_title,})
                playlist.add(url=movie_full_path, listitem=listitem, )
            
                #xbmc.Player().play( play_file)
                xbmc.Player().play( playlist)  

                #mode = xbmcplugin.getSetting('play_mode')
        except:
            xbmc.log( "[script.sneak] - Playing movie failed: " , xbmc.LOGNOTICE )
            i=1
            

addon = xbmcaddon.Addon(id = 'script.sneak')
resolution = addon.getSetting('play_resolution')
year_limit = addon.getSetting('year_limit')
rating_limit = addon.getSetting('rating_limit')

xbmc.log( "[script.sneak] - Value getting from settings: %s" % resolution, xbmc.LOGNOTICE )

i=0
if addon.getSetting('play_mode') == 'true':   
        runAction(1, resolution, year_limit, rating_limit)
   
else:
        runAction(0, resolution, year_limit, rating_limit)

#player=MyPlayer()
#xbmc.sleep(3000)
#while(i!=1):
            
#    if xbmc.Player().isPlayingVideo():
#        xbmc.log( "[script.sneak] - Video running:", xbmc.LOGNOTICE )
#        i = 0
#        xbmc.sleep(3000)
#    else:
#        xbmc.log( "[script.sneak] - Video stopped:" , xbmc.LOGNOTICE )
#        i = 1
#        break
#
#if i == 1:
#    xbmc.log( "[script.sneak] - Close script:", xbmc.LOGNOTICE )
#    xbmc.executebuiltin("Notification( Sneak Ended)")
#    pass
