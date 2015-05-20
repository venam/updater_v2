# https://www.archlinux.org/feeds/news/
# this could have solved the problem of feed burner
import re
import configuration
from urllib import FancyURLopener
import sqlite_manager


def check_news(db_conn):
    """
    check_news :: Sqlite3ConnectionData -> Void

    Takes an open Sqlite3 connection
    Checks the Archlinux.org news and prints it if it's new
    """
    br = FancyURLopener()
    response = br.open("http://www.archlinux.org/news/").readlines()
    for a in response:
        if 'title="View: ' in a:
            news = re.findall('">([^<]+)</a>', a)[0]
            break
    if sqlite_manager.is_news_new(db_conn, news):
            sqlite_manager.replace_news(db_conn, news)
            print news
