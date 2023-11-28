import mysql.connector as ms

con = ms.connect(host="Localhost", user="root", passwd="immastudyiniitgoa", database="S01")
cuz = con.cursor()

def execute_query(query, values=None):
    try:
        if values:
            cuz.execute(query, values)
        else:
            cuz.execute(query)
        con.commit()
        return True
    except Exception as e:
        print(f"Error during execution: {e}")
        return False

def cancel():
    namee = input("Enter Your name: ")
    query1 = f"SELECT train, seats FROM passenger WHERE name = '{namee}'"
    cuz.execute(query1)
    seats = cuz.fetchone()

    if seats:
        train, seatss = seats[0], seats[1]

        # Update train vacancy
        query2 = f"UPDATE trains SET vacancy = vacancy + {seatss} WHERE train = '{train}'"
        execute_query(query2)

        # Delete passenger record
        query3 = f"DELETE FROM passenger WHERE name = '{namee}'"
        execute_query(query3)

        print("Reservation canceled successfully!")
    else:
        print("No reservation found for the given name.")

def display_reservation_details():
    name = input("Enter your name: ")
    query = "SELECT * FROM passenger WHERE Name = %s"
    cuz.execute(query, (name,))
    data = cuz.fetchall()

    if not data:
        print("No reservation found for the given name.")
        return

    lit = [i for i in data[0]]
    print("Name:", lit[0])
    print("Seats:", lit[1])
    print("Amount:", lit[2])
    print("Destination:", lit[3])
    print("Train you should board:", lit[4])
    print("You are all set!!")

def reserve_seat():
    des = {}
    name = input("Enter your Name: ")
    seats = int(input("How many Seats will you need: "))
    destination = input("Enter your destination: ")

    # Fetch available trains for the destination
    query = "SELECT * FROM trains WHERE destination = %s"
    cuz.execute(query, (destination,))
    data = cuz.fetchall()

    if not data:
        print("Sorry, We don't provide our service for your destination")
        return

    print("The trains available for the destination are:")
    for i in data:
        print(i[0], "-", i[3], "  Date of boarding-", i[4])
        des[i[0]] = i[3]

    train = input("Type the name of the train you want to reserve your seats: ")
    for i in data:
        if i[0] == train:
            amount = i[2] * seats
            print("Your Fare will be:", amount)
            conf = input("Type [y] for confirmation and [n] to leave: ").lower()

            if conf == "y":
                # Insert passenger details
                query = "INSERT INTO passenger (Name, seats, amount, destination, train) VALUES (%s, %s, %s, %s, %s)"
                values = (name, seats, amount, destination, train)
                execute_query(query, values)

                # Update train vacancy
                query2 = "UPDATE trains SET vacancy = vacancy - %s WHERE train = %s"
                values2 = (seats, train)
                execute_query(query2, values2)

                print("Reservation successful!")
                print(f"You can collect your tickets by paying Rs {amount} before boarding")
            else:
                print("Reservation canceled.")
            break
    else:
        print("Train not found!")

def remove_train():
    trainn = input("Which train do you want to remove: ")
    query = "SELECT * FROM trains WHERE train = %s"
    cuz.execute(query, (trainn,))
    data = cuz.fetchall()

    if data:
        query = "DELETE FROM trains WHERE train = %s"
        execute_query(query, (trainn,))
        print("Record deleted!!")
    else:
        print("Train not found!")

def admin():
    print(" 1. Add train details \n 2. Add admin \n 3. Delete train Detail \n 4. Exit")
    res = int(input("Type 1, 2, 3, or 4: "))

    if res == 1:
        name = input("Enter the Train name: ")
        seat = int(input("Enter the Number of vacancy: "))
        price = int(input("Enter the Price of a ticket: "))
        des = input("Enter the destination: ")
        date = input("Enter the date: ")
        
        query = "INSERT INTO trains (TRAIN, VACANCY, PRICE, DESTINATION, Date) VALUES (%s, %s, %s, %s, %s)"
        values = (name, seat, price, des, date)
        execute_query(query, values)
        print("Record added!!")
    
    elif res == 2:
        username = input("Enter the Username: ")
        password = input("Enter the password: ")
        query = "INSERT INTO admin(username, password) VALUES (%s, %s)"
        values = (username, password)
        execute_query(query, values)

    elif res == 3:
        remove_train()
    
    elif res == 4:
        print("Thank you")

def code():
    def fancy_invalid_input():
        print("**************************************")
        print("***    Oops! Invalid Input.      ***")
        print("***   Please try again with a    ***")
        print("***     valid input format.      ***")
        print("**************************************")

    def fancy_welcome():
        print("**************************************")
        print("***                               ***")
        print("***  WELCOME TO RAILWAYS  ***")
        print("***                               ***")
        print("**************************************")
    
    fancy_welcome()

    print(" 1. Book Your Journey \n 2. Check status \n 3. Cancel Your Journey\n 4. Manage")
    response = int(input("\nWhat do you want to do: "))

    if response == 1:
        reserve_seat()
    elif response == 2:
        display_reservation_details()
    elif response == 3:
        cancel()
    elif response == 4:
        Username = input("Enter your username: ")
        password = input("Enter your password: ")
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cuz.execute(query, (Username, password))
        raw = cuz.fetchall()
        if raw:
            admin()
    else:
        fancy_invalid_input()

code()
