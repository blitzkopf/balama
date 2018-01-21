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
		self.version = self.miner.version()
		self.tags = {'host':hostname,'type':id_cleanup(self.version['Type'])}

	def tick(self):
		self.send_summary()
		self.send_stats()
		
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


	def run(self):
		for i in range(self.repeats):
			current_time = time.time()
			sleeptime = (self.start_time+(self.interval_sec*(i)-current_time))
			if(sleeptime>0):
				print(sleeptime) 
				time.sleep(sleeptime)
			self.tick()

