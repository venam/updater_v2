#!/usr/bin/env python2

"""
Copyright (c) 2015, Patrick Louis <patrick at iotek do org>
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    1.  The author is informed of the use of his/her code. The author does not
        have to consent to the use; however he/she must be informed.
    2.  If the author wishes to know when his/her code is being used, it the
        duty of the author to provide a current email address at the top of
        his/her code, above or included in the copyright statement.
    3.  The author can opt out of being contacted, by not providing a form of
        contact in the copyright statement.
    4.  If any portion of the author's code is used, credit must be given.
            a. For example, if the author's code is being modified and/or
               redistributed in the form of a closed-source binary program,
               then the end user must still be made somehow aware that the
               author's work has contributed to that program.
            b. If the code is being modified and/or redistributed in the form
               of code to be compiled, then the author's name in the copyright
               statement is sufficient.
    5.  The following copyright statement must be included at the beginning of
        the code, regardless of binary form or source code form.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Except as contained in this notice, the name of a copyright holder shall not
be used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization of the copyright holder.

----

The database handler/manager.

"""

import sqlite3


def get_db_connection(db_name):
    """
    get_db_connection :: String -> Sqlite3ConnectionData

    Takes the location of the db and connects to it
    Returns the connection data needed for the other functions
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    return (conn, c)


def db_timestamp(db_conn):
    """
    db_timestamp :: Sqlite3ConnectionData -> String

    Takes an Sqlite3 opened connection
    Returns the timestamp generated by the db
    """
    return db_conn[1].execute(
        "select CURRENT_TIMESTAMP;"
    ).next()[0]


def get_news(db_conn):
    """
    get_old_news :: Sqlite3ConnectionData -> String

    Takes an Sqlite3 opened connection
    Returns the news found in the db
    """
    return db_conn[1].execute(
        "select news from archnews limit 1;"
    ).next()[0]


def get_manga_chapter(db_conn, manga_name):
    """
    get_manga_chapter :: Sqlite3ConnectionData -> String -> Int

    Takes an Sqlite3 opened connection and a manga name (String)
    Returns the current chapter found in the db
    """
    return db_conn[1].execute(
        "select chapter from mangas where name='"+manga_name+"';"
    ).next()[0]


def get_manga_date(db_conn, manga_name):
    """
    get_manga_date :: Sqlite3ConnectionData -> String -> Date

    Takes an Sqlite3 opened connection and a manga name (String)
    Returns the current date found in the db
    """
    return db_conn[1].execute(
        "select release from mangas where name='"+manga_name+"';"
    ).next()[0]


def update_manga(db_conn, manga_name, chapter, release):
    """
    update_manga :: Sqlite3ConnectionData -> String ->
        Int -> Date -> Void
    """
    db_conn[1].execute(
        ("update mangas set chapter = "+ chapter +
            ", release='" + release + "' where name='" + manga_name +
            "';")
    )
    db_conn[0].commit()


def insert_manga(db_conn, manga_name, chapter, release):
    """
    update_manga :: Sqlite3ConnectionData -> String ->
        Int -> Date -> Void
    """
    db_conn[1].execute("delete from mangas where name='"+manga_name+"';")
    db_conn[0].commit()
    db_conn[1].execute(
        ("insert into mangas values( '"+manga_name+"',"+ chapter +
            ", '" + release + "' );")
    )
    db_conn[0].commit()


def replace_news(db_conn, news):
    """
    replace_news :: Sqlite3ConnectionData -> String -> Void

    Takes an Sqlite3 opened connection and a news (String)
    """
    db_conn[1].execute("delete from archnews;")
    db_conn[1].execute(
        ("insert into archnews values (" +
            "'" + news.replace("'", '"') + "'" +
            ");")
    )
    db_conn[0].commit()


def is_news_new(db_conn, news):
    """
    is_news_new :: Sqlite3ConnectionData -> String -> Bool

    Takes and Sqlite3 opened connection and a news (String)
    Returns true if the news differ
    """
    old_news = get_news(db_conn)
    news = news.replace("'", '"')
    return old_news != news
