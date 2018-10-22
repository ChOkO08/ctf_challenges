# coding: utf-8

#### CHALLENGE - AsciiNumberz
#### AUTHOR - ChOkO
#### OBS: alterar IP e PORT (hardcoded, veja abaixo no XXX)
#### LEMBRAR DE VERIFICAR SE O FORMATO DA FLAG ESTÁ CORRETO!

import random
import socket
import time
import thread

# Gera um numero aleatório no intervalo [a, b]
def geraRandom(a, b):
    return random.randint(a, b)

linha = "_,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,_\n"
chall="""
   ___
  / _ \\
 | | | |
 | |_| |
  \___/
######
   _
  / |
  | |
  | |
  |_|
######
  ____
 |___ \\
   __) |
  / __/
 |_____|
######
  _____
 |___ /
   |_ \\
  ___) |
 |____/
######
  _  _
 | || |
 | || |_
 |__   _|
    |_|
######
  ____
 | ___|
 |___ \\
  ___) |
 |____/
######
   __
  / /_
 | '_ \\
 | (_) |
  \___/
######
  _____
 |___  |
    / /
   / /
  /_/
######
   ___
  ( _ )
  / _ \\
 | (_) |
  \___/
######
   ___
  / _ \\
 | (_) |
  \__, |
    /_/

"""

# Faz uma lista de 10 posições com cada número (0 a 9)~
ascii_numbers=chall.split("######")

# Retorna uma string contendo o número em ASCII ~
def printAsciiNumber(x):
    asciinum = ""
    asciinum += linha
    #asciinum += "\n"
    for i in str(x):
        asciinum += str(ascii_numbers[int(i)])
    asciinum += "\n"
    #print "[ DEBUG ] ASCII GENERATED: \n%s\n" % asciinum
    return asciinum

# XXX ALTERAR HOST!!! XXX
HOST = "0.0.0.0"
PORT = 1337

def conectado(con, cliente):
    acertos = 0
    print '[+] Cliente: ', cliente
    con.send("\nOPA:) E ae beleza? Essa eh bem simples, basta ganhar 500 rounds, ok?:)\nReady? GO!!!\n")
    for i in range(1, 501): # Roda 500 rounds ~
    #for i in range(1,3): # TESTE 2 rounds ~
        flag = ''
        numero = geraRandom(10, 9999)
        con.send("\n---[ ROUND  %s of 500 ]---\n" % i)
        #print "\n[ DEBUG ] random = %s\n" % numero

        # Envia o número aleatório
        #print '[ DEBUG ] Enviando random...'
        flag = printAsciiNumber(numero)
        con.send(str(flag))

        #print '[ DEBUG ] Aguardando resposta...'
        # OBS: o timeout é de 3,5s ... setado lá embaixo.. no con.settimeout!
        con.send("\n[*] Answer: ")
        time.sleep(2)

        # Trata o recebimento e compara a resposta recebida ~
        msg = con.recv(8)
        #print '[ DEBUG ] Resposta recebida: %s' % msg
        if not msg: break

        # XXX - Tratar exceção qdo não vier INT ... Mas isso não bricka o server (até onde testei)
        elif int(msg) == numero:
            con.send("\n[!] CERTA RESPOSTA! \o/ TÁ VOANDO! GO GO GO!\n")
            acertos += 1
            #print '[ DEBUG ] Enviando a flag...'
            if acertos == 500:
                #con.send("\n\n\n\o/ !CONGRATZ! \o/\n\n ---> Here is your flag: ANDSEC{th4t5_caLL3d_FL4G_0r13Nt3d_Pr0gr4Mm1Ng!}\n\n\n")
                con.send("\n\n\n\o/ !CONGRATZ! \o/\n\n ---> Eis a sua flag: th4t5_caLL3d_FL4G_0r13Nt3d_Pr0gr4Mm1Ng!\n\n\n")
                print '[!] Flag enviada para: ', cliente
                con.close()
                thread.exit()
        else:
            #con.send("\n[!] NOOOOOOOOOO!!!! :( Carajo... you failed miserably, bro! ##NO TÁ BOM!! :\ ): \n #n00bzDetected! #gg #norev #tchau!\n\n")
            con.send("\n[!] NOOOOOOOOOO!!!! :( Putz... vc falhou miseravelmente! Tente outra vez! \n #n00bzDetected! #gg #norev #tchau!\n\n")
            print '[!] N00b detected @', cliente
            con.close()
            thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

print '[ DEBUG ] Iniciando TCP Server @ %s:%s\n' % (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
print '[ DEBUG ] Aguardando conexão...'
while True:
    con, cliente = tcp.accept()
    # XXX - Tratar exceção quando o timeout não for respeitado ~
    con.settimeout(3.5)
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
