from tkinter import *
from solar_wars import *

"""
To fix:
    -buy and sell buttons are both messed up. probably has to do with the interdependence between different 
        widgets in the planet  window - buy and sell buttons need to make a call to refresh the status bar, etc.
        -this would be a good time to implement a global refresh function, whatever that would look like 
    -make sure the destruction behavior of WarpWindow executes properly - might need to implement
        wait_window() - see other popups for examples
    -there is some weird behavior where the dividers are on the outside of the
        window instead of on the inside. Figure out what this is/why it happens
    -fix all the dependencies that have been messed up by implementing PlanetWindow (from here:
        -make a class that creates all the elements the planet buying and selling window,
        since they are not *really* the main windows, and also to easily refresh the planet items, etc.
        when warping)
    -on buying an item, this error message comes up:
        Exception in Tkinter callback
        Traceback (most recent call last):
          File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk/Tkinter.py", line 1410, in __call__
            return self.func(*args)
          File "/Users/christopher/hello-udacity-998877/Solar_Wars/gui_retry.py", line 151, in <lambda>
            self.b = Button(master, text=str(planet_item.price), command=lambda: self.popup(item_index, status_bar, status_box, player_quantity_box))
          File "/Users/christopher/hello-udacity-998877/Solar_Wars/gui_retry.py", line 159, in popup
            player_quantity_box.buttons_array[item_index].refresh_quantity_button(player.inventory[item_index].quantity)
        AttributeError: 'SellButton' object has no attribute 'buttons_array'

    **this appears to be happening because sell buttons live by themselves, they don't appear to have a coherent parent widget...    

        figure out what that's about

        -it doesn't appear to show that that item is owned by the player in the 
            corresponding sell buttons 
        -but they refresh and show how much you have when you click the sell button
            on an item you just bought
"""

"""
To do:
    -global refresh function - each button array needs to refresh each button any time something is done with it (?)
    -figure out if status_bar and status_box should be continually passed through all the method signatures, 
        or if they should be, e.g. self.status_box, for each thing that uses them, or if something else should happen
            -I guess it seems like they're tightly coupled if the other classes are causing refreshes of them - instead
            we should probably decouple them and just send a call to refresh - try winfo_toplevel().status_box.refresh()
    -give keyworded names to object instances, e.g. the planet buttons
    -change classes that inherit from object to inherit from Frame or other widgets - probably gives
        them more consistent behavior - this can also allow us to use options database to standardize
        and more easily change the look and feel of the GUI
    -make it so popup window can be exited (and still process the intended input) by pressing enter -
        so far this hasn't worked out too well. trying to use key binding
    -change BuyItemPopupWindow to defer game-logic-internal behavior to game engine - GUI shouldn't 
        determine what the player can do
    -abstract out the different widgets in the planet window
    -abstract row and column numbers (?)
        -if column full, fill in next column
        -OR define columns outside of class definition (make new class that handles column layout?)
    -use "sticky" NSEW (not sure on what because I never wrote it down when I made this comment...)
    -(eventually) abstract away from testing environment
    -implement some sort of overall refresh function? -- as it is, GUI elements that take dynamic 
        textVariables don't refresh (?)
"""

class PlanetWindow(object):
    """
    This is the main game window, where the majority of play happens. 
    One of these is created every time the player warps to a new planet. 
    """
    def __init__(self, master):
        # create the main container
        self.frame = Frame(master)
        master.wm_title('Solar Wars - ' + player.current_location.name)

        # fill it with other widgets
        self.make_widgets()

        # setup window layout
        self.frame.grid(row=0,column=0)

        # self.l.bind_class(Label)

    def cleanup(self):
        self.top.destroy()

    def make_widgets(self):
        self.status_bar = StatusBar(self.frame)
        self.status_box = StatusBox(self.frame)
        self.time_left_status_label = TimeLeftStatusLabel(self.frame, player)
        self.warp_button = WarpButton(self.frame)

        self.player_quantity_box = PlayerQuantityBox(self.frame, self.status_bar, self.status_box)
        self.item_name_box = ItemNameBox(self.frame)
        self.price_box = PlanetPriceBox(self.frame, self.status_bar, self.status_box, self.player_quantity_box)

