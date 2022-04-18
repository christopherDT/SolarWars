import random

"""
To do:
	-make a game over condition upon reaching 0 days
	-all planet prices should refresh every time you travel to a new planet -- there is a reset_prices() method for Planet class, but it doesn't seem to do anything? 
	-add time bonuses
		-add time addition (time travel) option to player.warp()
		-add time loss (ship repairs) option to player.warp()
	-figure out how to do dialogue output...
		-add dialogue for bonuses prices
	-figure out consistency when planet has no items to sell:
		quantity = None or price = None? or both?
	-figure out consistent way to refer to items -- by index? by item and then reverse lookup item index?
	-add special events that are planet-specific (double or nothing, buying more storage space, buying guns, etc.)
	-add random events (at least space pirate attacks)
		-this could probably be a random event triggered on warping - give a small percentage that before the warp
			takes place, space pirates attack
		-for that matter, this would probably need to be its own class, and certainly its own UI on the UI side of things
	-implement cargo space additions
"""

"""
To fix:
	-player can buy more items than planet has -- need to implement a check for this
	-consider factoring out output messages from game logic - should probably just be a success or failure,
        and really the GUI should probably be handling all messages - so the game logic can just pass off
        what happened or didn't happen, and the GUI can format the strings explaining what happened to the player
    -sanitize player input:
    	error message, e.g. "You can only enter a number!" should cover most situations, including if the field is left blank
"""

class Item(object):
	"""
	This class makes an Item -- Items are held, bought and sold by ItemCarriers (Players and Planets). They cost a certain amount, and have an associated quantity for each.
	"""
	def __init__(self, name):
		self.name = name
		self.quantity = 0
		self.price = None

	def get_quantity(self):
		return self.quantity

	def change_quantity(self, new_quantity):
		self.quantity = new_quantity

	def generate_price(self, base_num, modulo_num):
		self.price = base_num + random.getrandbits(32) % modulo_num
		self.add_bonus_price()
		self.deduct_bonus_price()

	def add_bonus_price(self):
		if random.randrange(1,100) > 90:
			# print 'The price of ' + self.name + ' has skyrocketed!'
			self.price = self.price * 10

	def deduct_bonus_price(self):
		if random.randrange(1,100) < 10:
			# print 'There is a surplus of ' + self.name + '. Prices plummet!'
			self.price = self.price / 10

	# def generate_quantity(self):
	# 	if random.randrange(0,10) > 9:
	# 		self.change_quantity(random.randrange(1,20))
	# 	else:
	# 		self.change_quantity(random.randrange(1,10))
	# 	self.add_bonus_quantity()
	# 	self.deduct_bonus_quantity()

	# def add_bonus_quantity(self):
	# 	if random.randrange(1,100) < 10:
	# 		self.quantity = self.quantity * 10

	# def deduct_bonus_quantity(self):
	# 	if random.randrange(1,100) < 10:
	# 		self.quantity = self.quantity / 10

	def take_away_item(self):
		if random.randrange(1,100) > 90:
			self.price = None
			self.quantity = 0
			self.has_item = False

"""
ItemCarriers are those entities that can own, buy, and sell Items, including the Player and all Planets.
"""
class ItemCarrier(object):
	def __init__(self, name):
		self.name = name
		self.populate_inventory()

	def populate_inventory(self):
		self.fuel = Item('Fuel')
		self.dilithium = Item('Dilithium')
		self.holos = Item('Holos')
		self.ore = Item('Ore')
		self.meds = Item('Meds')
		self.food = Item('Food')
		self.weapons = Item('Weapons')
		self.water = Item('Water')

		self.inventory = [self.fuel, self.dilithium, self.holos, self.ore, self.meds, self.food, self.weapons, self.water]

	def add_items(self, item, amount_to_add):
		self.item.quantity += amount_to_add

	def subtract_items(self, item, amount_to_subtract):
		self.item.quantity -= amount_to_subtract

	def get_index_by_item(self, item):
		return self.inventory.index(item)

	def get_item_by_index(self, index):
		return self.inventory[inventory]

	# def has_item(self, item_index):
	# 	return self.inventory[item_index].quantity != None
		# return self.has_item

	def has_quantity_of_item(self, item_index, quantity_query):
		return self.inventory[item_index].get_quantity() >= quantity_query

"""
Planets are the locations Players can travel to and from, and each sells items for some particular amount. Each has their own items they specialize in.
"""
class Planet(ItemCarrier):
	def __init__(self, name):
		ItemCarrier.__init__(self, name)
		# self.generate_quantities()
		# self.generate_item_prices()
		self.generate_item_params()


	def generate_item_params(self):
		# self.generate_quantities()
		self.generate_item_prices()
		self.take_away_items()

	def generate_item_prices(self):
		self.fuel.generate_price(1000, 3500)
		self.dilithium.generate_price(15000, 15000)
		self.holos.generate_price(10, 50)
		self.ore.generate_price(1000, 2500)
		self.meds.generate_price(5000, 9000)
		self.food.generate_price(300, 600)
		self.weapons.generate_price(600, 750)
		self.water.generate_price(70, 180)

	# def generate_quantities(self):
	# 	for item in self.inventory:
	# 		item.generate_quantity()

	def take_away_items(self):
		for item in self.inventory:
			item.take_away_item()

	def reset_prices(self):
		for item in self.inventory:
			item.generate_price()

	def has_item(self, item_index):
		return self.inventory[item_index].price != None

	# def num_of_items(self, item_index, num_of_items):
	# 	return self.inventory[item_index].quantity

