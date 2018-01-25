import threading
import time
import re

re_space = re.compile("\s")
re_pct = re.compile("%")

def id_cleanup(string):
  return re_pct.sub('_pct',re_space.sub('_',string))      

class Collector(threading.Thread):
	def __init__(self,miner,hostname,sender,interval_sec=10,repeats=1):
		self.start_time = time.time()
		super().__init__()
		self.miner = miner
		self.hostname = hostname
		self.sender = sender
		self.interval_sec = interval_sec
		self.repeats = repeats
		

	def tick(self):
		self.send_summary()
		self.send_stats()
		self.send_coin()
		self.send_pools()
		
	def send_summary(self):
		tm=int(time.time())
		summary = self.miner.summary()
		#print(summary)
		res=dict()
		for key,value in summary.items():
			res[id_cleanup(key)]=value
		self.sender.send(res,tm,self.tags,'summary.')
		#print(res)
		#return res

	def send_stats(self):
		tm=int(time.time())
		stats = self.miner.stats()
		#print(stats)
		res=dict()
		for key,value in stats[1].items():
			if(key == 'ID'):
				None
			elif(key.startswith('chain_acs')):
				res[key+'o']=value.count('o')
				res[key+'x']=value.count('x')
			else:
				res[id_cleanup(key)]=value
		self.sender.send(res,tm,self.tags,'stats.')
		#print(res)
		#return res

	def send_coin(self):
		tm=int(time.time())
		coin = self.miner.coin()
		#print(summary)
		self.sender.send({'Network_Difficulty':coin['Network Difficulty']},tm,self.tags,'coin.')

	def send_pools(self):
		tm=int(time.time())
		pools = self.miner.pools()
		i=0
		for pool in pools:
			res=self.numbers_only(pool)
			self.sender.send(res,tm,self.tags,'pools.'+str(i)+'.')
			i += 1
		
	def numbers_only(self,data):
		res=dict()
		for key,value in data.items():
			try:
				float(value)
				res[id_cleanup(key)]=value
			except ValueError:
				pass
		return res

	def run(self):
		self.version = self.miner.version()
		self.tags = {'host':self.hostname,'type':id_cleanup(self.version['Type'])}
		for i in range(self.repeats):
			current_time = time.time()
			sleeptime = (self.start_time+(self.interval_sec*(i)-current_time))
			if(sleeptime>0):
				#print(sleeptime) 
				time.sleep(sleeptime)
			self.tick()

