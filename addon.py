'''
Created on 10.02.2011

@author: htpc-tac
'''
__scriptID__ = "script.sneak"

import xbmc
import xbmcaddon
import xbmcgui
import sys
import os
import traceback
from urllib import quote_plus

def strings(id, replacements = None):
    string = xbmcaddon.Addon(id = 'script.sneak').getLocalizedString(id)
    if replacements is not None:
        return string % replacements
    else:
        return string

def runAction( mode = "0" , resolution = "0" ,year_limit = "1900", rating_limit = "R", exclude_path = "0"):

        xbmc.log( "[script.sneak] - Value handed over for mode: %s" % mode, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for resolution: %s" % resolution, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for year_limit: %s" % year_limit, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for rating_limit: %s" % rating_limit, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for exclude_path: %s" % exclude_path, xbmc.LOGNOTICE )
        xbmc.log( "[script.sneak] - Value handed over for rating_limit: %s" % rating_limit, xbmc.LOGNOTICE )
            
        xbmc.executebuiltin( "Playlist.Clear" )
        vplaylist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        vplaylist.clear()
        
        # Ratings set
        if rating_limit== "PG-13":
            rating_sql = "AND (movie.c12  like '%%G%%' OR movie.c12 like '%%12%%' OR movie.c12 like '%%FSK 6%%' OR movie.c12 = 'Rated ')"
        elif rating_limit == "PG":
            rating_sql = "AND (movie.c12  like '%%PG%%' OR movie.c12 like '%%Rated G%%' OR movie.c12 like '%%FSK 6%%' OR movie.c12 = 'Rated ')"
        elif rating_limit == "G":
            rating_sql = "AND (movie.c12  like '%%Rated G%%' OR movie.c12 = 'Rated ')"
        else:
            rating_sql = ""
        
        if exclude_path=="0":
            exclude_path_sql=""
        else:
            exclude_path_sql=" AND movieview.strPath NOT LIKE '%%" + exclude_path + "%%'" 
            
        #Resolution set    
        if resolution == "0":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, movie WHERE movie.idFile = movieview.idFile AND movieview.playcount ISNULL AND movieview.c07 >= '%s' %s %s ORDER BY RANDOM() LIMIT 1" % (year_limit, exclude_path_sql, rating_sql)
            
        elif resolution == "1":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, streamdetails, movie WHERE streamdetails.idFile = movieview.idFile AND movie.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 576 AND movieview.c07 >= '%s' %s ORDER BY RANDOM() LIMIT 1" % (year_limit, exclude_path_sql)
           
        elif resolution == "2":
            sql = "SELECT movieview.c00, movieview.strPath, movieview.strFileName FROM movieview, streamdetails, movie WHERE streamdetails.idFile = movieview.idFile AND movie.idFile = movieview.idFile AND movieview.playcount ISNULL AND iVideoHeight > 720 AND movieview.c07 >= '%s' %s ORDER BY RANDOM() LIMIT 1" % (year_limit, exclude_path_sql)
            
        
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
        
        header = "SNEAK"
        message = "Enjoy the show"
        image = xbmc.translatePath( os.path.join( addon.getAddonInfo("path"), "icon.png") )
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, message, 5000, image) )
        
        
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

def getCachedThumb(file):
        if file[0:8] == 'stack://':
            commaPos = file.find(' , ')
            file = xbmc.getCacheThumbName(file[8:commaPos].strip())

        crc = xbmc.getCacheThumbName(file.lower())
        return xbmc.translatePath('special://profile/Thumbnails/Video/%s/%s' % (crc[0], crc))
    
#**************************
class SneakGui(xbmcgui.WindowXML):
    C_MENU_SNEAK = 4000
    C_MENU_SETTINGS = 4002
    C_MENU_EXIT = 4003
    #C_MAIN_POSTER = 4400
    #C_SEC_POSTER = 4401
    #C_THR_POSTER = 4402
    
    def __init__(self, xmlFilename, scriptPath, addon):
        xbmcgui.WindowXML.__init__(self, xmlFilename, scriptPath)
        self.addon = addon
        
    def onInit(self):
        print "MenuGui.onInit"
        #trivia = "htpc-tac"
        
        q=4400
        while q<4403:
            sql = "SELECT movieview.strPath, movieview.strFileName FROM movieview WHERE movieview.c07 < 2010 ORDER BY RANDOM() LIMIT 1"
            
            try:
                path, filename, dummy  = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
            except:
                xbmc.log( "[script.sneak] - SQL failed for guisetup: " , xbmc.LOGNOTICE )
            
            ja = 0
            ja = path.find("<field>")
            
            if ja !=-1:
                
                dummy, path = path.split( "<field>" )
                dummy, filename= filename.split( "<field>" )
            
            xbmc.log( "[script.sneak] - Gui Poster Path: %s " % path, xbmc.LOGNOTICE )
            xbmc.log( "[script.sneak] - Gui Poster filename: %s"  % filename, xbmc.LOGNOTICE )
    
            poster = getCachedThumb(os.path.join(path, filename))
            xbmc.log( "[script.sneak] - Gui Poster combine: %s"  % poster, xbmc.LOGNOTICE )
            self.getControl(q).setImage(poster)
            q= q+1
        #label = '  *  '.join(trivia)
        #self.getControl(self.C_MENU_COLLECTION_TRIVIA).setLabel(label)
        
    
    def onAction(self, action):
        if action.getId() == 9 or action.getId() == 10:
            self.close()
            
    def onClick(self, controlId):
        if controlId == self.C_MENU_SNEAK:
            if addon.getSetting('play_mode') == 'true':   
                runAction(1, resolution, year_limit, rating_limit, exclude_path)
            else:
                runAction(0, resolution, year_limit, rating_limit, exclude_path)

        elif controlId == self.C_MENU_SETTINGS:
            self.addon.openSettings()

        elif controlId == self.C_MENU_EXIT:
            self.close()
            
     #noinspection PyUnusedLocal
    def onFocus(self, controlId):
        pass
    
    def setVideoFile(self, path, filename, setCoverFile = False):
        if filename[0:8] == 'stack://':
            self.videoFile = filename
        else:
            self.videoFile = os.path.join(path, filename)

        if setCoverFile:
            self.coverFile = thumb.getCachedThumb(self.videoFile)
           
#run the script

# read the settings from /resources/settings.xml
addon = xbmcaddon.Addon(id = 'script.sneak')
resolution = addon.getSetting('play_resolution')
year_limit = addon.getSetting('year_limit')
rating_limit = addon.getSetting('rating_limit')
exclude_path_option = addon.getSetting('exclude_path_option')
#enable_gui = addon.getSetting('enable_gui')

xbmc.log( "[script.sneak] - Value getting from settings: %s" % resolution, xbmc.LOGNOTICE )

i=0
if addon.getSetting('exclude_path_option') == 'true':
    exclude_path = addon.getSetting('exclude_path')
else:
    exclude_path = "0"

if addon.getSetting('enable_gui') == 'true':
    __name__ = '__main__'
    path = addon.getAddonInfo('path')
    addon = xbmcaddon.Addon(id = 'script.sneak')

    sneakdisplay = SneakGui('script-sneak-menu.xml', path, addon = addon)
    sneakdisplay.doModal()
    del sneakdisplay
else:
    
    if addon.getSetting('play_mode') == 'true':   
            runAction(1, resolution, year_limit, rating_limit, exclude_path)
       
    else:
            runAction(0, resolution, year_limit, rating_limit, exclude_path)


#to run the window:
#sneakdisplay = SneakGui()
#sneakdisplay .doModal()
#del sneakdisplay

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
