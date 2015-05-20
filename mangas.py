import re
import subprocess
import configuration
import sqlite_manager
import os
from urllib import URLopener
from threading import Thread
import socket
socket.setdefaulttimeout(5)


class check_the_mangas():
    def __init__(self,manga_name, db_conn):
        self.db_conn = db_conn
        self.manga_name = manga_name
        self.manga_oldnumber = sqlite_manager.get_manga_chapter(
            db_conn,
            manga_name)
        self.manga_nownumber = self.manga_oldnumber
        self.manga_olddate = sqlite_manager.get_manga_date(
            db_conn,
            manga_name)
        self.nowdate = self.today_date()
        self.br = URLopener()

    def today_date(self):
        return subprocess.check_output(["date","+%a-%b-%e"]).replace("\n","")

    #return 1 if the connection is working
    def test_connection(self):
        try:
            response = self.br.open(configuration.WEBSITE_TO_CHECK_CONNECTION).read()
            if configuration.KEYWORD in response:
                return 1
            else:
                return 0
        except:
            print "manga connection"
            return 0

    def exec_cmd(self):
        pid = os.fork()
        os.umask(0)
        os.system(configuration.MANGA_NEW_CMD.replace("MANGA",self.manga_name))

    def run(self):
        if( self.test_connection() ):
            last_chapter = False
            try:
                while(last_chapter==False):
                    to_open = "http://www.mangareader.net/" + self.manga_name + "/" + str( int(self.manga_nownumber)+1 )
                    response = self.br.open( to_open).read()
                    if "is not released yet" in response or "not published yet" in response or response == "":
                        last_chapter = True
                        if self.manga_nownumber != sqlite_manager.get_manga_chapter(self.db_conn, self.manga_name):
                            print self.manga_name+":"+self.manga_nownumber+":"+self.nowdate
                            sqlite_manager.update_manga(self.db_conn,
                                self.manga_name,
                                self.manga_nownumber,
                                self.nowdate)
                    else:
                        self.manga_nownumber = str( int(self.manga_nownumber)+1 )
            except Exception,e :
                if "is not released yet. If you liked" in response:
                    if self.manga_nownumber != sqlite_manager.get_manga_chapter(self.db_conn,self.manga_name):
                        print self.manga_name+":"+self.manga_nownumber+":"+self.nowdate
                        sqlite_manager.update_manga(self.db_conn,
                            self.manga_name,
                            self.manga_nownumber,
                            self.nowdate)
                pass

def connection():
    try:
        br = URLopener()
        response = br.open(configuration.WEBSITE_TO_CHECK_CONNECTION).read()
        if configuration.KEYWORD in response:
            return 1
        else:
            return 0
    except:
        return 0

