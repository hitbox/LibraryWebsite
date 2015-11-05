import sqlite3
# create a new database if the database doesn't already exist
with sqlite3.connect("library.db") as connection:
    c = connection.cursor()
    try:
        # STAFF TABLE
        c.execute("""CREATE TABLE staff (username TEXT PRIMARY KEY, password TEXT, f_name TEXT, l_name TEXT, phone INT) """)
        c.execute("INSERT INTO staff (username,password,f_name,l_name,phone) VALUES ('admin', 'admin', 'Admin', 'User', 1111111111);")
        c.execute("INSERT INTO staff (username,password,f_name,l_name,phone) VALUES ('fred', 'fred', 'Fred', 'Fredderson', 2222222222);")

        # PROFILE TABLE
        c.execute("""CREATE TABLE profile (username TEXT, bio TEXT, FOREIGN KEY(username) REFERENCES staff(username))""")
        c.execute("""INSERT INTO profile (username,bio) VALUES('fred','')""")
        c.execute("""INSERT INTO profile (username) VALUES('admin')""")

        # READINGLIST TABLE
        c.execute("""CREATE TABLE readinglist (RLID INTEGER PRIMARY KEY AUTOINCREMENT, recdate TEXT, username TEXT,
                    book TEXT, author TEXT, comment TEXT, url TEXT, sticky INTEGER DEFAULT 0, FOREIGN KEY(username) REFERENCES staff(username))""")
        c.execute("""INSERT INTO readinglist (RLID, recdate, username, book, author, comment, url)
              VALUES (null,'2015-10-01','fred','ABCs', 'Dr. Suess','best seller','http://www.seussville.com/books/book_detail.php?isbn=9780394800301')""")
        c.execute("""INSERT INTO readinglist (RLID, recdate, username, book, author, comment, url)
              VALUES (null,'2015-10-02','fred','Night Before Christmas', 'Santa','fine holiday fun','https://www.overdrive.com/media/1577310/the-night-before-christmas')""")
    except sqlite3.OperationalError as e:
        print "Failure: " + str(e)
