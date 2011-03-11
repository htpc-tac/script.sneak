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

def runAction( mode = "0" , resolution = "0"):

        xbmc.log( "[script.sneak] - Value handed over for mode: %s" % mode, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for resolution: %s" % resolution, xbmc.LOGNOTICE )
            
        xbmc.executebuiltin( "Playlist.Clear" )
        vplaylist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        vplaylist.clear()
        
        # sql statment: SELECT * FROM streamdetails, movieview WHERE  streamdetails.idFile = movieview.idFile AND iVideoHeight > 384h
        #sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview WHERE movieview.playcount ISNULL ORDER BY RANDOM() LIMIT 1"
        
        if resolution == "0":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview WHERE movieview.playcount ISNULL ORDER BY RANDOM() LIMIT 1"
            sql_count = "SELECT count() FROM movieview WHERE movieview.playcount ISNULL ORDER BY RANDOM() LIMIT 1"
        elif resolution == "1":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, streamdetails WHERE streamdetails.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 576 ORDER BY RANDOM() LIMIT 1"
            sql_count = "SELECT count() FROM movieview, streamdetails WHERE streamdetails.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 576 ORDER BY RANDOM() LIMIT 1"
        elif resolution == "2":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, streamdetails WHERE streamdetails.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 720 ORDER BY RANDOM() LIMIT 1"
            sql_count = "SELECT count() FROM movieview, streamdetails WHERE streamdetails.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 720 ORDER BY RANDOM() LIMIT 1"
        
        xbmc.log( "[script.sneak] - SQL Statement: %s" % sql, xbmc.LOGNOTICE )
        
        try:
            movie_title, movie_path, movie_filename, dummy  = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
            number_of_movies, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_count ), ).split( "</field></record>" )
        except:
            xbmc.log( "[script.sneak] - SQL failed: " , xbmc.LOGNOTICE )
            movie_title ="" 
            movie_path ="" 
            movie_filename =""
            number_of_movies = "<record><field>0"
            
        
        #log sql result:
        
        dummy, number_of_movies = number_of_movies.split( "<record><field>" )
        xbmc.log( "[script.sneak] - Count: %s" % number_of_movies, xbmc.LOGNOTICE )
                
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
            

addon = xbmcaddon.Addon(id = 'script.sneak.headless')
resolution = addon.getSetting('play_resolution')
year_limit = addon.getSetting('year_limit')

xbmc.log( "[script.sneak] - Value getting from settings: %s" % resolution, xbmc.LOGNOTICE )

i=0
if addon.getSetting('play_mode') == 'true':   
        runAction(1, resolution)
   
else:
        runAction(0, resolution)

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
