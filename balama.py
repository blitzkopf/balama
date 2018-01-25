from minerapi import Cgminer
import argparse
import graphite
import data_collector



parser = argparse.ArgumentParser(description='Collect performance data from cgminers.')
parser.add_argument('--interval','--interval-seconds','-i', metavar='interval',
                   help='seconds to wait between data collections ')
parser.add_argument('--repeats','-repeat-count','-r', metavar='repeats',
                   help='number of data collections before exiting ')
parser.add_argument('--server','--graphite-server','-s', metavar='server',
                   help='seconds to wait between data collections ',default='localhost')
parser.add_argument('hosts', metavar='host', nargs='+',	
                   help='hostname to collect data from ')

args = parser.parse_args()

sender = graphite.Sender(server=args.server)

for host in args.hosts:
  cgminer = Cgminer(host=host)
  coll = data_collector.Collector(cgminer,host,sender, repeats=int(args.repeats)) 
  coll.start()