class SellButton(object):
    """
    This makes a button that the player can push when they want to sell 
    an item. It displays the amount of the item the player currently has.
    When pressed it creates a SellItemPopupWindow, where the 
    player can specify how much of that item they want to sell.
    """
    def __init__(self, master, status_bar, status_box, item_index):
        self.master = master
        self.quantity = StringVar()
        self.quantity.set(player.inventory[item_index].quantity)
        self.b = Button(self.master, textvariable=self.quantity, command=lambda: self.popup(status_bar, status_box, item_index))

    def popup(self, status_bar, status_box, item_index):
        self.w=SellItemPopupWindow(self.master, status_bar, status_box, item_index)
        self.master.wait_window(self.w.top)
        self.refresh_quantity_button(player.inventory[item_index].quantity)

    def entry_value(self):
        return self.w.value

    def refresh_quantity_button(self, text):
        self.quantity.set(text)

class SellItemPopupWindow(object):
    """
    This is the popup window that comes up when a SellButton is pressed.
    It allows the player to specify how many of a particular item they
    want to sell.
    """
    def __init__(self, master, status_bar, status_box, item_index):
        top=self.top=Toplevel(master)
        if player.current_location.inventory[item_index].price is not None:
            self.l=Label(top,text='You have ' + str(player.inventory[item_index].quantity) + ' ' + str(player.inventory[item_index].name)+'. How many would you like to sell?')
            self.l.grid(row=0,column=0)
            self.e=Entry(top)
            self.e.grid(row=1,column=0)
            self.e.focus()
            self.b=Button(top,text='Sell',command=lambda: self.sell(status_bar, status_box, player.inventory[item_index]))
            # self.l.bind('<Button-KP-Enter>', self.sell(player.inventory[item_index]))
            self.b.grid(row=2,column=0)
        else:
            self.l=Label(top,text='No one is buying any ' +  str(player.inventory[item_index].name) + ' here!')
            self.l.grid(row=0,column=0)
            self.b=Button()

    def cleanup(self):
        # self.value=self.e.get()
        self.top.destroy()

    # def refresh_quantity_button(self, text):
    #     self.quantity.set(text)

    def sell(self, status_bar, status_box, item):
        amount_to_sell = int(self.e.get())
        player.sell(item, amount_to_sell)
        status_bar.refresh_status()
        status_box.refresh_status()
        # self.refresh_quantity_button(item.quantity)
        self.cleanup()

class BuyButton(object):
    """
    This makes a button that the player can push when they want to buy
    an item. It displays the amount of the item that the current planet has.
    When pressed it creates a BuyItemPopupWindow, where the player can specify
    how much of that item they want to buy.
    """
    def __init__(self, master, status_bar, status_box, item_index, player_quantity_box):
        self.master = master
        # self.status_bar = status_bar
        # self.status_box = status_box
        planet_item = player.current_location.inventory[item_index]
        self.b = Button(master, text=str(planet_item.price), command=lambda: self.popup(item_index, status_bar, status_box, player_quantity_box))

    def popup(self, item_index, status_bar, status_box, player_quantity_box):
        planet_item = player.current_location.inventory[item_index]
        self.w=BuyItemPopupWindow(self.master, item_index, status_bar, status_box)
        self.master.wait_window(self.w.top)
        # player_quantity_box.refresh_quantity_button(player.inventory[item_index].quantity)
        # player_quantity_box.buttons_array[player.current_location.inventory.index(item)].refresh_quantity_button(player.inventory[player.current_location.inventory.index(item)].quantity)
        player_quantity_box.buttons_array[item_index].refresh_quantity_button(player.inventory[item_index].quantity)

    def entry_value(self):
        return self.w.value

