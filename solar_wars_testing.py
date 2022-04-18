from solar_wars import *
import unittest

"""
TO DO:
    make sure quantities cannot go below zero
        including prices, item quantities
"""
class TestItemFunctions(unittest.TestCase):
    def setUp(self):
        self.fuel = Item('Fuel')

class TestPlanetFunctions(unittest.TestCase):

    def setUp(self):
        self.earth = Planet('Earth')
        self.mars = Planet('Mars')

    def test_planet_uniqueness(self):
        self.assertNotEqual(self.earth, self.mars)

    def test_item_uniqueness(self):
        self.assertNotEqual(self.earth.fuel, self.mars.fuel)

    def test_item_uniqueness_2(self):
        self.earth.fuel.change_quantity(300)
        self.assertNotEqual(self.earth.fuel, self.mars.fuel)

    def test_planet_name(self):
        self.assertEqual(self.earth.name, 'Earth')

    def test_inventory_length_equality(self):
        self.assertEqual(len(self.earth.inventory), len(self.mars.inventory))

    def test_unique_item_prices(self):
        earth_prices = [self.earth.inventory[i].price for i in range(len(self.earth.inventory))]
        mars_prices = [self.mars.inventory[i].price for i in range(len(self.mars.inventory))]

        # test inequality of the whole lists
        self.assertNotEqual(earth_prices, mars_prices)

    def test_planet_has_item(self):
        self.earth.meds.price = 100
        self.earth.holos.price = None

        self.assertTrue(self.earth.has_item(self.earth.get_index_by_item(self.earth.meds)))
        self.assertFalse(self.earth.has_item(self.earth.get_index_by_item(self.earth.holos)))

    def test_planet_has_quantity_of_item(self):    
        self.earth.meds.quantity = 785

        self.assertTrue(self.earth.has_quantity_of_item(self.earth.get_index_by_item(self.earth.meds), 785))

