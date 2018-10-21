import pymysql
import unittest
import sys
import socket
import pickle
from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths
import test


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

		def find_default_path(self, pgraph):
			con = pymysql.connect(host='localhost', user='root', password='1', db='drive2', charset='utf8')


			curs = con.cursor()
		
			#  sql = "SELECT id , MIN(6371*acos(cos(radians({0}))*cos(radians(gps.lat))*cos(radians(gps.lon) - radians({1})) + sin(radians({2}))*sin(radians(gps.lat)))) AS distance , lat, lon FROM jcm_drive.gps where id like 'A3%' group by id order by distance limit 4".format(x,y,x);
			#  tonode_sql = "select tonode from drive2.a3_link_view where fromnode= "
			#  curs.execute(tonod_sql+"'" +linkId+"';")
	
			#  to_node=curs.fetchall()
			# '155M10640204', 155M10660204, 155M10680204, 155M10690204,155M10720204,155M10740204, 155M10760204, 155M10790204a
			node_list = []
			node = ['155M10640204','155M10690204','155M10660204','155M10720204','155M10740204','155M10810204']
			path=test.Tests()
			result = path.find_short_path(pgraph,'155M10630204','155M10720204',node)
			node_list+=result
			print(node_list)
			return node_list


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('{0} <BIND IP>'.format(sys.argv[0]))
		sys.exit()
	
	graph_object=test.Tests()
	r_graph = graph_object.make_graph()
	ip = sys.argv[1]
	port = 7429
	print('{0} server start'.format(ip))
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, port))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				print(data)
				if not data:
					break
	ps = passenger()
	nodes = ps.find_default_path(r_graph)