class BuyItemPopupWindow(object):
    """
    This is the popup window that comes up when a BuyButton is pressed.
    It allows the player to specify how many of a particular item they want
    to buy.
    """
    def __init__(self, master, item_index, status_bar, status_box):
        top=self.top=Toplevel(master)
        planet_item = player.current_location.inventory[item_index]
        if planet_item.price is not None:
            self.l=Label(top,text='You can afford ' + str(player.cash/planet_item.price) + ' ' + str(planet_item.name))
            self.l.grid(row=0,column=0)
            self.e=Entry(top)
            self.e.grid(row=1,column=0)
            self.e.focus()
            self.b=Button(top,text='Buy',command=lambda: self.buy(planet_item, status_box, status_bar))
            self.b.grid(row=2,column=0)
        else:
            self.l=Label(top,text='No one is selling any ' +  str(planet_item.name) + ' here!')
            self.l.grid(row=0,column=0)
            self.b=Button()
    def cleanup(self):
        # self.value=self.e.get()
        self.top.destroy()

    def buy(self, item, status_box, status_bar):
        amount_to_buy = int(self.e.get())
        player.buy(item, amount_to_buy)
        status_bar.refresh_status()
        status_box.refresh_status()
        self.cleanup()

class PlayerQuantityBox(object):
    """
    This is the section of the PlanetWindow where SellButtons live.
    It makes one button for each item in the player's inventory.
    """
    def __init__(self, master, status_bar, status_box):
        self.master = master
        self.buttons_array = []
        for i in range(len(player.inventory)):
            b = SellButton(master, status_bar, status_box, i)
            b.b.grid(row=i,column=0)
            self.buttons_array.append(b)

class ItemNameBox(object):
    """
    This is the section of the PlanetWindow where the labels for each item
    live. This label is just the name of the item. It makes one label for 
    each item in the player's inventory.
    """
    def __init__(self,master):
        self.master = master
        for i in range(len(player.inventory)):
            item_name = Label(self.master, text=player.inventory[i].name)
            item_name.grid(row=i,column=1)

class PlanetPriceBox(object):
    """
    This is the section of the PlanetWindow where BuyButtons live.
    It makes one button for each item in the planet's inventory. 
    """
    def __init__(self, master, status_bar, status_box, player_quantity_box):
        self.master = master
        self.buttons_array = []
        for i in range(len(player.inventory)):
            b = BuyButton(master, status_bar, status_box, i, player_quantity_box.buttons_array[i])
            b.b.grid(row=i,column=2)
            self.buttons_array.append(b)

class TimeLeftStatusLabel(object):
    """
    This is the section of the PlanetWindow where the time status label
    lives. Also, it puts a divider at top to make things look nice.
    """
    def __init__(self, master, player):
        divider = Frame(height=2, bd=5, relief=SUNKEN)
        divider.grid(row=8,column=0,columnspan=8, padx=5, sticky='ew')

        self.time_left = StringVar()
        self.time_left.set('Time remaining: ' + str(player.time_left) + ' days')
        l = Label(master, textvariable=self.time_left)
        l.grid(row=9, column=0, columnspan=8, sticky='w')

    def update_days_left(self, new_value):
        self.time_left.set('Time remaining: ' + str(new_value) + ' days')


"""
warp stuff
"""
class WarpButton(object):
    """
    This button makes the WarpWindow popup. It lives down below the 
    TimeLeftStatusLabel.
    """
    def __init__(self, master):
        self.master = master
        b = Button(master, text='Warp', command=self.popup)
        b.grid(row=10,column=0)

    def popup(self):
        self.w = WarpWindow(self.master)
        self.master.wait_window(self.w.top)