class TestPlayerFunctions(unittest.TestCase):
    def setUp(self):
        self.jupiter = Planet('Jupiter')
        self.neptune = Planet('Neptune')
        self.player = Player('Jim', self.jupiter, 30)

    def test_warping_success(self):
        starting_location = self.player.current_location
        starting_days_left = self.player.time_left

        self.player.warp(self.neptune)

        ending_location = self.player.current_location
        ending_days_left = self.player.time_left

        self.assertNotEqual(starting_location, ending_location)
        self.assertEqual(ending_days_left, starting_days_left - 1)

    def test_warping_failure(self):
        starting_location = self.player.current_location
        self.player.warp(self.jupiter)

        ending_location = self.player.current_location

        self.assertEqual(starting_location, ending_location)
        self.assertEqual(self.player.output.return_status_message(), 'You\'re already there, pick a new location!')

    def test_player_has_item(self):
        self.player.meds.quantity = 100
        self.player.holos.quantity = 0

        self.assertTrue(self.player.has_item(self.player.get_index_by_item(self.player.meds)))
        self.assertFalse(self.player.has_item(self.player.get_index_by_item(self.player.holos)))

    def test_player_has_quantity_of_item(self):    
        self.player.meds.quantity = 10000

        self.assertTrue(self.player.has_quantity_of_item(self.player.get_index_by_item(self.player.meds), 785))

    def test_can_afford_item(self):
        self.player.current_location.fuel.price = 500
        self.player.cash = 10000000000000

        self.assertTrue(self.player.can_afford_item(self.player.current_location.fuel, 100))

        self.player.cash = 0
        self.assertFalse(self.player.can_afford_item(self.player.current_location.fuel, 100))

    def test_has_enough_space(self):
        self.player.current_location.fuel.price = 500
        self.player.cash = 10000000000000
        self.player.cargo_bays = 100000000
        self.jupiter.fuel.quantity = 100000

        self.assertTrue(self.player.has_enough_space(self.player.current_location.fuel, 100))

    def test_buying_success(self):
        self.player.current_location.fuel.price = 500
        self.player.cash = 10000000000000
        starting_cash = self.player.cash
        self.jupiter.fuel.quantity = 1000000

        self.player.buy(self.player.current_location.fuel, 100)

        ending_cash = self.player.cash

        # self.assertEqual(return_, 'You bought 100 Fuel')
        self.assertEqual(self.player.output.return_status_message(), 'You bought 100 Fuel!')
        self.assertNotEqual(starting_cash, ending_cash)

    def test_buying_cannot_afford(self):
        self.player.current_location.fuel.price = 10000000000000
        self.player.cash = 10
        starting_cash = self.player.cash

        self.player.buy(self.player.current_location.fuel, 100)

        ending_cash = self.player.cash

        # self.assertEqual(return_, 'You can\'t buy that!')
        self.assertEqual(self.player.output.return_status_message(), 'You can\'t afford that!')
        self.assertEqual(starting_cash, ending_cash)        

    def test_enough_space_success(self):
        self.player.cargo_space = 100
        self.player.cash = 100000000000000000000
        starting_size = self.player.cargo_space
        self.player.current_location.fuel.price = 10
        self.player.current_location.fuel.quantity = 10000000000000

        self.player.buy(self.player.current_location.fuel, 10)

        ending_size = self.player.cargo_space

        self.assertNotEqual(starting_size, ending_size)
        self.assertEqual(self.player.output.return_status_message(), 'You bought 10 Fuel!')

    def test_enough_space_failure(self):
        self.player.cargo_space = 1
        self.player.cash = 100000000000000000000
        starting_size = self.player.cargo_space
        self.player.current_location.fuel.price = 10

        self.player.buy(self.player.current_location.fuel, 10)

        ending_size = self.player.cargo_space

        self.assertEqual(starting_size, ending_size)
        self.assertEqual(self.player.output.return_status_message(), 'You don\'t have enough space!')

    def test_current_location_has_item(self):
        self.jupiter.meds.quantity = 100
        self.neptune.meds.quantity = None

    def test_selling_success(self):
        self.jupiter.holos.quantity = 100
        self.jupiter.holos.price = 10
        self.player.holos.quantity = 5000

        starting_cash = self.player.cash
        starting_cargo_space = self.player.cargo_space

        self.player.sell(self.player.holos, 100)

        ending_cash = self.player.cash
        ending_cargo_space = self.player.cargo_space

        self.assertNotEqual(starting_cash, ending_cash)
        self.assertEqual(ending_cash, starting_cash + self.player.current_location.holos.price * 100)

        self.assertNotEqual(starting_cargo_space, ending_cargo_space)
        self.assertEqual(ending_cargo_space, starting_cargo_space + 100)

        self.assertEqual(self.player.output.return_status_message(), 'You sold 100 Holos!')

    def test_selling_failure_planet_not_buying_item(self):
        self.jupiter.holos.price = None
        # self.player.holos.price = None

        starting_cash = self.player.cash
        starting_cargo_space = self.player.cargo_space

        self.player.sell(self.player.holos, 100)

        ending_cash = self.player.cash
        ending_cargo_space = self.player.cargo_space

        self.assertEqual(starting_cash, ending_cash)
        self.assertEqual(starting_cargo_space, ending_cargo_space)
        self.assertEqual(self.player.output.return_status_message(), 'No one here is buying that item!')

    def test_selling_failure_do_not_have_item(self):
        self.jupiter.holos.price = 100000
        self.player.holos.quantity = 0

        starting_cash = self.player.cash
        starting_cargo_space = self.player.cargo_space

        self.player.sell(self.player.holos, 100)

        ending_cash = self.player.cash
        ending_cargo_space = self.player.cargo_space

        self.assertEqual(starting_cash, ending_cash)
        self.assertEqual(starting_cargo_space, ending_cargo_space)
        self.assertEqual(self.player.output.return_status_message(), 'You don\'t have any Holos to sell!')

    def test_selling_failure_do_not_have_enough_items(self):
        # self.jupiter.holos.quantity = 100000
        self.player.holos.quantity = 5
        self.jupiter.holos.price = 50000000000000000

        starting_cash = self.player.cash
        starting_cargo_space = self.player.cargo_space

        self.player.sell(self.player.holos, 100)

        ending_cash = self.player.cash
        ending_cargo_space = self.player.cargo_space

        self.assertEqual(starting_cash, ending_cash)
        self.assertEqual(starting_cargo_space, ending_cargo_space)
        self.assertEqual(self.player.output.return_status_message(), 'You don\'t have that many Holos to sell!')

class TestOutputFunctions(unittest.TestCase):
    def setUp(self):
        self.output = Output()
    def test_set_status_message(self):
        self.output.set_status_message('Hello!')
        self.assertEqual(self.output.return_status_message(), 'Hello!')

if __name__ == '__main__':
    unittest.main()