import math

class Board(object):
	"""Definerer storrelsen af kortet. Det er meget vigtigt er height er et multiplum af zones"""
	def __init__(self, width, height, zones):
		self.width=width
		self.height=height
		self.zones=zones

		self.zone_map = [[0 for x in range(width)] for y in range(height)]
		self.vote_map = [[0 for x in range(width)] for y in range(height)]

		"""Indeler raekkerne i zoner"""
		for y in range(0,self.height):
			self.zone_map[y]=[math.floor(y*self.zones/self.height)]*self.width


	"""Loader stemmer fra en fil"""
	def load(self, path):
		x=0
		y=0


		"""Looper over hver linje i filen"""
		fil = open(path,"r")
		for line in fil:
			for vote in list(line):
				if vote!="+" and vote!="\n":
					self.vote_map[y][x]=vote
					x+=1
			x=0
			y+=1

	def switch(self,x,y):
		neighbors = set()

		"""Tilfojer zone-tallene til et saet"""
		neighbors.update(self.get_set_zone(x+1,y))
		neighbors.update(self.get_set_zone(x-1,y))
		neighbors.update(self.get_set_zone(x,y+1))
		neighbors.update(self.get_set_zone(x,y-1))

		"""Fjerner cellens egen zone"""
		neighbors.discard(self.zone_map[y][x])


		"""Aendrer cellen hvis saettet har storrelse 1"""
		if len(neighbors)==1:
			self.zone_map[y][x]=neighbors.pop()

	def get_set_zone(self, x, y):
		try:
			returning = set([self.zone_map[y][x]])
		except IndexError:
			returning = set()
		return returning

	def zone_size(self,zoneNr):
		count = 0
		for y in range(self.height):
			for x in range(self.width):
				if int(self.zone_map[y][x]) == zoneNr:
					count += 1

		return count

	def cost_win(self):
		cost=0
		zone_vote=[0 for i in range(self.zones)]
		zone_count=[0 for i in range(self.zones)]
		"""Taeller stemmer i hver zone, samt antal af stemmere i hver zone"""
		for y in range(len(self.vote_map)):
			for x in range(len(self.vote_map[y])):
				zone_count[self.zone_map[y][x]]+=1
				zone_vote[self.zone_map[y][x]]+=float(self.vote_map[y][x])
		"""Vurderer om der er vundet eller tabt i hver zone"""
		win_percentage=0
		for i in range(len(zone_vote)):
			win_percentage+=zone_vote[i]/zone_count[i]
		win_percentage=win_percentage/self.zones
		return(win_percentage)

	def vote_print(self):
		print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in self.vote_map]))

	def zone_print(self):
		print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in self.zone_map]))
