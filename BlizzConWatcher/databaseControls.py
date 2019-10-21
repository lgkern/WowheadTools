import sqlite3
import os
import urllib


class DbApi:
    def getDatabase(self):

        dbName = 'blizzconWatcher.db'
        freshDb = os.path.isfile(dbName)
        db = sqlite3.connect(dbName)

        if not freshDb:
            cursor = db.cursor()
            cursor.execute(''' CREATE TABLE posts(post_id TEXT, title TEXT, timestamp DATE DEFAULT (datetime('now','localtime')))''')
            db.commit()

        return db


    def registerArticle(self, article):
        db = self.getDatabase()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO posts(post_id, title) VALUES(?,?)''', (article[1], article[0]) )
        db.commit()

    def checkChanges(self, article):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute( '''SELECT 1 FROM posts where post_id = ?''', (article[1],) )
        results = cursor.fetchall()

        db.commit()        
        #db.close()

        if results:
            return True
        else:
            return False

    def fetchCurrentRaw(self):
        db = self.getDatabase()

        cursor = db.cursor()
        cursor.execute( '''SELECT * FROM posts ORDER BY timestamp DESC LIMIT 1''' )
        results = cursor.fetchall()        

        db.commit()

        return results