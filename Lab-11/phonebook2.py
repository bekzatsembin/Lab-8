import psycopg

# establish a connection to the 'testdb' database using the psycopg2 library
conn = psycopg.connect(dbname="testdb", user='postgres', password='admin')

# create a cursor object to execute SQL queries on the database
cur = conn.cursor()

# set autocommit mode to True to automatically commit changes to the database
conn.autocommit = True

# create a function named 'get_pagination' that takes two arguments '_limit' and '_offset', and returns a table with two columns 'name' and 'phone'
cur.execute(''' CREATE OR REPLACE FUNCTION get_pagination(
                    _limit INT,
                    _offset INT)
                RETURNS TABLE(
                     name TEXT,
                     phone TEXT
                )
                LANGUAGE SQL
                AS $$
                    SELECT * FROM phonebook
                    LIMIT _limit
                    OFFSET _offset;
                $$''')

# create a procedure named 'add_update_user' that takes two arguments '_name' and '_phone', and adds or updates a user in the 'phonebook' table
cur.execute(''' CREATE OR REPLACE PROCEDURE add_update_user(
                    _name TEXT,
                    _phone TEXT)
            LANGUAGE plpgsql
            AS $$
            BEGIN
                UPDATE phonebook SET phone = _phone WHERE name = _name;
                IF NOT FOUND THEN
                    INSERT INTO phonebook (name, phone) VALUES (_name, _phone);
                END IF;
            END
            $$
            ''')

# create a procedure named 'delete_user' that takes two arguments '_n' and '_m', and deletes a user from the 'phonebook' table based on either their name or phone number
cur.execute('''CREATE OR REPLACE PROCEDURE delete_user(
               _n TEXT,
               _m TEXT)
               LANGUAGE plpgsql
               AS $$
               BEGIN
                   IF _m = 'p' THEN
                       DELETE FROM phonebook WHERE phone = _n;
                   ELSE
                       DELETE FROM phonebook WHERE name = _n;
                   END IF;
               END
               $$''')

check = True

while check:
    # Display the options for the user to choose from
    print("[0] to exit\n[1] to print data with pattern\n[2] to insert/update user\n[3] insert many\n[4] pagination\n[5] delete by name/phone")

    # Get the user's choice
    choice = int(input("number:"))

    # If the user chooses 0, exit the loop and end the program
    if choice == 0:
        check = False
    
    # If the user chooses 1, search for data with a specific pattern in the phonebook
    if choice == 1:
        pattern = input("what pattern?")
        cur.execute("SELECT * FROM phonebook WHERE CONCAT(name, phone) LIKE '%"+pattern+"%'")
        result = cur.fetchall()
        for i in result:
            print(i)
    
    # If the user chooses 2, insert or update a user in the phonebook
    if choice == 2:
        user = input("user_name:")
        phone = input("phone:")
        cur.execute("CALL add_update_user(%s,%s)",(user,phone))
    
    # If the user chooses 3, insert many users into the phonebook
    if choice == 3:
        print('insert name phone and so on')
        values = input()
        values = values.split(" ")
        inc_v = {}
        a = {}
        i = 0
        while i != len(values):
            n, p = values[i], values[i + 1]
            try:
                if type(int(p)) is int:
                    a[n] = p
                    cur.execute("CALL add_update_user(%s, %s)", (n, p))
            except:
                inc_v[n] = p
            i += 2
    
    # If the user chooses 4, display a pagination of the phonebook
    if choice == 4:
        offset = input("offset")
        limit = input("limit:")
        cur.execute('SELECT * FROM get_pagination(%s,%s)',(limit,offset))
        result = cur.fetchall()
        for i in result:
            print(i)
    
    # If the user chooses 5, delete a user from the phonebook
    if choice == 5:
        what_to_delete = input('p/n:')
        nameORphone = input('input name/phone to delete:')
        cur.execute("CALL delete_user(%s,%s)",(nameORphone,what_to_delete))