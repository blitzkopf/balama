import queue
import threading
import pickle 
import struct 
import socket 

def queue_worker(sender):
	while True:
		msg = sender.queue.get()
		sender.send_data(msg)
		sender.queue.task_done()

class Sender:
	def __init__(self, prefix="mining.", server="localhost", port=2004, workers=0):
		self.prefix = prefix
		self.server = server
		self.port = int(port)
		self.workers = workers
		if(workers > 0):
			self.queue=Queue();
			for i in xrange(workers):
				threading.Thread(worker=queue_worker,args=(self,))

	def send(self, data, time, tags=None, section=''):
		tagstring = ''
		for key,value in tags.items():
			tagstring = tagstring+';'+key+'='+value
		pickled = ([])
		for key,value in data.items():
			pickled.append(( self.prefix + section + key+tagstring, ( time, value)))
		#print(pickled)
		payload = pickle.dumps(pickled,protocol=2)
		header = struct.pack("!L", len(payload))
		message = header + payload
		#print(message)
		if(self.workers > 0):
			self.queue(message)
		else:
			self.send_data(message)

	def send_data(self, message):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.server, self.port))
		try:
			#print('sending message ' + str(message))
			s.sendall(message)
		except OSError as  e:
		    print("could not send message:" + e.strerror	)
		    #sys.exit(1)
		s.close()
