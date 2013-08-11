import sqlite3

class model(object):
    """
    cutter ivory library
    model object
    This class is intended to be inherited by application model classes.

    """
       
    def __init__(self, table, db):
        self.table = table
        self.db = db
        self.con = None
        self.cur = None

    def execute(self, st, args):
        if self.cur:
            self.cur.execute(st, args)
        else:
            self.begin()
            self.cur.execute(st, args)
            self.end()
        cur = self.cur
        del self.cur
        return cur

    def begin(self):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def end(self):
        self.con.close()
        del self.con

    def __call__(self, cur):
        self.cur = cur
        return cur

    def transaction(self, cur):
        return self(cur)


