"""
A Player travels from planet to planet, buying and selling objects. Eventually, they will also be able to engage in special activities at each Planet.
"""
class Player(ItemCarrier):
	def __init__(self, name, starting_location, starting_num_of_days):
		ItemCarrier.__init__(self, name)
		self.cash = 2000
		self.debt = 5500
		self.cargo_space = 100
		self.current_location = starting_location
		self.savings = 0
		self.time_left = starting_num_of_days
		self.output = Output()

	def warp(self, new_location):
		if new_location == self.current_location:
			self.output.set_status_message('You\'re already there, pick a new location!')
		else:
			self.current_location = new_location
			self.time_left -= 1

	def can_afford_item(self, item_to_buy, quantity_to_buy):
		price_of_desired_items = item_to_buy.price * quantity_to_buy

		return self.cash >= price_of_desired_items

	def has_enough_space(self, item, quantity_to_buy):
		return self.cargo_space >= quantity_to_buy

	def has_item(self, item_index):
		return self.inventory[item_index].quantity != 0

	def update_cargo_space(self, item, quantity):
		self.cargo_space -= item * quantity

	def buy(self, item_to_buy, quantity_to_buy):
		item_index = self.current_location.get_index_by_item(item_to_buy)

		planet_item = item_to_buy
		player_item = self.inventory[item_index]

		# price_of_desired_items = planet_item.price * quantity_to_buy

		if not self.can_afford_item(planet_item, quantity_to_buy):
			self.output.set_status_message('You can\'t afford that!')
		else:
			if not self.has_enough_space(planet_item, quantity_to_buy):
				self.output.set_status_message('You don\'t have enough space!')
			else:
				planet_item.quantity -= quantity_to_buy
				player_item.quantity += quantity_to_buy
				self.cargo_space -= quantity_to_buy
				price_of_desired_items = planet_item.price * quantity_to_buy
				self.cash -= price_of_desired_items
				self.output.set_status_message('You bought %(quantity)s %(item_name)s!' % {'quantity':str(quantity_to_buy), 'item_name':item_to_buy.name})

	def sell(self, item_to_sell, quantity_to_sell):
		item_index = self.get_index_by_item(item_to_sell)

		player_item = item_to_sell
		planet_item = self.current_location.inventory[item_index]

		# if planet_item.quantity == None or planet_item.price == None:
		if not self.current_location.has_item(item_index):
			self.output.set_status_message('No one here is buying that item!')
		elif not self.has_item(item_index): #or not self.has_quantity_of_item(item_index, quantity_to_sell):
			self.output.set_status_message('You don\'t have any ' + item_to_sell.name + ' to sell!')
		elif not self.has_quantity_of_item(item_index, quantity_to_sell):
			self.output.set_status_message('You don\'t have that many ' + item_to_sell.name + ' to sell!')
		else:
			player_item.quantity -= quantity_to_sell
			planet_item.quantity += quantity_to_sell
			self.cargo_space += quantity_to_sell
			price_of_items_to_sell = planet_item.price * quantity_to_sell
			
			self.cash += price_of_items_to_sell
			self.output.set_status_message('You sold %(quantity)s %(item_name)s!' % {'quantity':str(quantity_to_sell), 'item_name':item_to_sell.name})

class Output(object):
	def __init__(self):
		self.status_message = ''

	def return_status_message(self):
		return self.status_message

	def display_status_message(self):
		print(self.status_message)

	def set_status_message(self, message):
		self.status_message = message

	def append_to_status_message(self, append):
		self.status_message += append

	def prepend_to_status_message(self, prepend):
		self.status_message = prepend + self.status_message

	def clear_status_message(self):
		self.status_message = None

	def check_for_status_message(self):
		return self.status_message


class GameEngine(object):
	def __init__(self):
		self.earth = Planet('Earth')
		self.mercury = Planet('Mercury')
		self.mars = Planet('Mars')
		self.venus = Planet('Venus')
		self.neptune = Planet('Neptune')
		self.jupiter = Planet('Jupiter')
		self.saturn = Planet('Saturn')
		self.pluto = Planet('Pluto')
		self.player = Player(self.earth, 30)
		self.game_over = False
		self.planets_list = [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto]

	def start_game(self):
		while self.player.days_left >= 0:
			game_over = False



	# def end_game(self):
	# 	while self.player.days_left >= 0:
	# 		# continue game
