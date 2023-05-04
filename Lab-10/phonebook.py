import psycopg
import csv

# Establish a connection to the database
conn = psycopg.connect("dbname=testdb user=postgres password=admin")

# Create a cursor object to execute queries
cur = conn.cursor()

# Set autocommit to True so that every query is automatically committed to the database
conn.autocommit = True 

# Create a table if it doesn't already exist
cur.execute("""CREATE TABLE IF NOT EXISTS phonebook 
            (name TEXT,
            phone TEXT
            )""") 

# Start a loop to continuously ask for user input until they choose to exit
check = True
while check:
    print(
        "[0] to exit\n[1] to add phone\n[2] to update phone\n[3] to delete phone\n[4] print data\n[5] add csv file")
    n = int(input())

    # If the user enters 0, set check to False to exit the loop
    if n == 0:
        check = False

    # If the user enters 1, ask for a name and phone number and insert them into the phonebook table
    if n == 1:
        print("write name:")
        name = input()
        print("write phone:")
        phone = input()
        cur.execute(f"INSERT INTO phonebook (name, phone) VALUES ('{name}', '{phone}')")

    # If the user enters 2, ask for the name and phone number of the record to update, as well as the new name and phone number
    # Update the record with the new name and phone number
    if n == 2:
        print("write the user name which you want to update:")
        name = input()
        print("write the user phone which you want to update:")
        phone = input()
        print("write the new user name which you want to update:")
        new_name = input()
        print("write the new phone which you want to update:")
        new_phone = input()
        cur.execute(f"""UPDATE phonebook 
                        SET name = '{new_name}', phone = '{new_phone}'
                        WHERE name = '{name}' AND phone = '{phone}'""")

    # If the user enters 3, ask for the name and phone number of the record to delete
    # Delete the record from the phonebook table
    if n == 3:
        print("write the user name which you want to delete:")
        name = input()
        cur.execute(f"DELETE FROM phonebook WHERE name = '{name}'")

    # If the user enters 4, ask if they want to sort the data by name
    # If not, print the data in the order they were inserted
    # If yes, print the data sorted by name
    if n == 4:
        print("write the user name whose phone number you want to find:")
        name = input()
        cur.execute(f"SELECT phone FROM phonebook WHERE name = '{name}'")
        # Fetch the first row of the result
        result = cur.fetchone()
        # Print the phone number, if found
        if result:
            phone_number = result[0]
            print(f"The phone number of {name} is {phone_number}")
        else:
            print(f"No phone number found for {name}")

    # If the user enters 5, open a CSV file and insert its data into the phonebook table
    if n == 5:  # check if user input is 5
        with open('phone_book.csv') as file:  # open phone_data.csv file
            reader = csv.reader(file, delimiter=',')  # create a reader object to parse csv data
            for i in reader:  # iterate through each row of csv data
                name = i[0]  # assign the first column as name
                phone = i[1]  # assign the second column as phone
                cur.execute(f"INSERT INTO phonebook (name, phone) VALUES ('{name}', '{phone}')")  # insert the name and phone into the phonebook table
    conn.commit()  # commit changes to the database