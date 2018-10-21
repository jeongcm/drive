import pymysql
import unittest
import sys
import socket
import pickle
from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths
import test
from collections import OrderedDict

class TcpHandler():

	#  def handle(self):
	#      print("client ip : {0}".format(self.client_address[0]))
	#      sock = self.request
    #
	#      __recv_msg = sock.recv(1024)
    #
	#      recv_message= str(__recv_msg, encoding='utf-8')
    #
	#      print("recv: {0}".format(recv_message))
	#  메시지 보낼때는 직접 리스트를 pickle.dump이용해서 빼낸다음 하나씩 보낼 예정
	def send_msg(self,result_list):
		ip = sys.argv[1]
		port = 7429
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connet((ip,port))
			for data  in result_list:
				print('module send data : {0}'.format(data))
				s.sendall(data)

class passenger():

		def find_default_path(self, pgraph,s,d):
			con = pymysql.connect(host='localhost', user='root', password='1', db='drive2', charset='utf8')

			curs = con.cursor()
		
			#  sql = "SELECT id , MIN(6371*acos(cos(radians({0}))*cos(radians(gps.lat))*cos(radians(gps.lon) - radians({1})) + sin(radians({2}))*sin(radians(gps.lat)))) AS distance , lat, lon FROM jcm_drive.gps where id like 'A3%' group by id order by distance limit 4".format(x,y,x);
			#  tonode_sql = "select tonode from drive2.a3_link_view where fromnode= "
			#  curs.execute(tonod_sql+"'" +linkId+"';")
	
			#  to_node=curs.fetchall()
			# '155M10640204', 155M10660204, 155M10680204, 155M10690204,155M10720204,155M10740204, 155M10760204, 155M10790204a
			node_list = []
			result_path= []
			node = ['155M10640204','155M10690204','155M10660204','155M10720204','155M10740204','155M10810204']
			path=test.Tests()
			result = path.find_short_path(pgraph,s,node)
			node_list+=result
			for path_node in node_list:
				path_result =find_path(pgraph,s,path_node)

				nodes,edges,costs,total_cost = path_result
				#  print(nodes)
				result_path+=nodes
				s= path_node
			destination_result = find_path(pgraph,s,d)
			nodes,edges,costs,total_cost = destination_result
			result_path +=nodes
			OrderedDict.fromkeys(result_path)
			return result_path


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('{0} <BIND IP>'.format(sys.argv[0]))
		sys.exit()
	result_string = ""
	graph_object=test.Tests()
	r_graph = graph_object.make_graph()
	ip = sys.argv[1]
	port = 7429
	print('{0} server start'.format(ip))
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, port))
		#  print('Connected by', addr)
		while True:
				s.listen(1)
				conn, addr = s.accept()
				data = conn.recv(1024)
				if not data :
					continue
				ps = passenger()
				nodes = ps.find_default_path(r_graph,'155M10630204','155M10820204')
				for i in range(len(nodes)):
						pop_index=nodes.pop(0)
						result_string+=str(pop_index)
						result_string+=" "
				print(result_string)
				print(data)