class WarpWindow(object):
    """
    This popup window creates a PlanetButton for each planet the player
    can warp to.
    """
    def __init__(self, master):
        top=self.top=Toplevel(master)
        self.buttons_array = []
        for i in range(len(planets_list)):
            b = PlanetButton(top, planets_list[i])
            self.buttons_array.append(b)
            b.b.grid(row=i,column=0)

    def cleanup(self):
        self.top.destroy()

class PlanetButton(object):
    """
    This is a button that, when clicked, warps the player to the planet
    that is listed on the button's text.
    """
    def __init__(self, master, planet):
        self.master = master
        self.b = Button(master, text=planet.name, command=lambda: self.warp(planet))

    def warp(self, planet):
        player.warp(planet)
        new_planet=PlanetWindow(root)
        self.master.winfo_toplevel().destroy()

"""
end warp stuff
"""

class StatusBar(object):
    """
    This is the status bar. It updates the player on things that have happened
    by updating a string variable. It lives below the WarpButton.
    """
    def __init__(self, master):
        self.master = master
        self.status = StringVar()
        Label(master, textvariable=self.status).grid(row=11,column=0,columnspan=8)
        self.status.set(player.output.return_status_message())

    def refresh_status(self):
        self.status.set(player.output.return_status_message())

    def set_status(self, message):
        self.status.set(str(message))

class StatusBoxItem(object):
    """
    This is a class for objects that will go in the side status bar. It abstracts
    the code for one label/dynamic variable coupling so it can be reusable.

    @param label_text: A string of the label to appear in the right side status box.
    @param player_attribute: The player attribute to appear in the right side status box (e.g. player.cash)
    @param starting_row_number: The row number the label will appear in. The label will appear above the
    variable.
    @param column_number: The column that the label and variable will appear in.
    """
    def __init__(self, master, label_text, player_attribute, starting_row_number, column_number):
        self.master = master
        self.label = Label(master, text=label_text)
        self.label.grid(row=starting_row_number,column=column_number)
        self.string_variable = StringVar()
        self.string_variable.set(player_attribute)
        Label(master, textvariable=self.string_variable).grid(row=starting_row_number + 1, column=column_number)
        self.player_attribute = player_attribute

    def refresh_variable(self, player_attribute):
        self.string_variable.set(player_attribute)

class StatusBox(object):
    """
    This is the side status box of the PlanetWindow. It creates a bunch of
    StatusBoxItems for each label it's going to display. They're all dynamic
    labels so that they are updated anytime a game-logic-internal variable
    changes.
    """
    def __init__(self,master):
        self.master = master
        divider = Frame(width=2, bd=5, relief=SUNKEN)
        divider.grid(row=0,column=3,rowspan=8, padx=5, sticky='ns')

        self.cash_status_box_item = StatusBoxItem(master,'Cash', player.cash, 0, 4)
        self.debt_status_box_item = StatusBoxItem(master, 'Debt', player.debt, 2, 4)
        self.savings_status_box_item = StatusBoxItem(master, 'Savings', player.savings, 4, 4)
        self.cargo_space_status_box_item = StatusBoxItem(master, 'Cargo Space', player.cargo_space, 6, 4)

    def refresh_status(self):
        self.cash_status_box_item.refresh_variable(player.cash)
        self.debt_status_box_item.refresh_variable(player.debt)
        self.savings_status_box_item.refresh_variable(player.savings)
        self.cargo_space_status_box_item.refresh_variable(player.cargo_space)

'''
Main running stuff:
'''

root = Tk()

"""
<Testing environment setup>
"""
mercury = Planet('Mercury')
venus = Planet('Venus')
earth = Planet('Earth')
mars = Planet('Mars')
jupiter = Planet('Jupiter')
saturn = Planet('Saturn')
uranus = Planet('Uranus')
neptune = Planet('Neptune')
pluto = Planet('Pluto')

earth.fuel.price = 1
player = Player('Jim', earth, 30)
player.cash = 100000
planets_list = [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto]

"""
</Testing environment setup>
"""

PlanetWindow(root)

root.mainloop()
