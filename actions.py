from game import *
from inputs import *


class Action(object):
	def __init__(self,player):
		self.name = 'unknown action'
		self.trigger = 'unknown'
		self.player = player



"""******************"""
"""Place worker actions"""
"""******************"""
class ActiveAction(Action):
	def __init__(self):
		Action.__init__(self)
		self.name = 'unknown active action'

	def execute(self):
		return True

class BuildingAction(Action):
	def __init__(self, building, player):
		Action.__init__(self, player)
		self.name = 'Go to the %s' % building.name
		self.building = building

	def execute(self):
		#this will look at the building type and add the correct resources to the player, mark the worker as used, and use a building spot

		worker = GetWorker(self.player)

		if worker.is_placed:
			print 'This %s is already used!' % worker.name
			return False

		else:

			if self.building.is_available():
				resources = worker.building_resources[type(self.building)]
				self.player.add_resources(resources)
				self.building.use_spot()
				worker.is_placed = True
				print '---Action: Visit Building---'
				print '   %s sent a %s to the %s.' % (self.player.name, worker.name, self.building.name)
				print ''
				return True
			else:
				print 'The %s is full!' % self.building.name
				print ''
				return False

class TownHallAction(Action):
	def __init__(self, building, player, starting_player_available):
		Action.__init__(self, player)

		self.name = 'Go to the %s' % building.name
		self.starting_player_available = starting_player_available
		
		"""This doesn't seem to be working right now"""

		if self.starting_player_available:
			self.name = self.name + ' and take Starting Player!'

		self.building = building

	def execute(self):
		#this will...do nothing now because I haven't set up the town hall

		worker = GetWorker(self.player)

		if worker.is_placed:
			print 'This %s is already used!' % worker.name
			return False

		else:

			if self.building.is_available():

				worker.is_placed = True
				self.building.use_spot()
				"""Give the player a card or something"""

				print '---Action: Visit Building---'
				print '   %s sent a %s to the %s. (but it does nothing right now)' % (self.player.name, worker.name, self.building.name)


				if self.starting_player_available:
					if take_starting_player():
						print '   %s took Starting Player!' % self.player.name
						self.player.starting_player = True
						self.building.starting_player_available = False
						# The logic for switching starting player is in game.py

				print ''

				return True

			else:
				print 'The %s is full!' % self.building.name
				print ''
				return False

class PlayerPass(Action):
	def __init__(self, player):
		Action.__init__(self, player)
		self.name = 'Pass this turn'

	def execute(self):
		self.player.has_passed = True
		print '---Inaction: Pass---'
		print '   %s passed their turn.' % self.player.name
		print '' 
		return True


"""******************"""
"""Triggered actions"""
"""******************"""
class IncomeAction(Action):
	def __init__(self):
		Action.__init__(self)
		self.name = 'unknown income action'
		self.trigger = 'round_start'

		"""Do this one next"""

	def execute(self):
		return True



"""******************"""
"""Passive actions"""
"""******************"""
class PassiveAction(Action):
	def __init__(self):
		Action.__init__(self)
		self.name = 'unknown passive action'

	def execute(self):
		return False

class TradeAction(Action):
	def __init__(self, player, resource_in, resource_in_amt, resource_out, resource_out_amt):
		# Generic trade transaction
		# Specify which resource comes in and how many you need
		# and specify what and how much comes out!
		Action.__init__(self, player)

		self.name = 'Trade %s %s for %s %s' % (str(resource_in_amt), str(resource_in), str(resource_out_amt), str(resource_out))

		self.resource_in = resource_in
		self.resource_out = resource_out

		# Use this in the actual transaction below
		self.transaction = {
		resource_in : resource_in_amt,
		resource_out : resource_out_amt,
		}

	def execute(self):
		
		player = self.player

		amount_in = GetTradeAmount(player, self.resource_in)

		# First check the amount available to make sure they're not asking for too much
		amount_available = player.resources[self.resource_in]

		if amount_in > amount_available:
			# If not, delived the bad news
			print '%s does not have enough %s!' % (player.name, self.resource_in),
			print '(requested: %s, available: %s)' % (str(amount_in), str(amount_available))
			print ''
		else:
			# Get a corrected amount in case they want to trade some incorrect ratio
			corrected_amount_in = int(amount_in/self.transaction[self.resource_in])*self.transaction[self.resource_in]

			# Calculate the amount out
			amount_out = amount_in/self.transaction[self.resource_in]*self.transaction[self.resource_out]

			# build a resource dictionary and perform the transaction for the player
			resource_transaction = {
			self.resource_in : -1*corrected_amount_in,
			self.resource_out : amount_out
			}

			player.add_resources(resource_transaction)

			# And send confirmation!
			print '---Passive Action: Trade---'
			print '   %s traded %s %s for %s %s' % (player.name, str(corrected_amount_in), self.resource_in, str(amount_out), self.resource_out)
			print ''


		return False



"""******************"""
"""Start game actions"""
"""******************"""
class StartingIncome(Action):
	def __init__(self, player, occupation, resources):
		Action.__init__(self, player)
		self.name = '%s\'s starting income' % occupation.name

		self.resource_transaction = resources

	def execute(self):
		print '---Starting Income---'
		print '   %s got the %s' % (self.player.name, self.name)
		print ''
		self.player.add_resources(self.resource_transaction)



"""******************"""
"""End game actions"""
"""******************"""
class EndgameAction(Action):
	def __init__(self, player):
		Action.__init__(self, player)
		self.name = 'unknown endgame action'

	def execute(self):
		pass