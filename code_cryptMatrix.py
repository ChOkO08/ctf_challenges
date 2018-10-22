#!/usr/bin/env python
#coding:utf-8

# Author: RTFM[ChOkO]

import socket
import string
import sys
import random
from thread import *

if len(sys.argv) > 2:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
else:
        print '[*] Usage: python %s <HOST> <PORT>\n' % sys.argv[0]
        exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print '[*] Socket created'

try:
        s.bind((HOST, PORT))
except socket.error as e:
        print '[*] Bind failed!\n - Error code: %s\n - Message: %s\n' % (str(e[0]),e[1])
        exit()

print '[*] Socket bind complete'
s.listen(10)
print '[*] Listening on %s:%s \n' % (HOST, str(PORT))

# Ideia do chall: a cada nova conexao no servico o usuario recebe uma matriz diferente que gera um novo ciphertext~

def clientThread(conn):

        flag = """"This is your last chance. After this, there is no turning back. You take the blue pill - the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill - you stay in Wonderland and I show you how deep the rabbit-hole goes...". It seems you have potential. This flag unlocks the challenge at port 1338 of this host.. Here you go: Crypt0M4tr1x_B4byL3v3L_H4PpY_h@Ck1NG! """

        # Cria uma lista com o nosso alfabeto ~ 
        alfa = string.printable
        #alfa_list = list(alfa[:36]) # tah muito pequeno :b
        alfa_list = list(alfa[:95])

        # Cria uma matriz NxN zerada - se for fazer soh com alfa[:36]
        #i,j = 6,6
        i,j = 10,10

        # Inicializa a Matriz
        M = [[0 for x in range(i)] for y in range(j)]

        # Embaralha o alfabeto  # Vai ter que rolar a cada conexao esse shuf e a geracao do alfabeto~
        random.shuffle(alfa_list)
        shuf_list = alfa_list
        shuf_dict = {}
        x = y = k = 0

        # Inicializando o dicionario 
        for x in range(i):
            for y in range(j):
                try:
                    if k > len(shuf_list):
                    #shuf_dict[''] = '%s%s' % (x,y)
                        continue 
                    else:
                        shuf_dict[str(shuf_list[k])] = '%s%s' % (x,y)
                        M[x][y] = str(shuf_list[k])
                    k += 1
                except:
                    continue

        chall = ''

        for f in flag:
            #print "%s = %s" % (f, shuf_dict.get(f))
            chall += shuf_dict.get(f)

        banner = """
          __|             |         \  |       |     _)      
         (     _||  | _ \  _|  _ \ |\/ |  _` |  _|  _||\ \ / 
        \___|_| \_, |.__/\__|\___/_|  _|\__,_|\__|_| _| _\_\ 
                ___/_|                                       
        """

        mat = ''

        mat += '--------------------\n'
        for x in range(i):
            for y in range(j):
                #print M[x][y],
                mat += str(M[x][y]) + ' '
            mat += '\n'
        mat += '--------------------\n'

        sendit = '%s\n\n Receiving transmission... \n Direto ao ponto: para obter a flag decifre: %s de acordo com a matriz a seguir:\n%s\n\n\n[!] OBS: Se o challenge cair, tente novamente dentro de 1 min!' % (banner,chall.replace(' ',''), mat)
        # Resolvi arrancar os spaces com chall.replace(' ','') pq ia ficar muito na cara que sao coordenadas -_- viva o guess \o/ hu3

        conn.sendall(sendit+'\n')
        conn.close()

while 1:
        conn, addr = s.accept()
        print '[+] New client --> %s:%s\n' % (addr[0],str(addr[1]))
        start_new_thread(clientThread, (conn,))

s.close()
