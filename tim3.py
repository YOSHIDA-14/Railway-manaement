from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager

import mysql.connector as ms

con = ms.connect(host="localhost", user="root", passwd="immastudyiniitgoa", database="S01")
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

def reserve_seat(name, seats, destination):
    des = {}
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

                # Display reservation details
                display_reservation_details(name)
            else:
                print("Reservation canceled.")
            break
    else:
        print("Train not found!")

def display_reservation_details(name):
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


def remove_train(train_name):
    query = "SELECT * FROM trains WHERE train = %s"
    cuz.execute(query, (train_name,))
    data = cuz.fetchall()

    if data:
        query = "DELETE FROM trains WHERE train = %s"
        execute_query(query, (train_name,))
        print("Record deleted!!")
    else:
        print("Train not found!")


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text='===== WELCOME TO RAILWAYS =====', font_size=20)
        layout.add_widget(label)

        button_book = Button(text='Book Your Journey', on_press=self.switch_to_book_journey)
        layout.add_widget(button_book)

        # ... (other buttons)

        self.add_widget(layout)

    def switch_to_book_journey(self, instance):
        self.manager.current = 'book_journey'


class BookJourneyScreen(Screen):
    def __init__(self, **kwargs):
        super(BookJourneyScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text='Booking Journey Screen', font_size=20)
        layout.add_widget(label)

        # Input fields
        input_name = TextInput(hint_text='Enter your Name')
        layout.add_widget(input_name)

        input_seats = TextInput(hint_text='How many Seats will you need', input_type='number')
        layout.add_widget(input_seats)

        input_destination = TextInput(hint_text='Enter your destination')
        layout.add_widget(input_destination)

        button_confirm = Button(text='Confirm Reservation', on_press=self.confirm_reservation)
        layout.add_widget(button_confirm)

        self.add_widget(layout)

    def confirm_reservation(self, instance):
        name = self.children[0].text
        seats = int(self.children[1].text)
        destination = self.children[2].text
        reserve_seat(name, seats, destination)

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text='Admin Screen', font_size=20)
        layout.add_widget(label)

        # Input field for train removal
        input_train_remove = TextInput(hint_text='Enter the train to remove')
        layout.add_widget(input_train_remove)

        # Button to remove train
        button_remove_train = Button(text='Remove Train', on_press=self.remove_train)
        layout.add_widget(button_remove_train)

        self.add_widget(layout)

    def remove_train(self, instance):
        train_name = self.children[0].text
        remove_train(train_name)