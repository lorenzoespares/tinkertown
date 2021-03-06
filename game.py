from players import *
from workers import *
from buildings import *
from machines import *
from inputs import *
from actions import *

class Game(object):
	def __init__(self):
		# self.num_players = input('Number of players? ')
		self.workers_per_occupation = 1
		self.num_rounds = 4
		self.round = 0

		self.num_players = 0
		self.players = {}
		self.buildings = {}

		self.turn_order = []
		self.old_starting_player = ''
		self.starting_player = ''
		self.rounds = [i for i in range(self.num_rounds)]

	def create_players(self, players):
		
		for name, occupation in players.items():

			self.players[name] = Player(name)

			player = self.players[name]

			player.add_starting_occupations(occupation, [self.workers_per_occupation for i in occupation])

	def create_buildings(self):
		self.buildings['Bank'] = Bank(self.num_players)
		self.buildings['Forge'] = Forge(self.num_players)
		self.buildings['Workshop'] = Workshop(self.num_players)
		self.townhall = TownHall(self.num_players)

	def create_market(self):
		pass

	def create_townhall_cards(self):
		pass

	def check_actions(self, player):
		# this method will be called throughout the game to make sure the player has the correct actions

		player.start_game_actions = []
		player.place_actions = [PlayerPass(player)]
		player.passive_actions = []
		player.trigger_actions = []

		player.actions = {
		'Start Game' : player.start_game_actions,
		'Place Worker' : player.place_actions,
		'Passive Action' : player.passive_actions,
		'Triggered Actions' : player.trigger_actions,
		}

		# check the occupations first
		for worker in player.workers:
			for action_type, player_action_set in player.actions.items():
				for worker_action in worker.actions[action_type]:

					action_name = worker_action.name

					if action_name not in [action.name for action in player_action_set]:
							player_action_set.append(worker_action)


		# then check all the buildings for available spots
		for name, building in self.buildings.items():
			if building.is_available():
				player.place_actions.append(BuildingAction(building, player))

		if self.townhall.is_empty():
			player.place_actions.append(TownHallAction(self.townhall, player, True))
		elif self.townhall.is_available():
			player.place_actions.append(TownHallAction(self.townhall, player, False))


		# and then check the machines
		"""Not done yet. Machines don't exist yet!"""

		# AND check the cards this player has

		player.consolidate_actions()

	def list_players(self):
		for player_name in self.players:
			print player_name

	def list_available_buildings(self):
		for name, building in self.buildings.items():
			if building.is_available():
				print '    The %s is available' % name

	def end_of_round(self):
		return sum([player.has_action() for name, player in self.players.items()])==0


	def start_game(self, players):
		print '********************************'
		print '********************************'
		print 'Start the game!!'
		print '********************************'
		print '********************************'
		print ''
		self.num_players = len(players)

		self.create_buildings()
		self.create_market()
		self.create_townhall_cards()

		self.create_players(players)

		# based on the occupations of each player, get their starting resources
		# probably should refactor this...
		for name, player in self.players.items():
			self.check_actions(player)
			for action in player.start_game_actions:
				action.execute()

	def start_round(self):
		# determine starting player and play order using self.turn_order
		# set up the cards and the machines

		for name, building in self.buildings.items():
			building.reset_building()

		self.townhall.reset_building()

		# totally rando right now
		for name, player in self.players.items():
			self.turn_order.append(name)
			player.reset_workers()
			player.check_workers()
			player.has_passed = False

		print '********************************'
		print 'Start round ' + str(self.round)
		print '********************************'
		print ''


	def take_turn(self, player):
		print '********************************'
		print '%s\'s turn' % player.name
		print ''

		turn_taken = False

		while not(turn_taken):
			self.check_actions(player)
			player.list_actions()

			chosen_action = input('Take which action? ') - 1
			print ''
			turn_taken = player.all_actions[chosen_action].execute()

	def end_round(self):
		# at round end, give each player the resources for unplaced workers
		# at round end, give the appropriate won auctions to the players
		# at round end, un-place each worker
		# at round end, check for game end and do appropriate actions
		
		for name, player in self.players.items():
			player.list_resources()

		print '********************************'
		print 'End round ' + str(self.round)
		print '********************************'
		print ''

	def end_game(self):
		# count up the power!
		print '********************************'
		print '********************************'
		print 'End the game'
		print '********************************'
		print '********************************'

	def run_game(self, players):

		self.start_game(players)

		for round in self.rounds:

			self.round = round + 1

			self.start_round()

			turn_marker = 0

			while not(self.end_of_round()):
				player = self.players[self.turn_order[turn_marker]]
				player.has_passed = False
				player.check_workers()

				if player.has_action():
					self.take_turn(player)
				else:
					player.has_passed = True

				turn_marker = (turn_marker + 1) % self.num_players

			self.end_round()

		self.end_game()