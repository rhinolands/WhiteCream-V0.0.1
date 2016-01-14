'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sqlite3

import utils

dialog = utils.dialog

favoritesdb = os.path.join(utils.profileDir, 'favorites.db')

if not os.path.isfile(xbmc.translatePath(favoritesdb)):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM favorites;")
    except sqlite3.OperationalError:
        c.executescript("CREATE TABLE favorites (name, url, mode, image);")


def List():
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM favorites")
        for (name, url, mode, img) in c.fetchall():
            utils.addDownLink(name, url, int(mode), img, '', '', 'del')
        xbmcplugin.endOfDirectory(utils.addon_handle)
    except:
        dialog.ok('No Favorites','No Favorites found')
        return


def Favorites(fav,mode,name,url,img):
    if fav == "add":
        delFav(url)
        addFav(mode, name, url, img)
        dialog.ok('Favorite added','Video added to the favorites')
    elif fav == "del":
        delFav(url)
        dialog.ok('Favorite deleted','Video removed from the list')
        xbmc.executebuiltin('Container.Refresh')


def addFav(mode,name,url,img):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO favorites VALUES (?,?,?,?)", (name, url, mode, img))
    conn.commit()


def delFav(url):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE url = '%s'" % url)
    conn.commit()

