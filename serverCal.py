import socket
import sys
import time
import errno
import math     
from multiprocessing import Process

ok_message = '\nHTTP/1.0 200 OK\n\n'
nok_message = '\nHTTP/1.0 404 NotFound\n\n'

def process_start(s_sock):
    s_sock.send(str.encode(" _____________________________________\n|         SIMPLE CALCULATOR           |\n|_____________________________________|\n|       AVAILABLE OPERATIONS :        |\n|    log  - Logarithmic Function      |\n|    sqrt - Square Root Function      |\n|    exp  - Exponential Function      |\n|                                     |\n|                                     |\n|          EXAMPLE : sqrt 8           |\n|                                     |\n| Type 'exit' to close the calculator |\n|_____________________________________|\n"))
                    
    while True:
        data = s_sock.recv(2048)                        
        data = data.decode("utf-8")
        
        try:
            operation, value = data.split()
            op = str(operation)
            num = int(value)
        
            if op[0] == 'l':
                op = 'Log'
                answer = math.log10(num)
            elif op[0] == 's':
                op = 'Square root'
                answer = math.sqrt(num)
            elif op[0] == 'e':
                op = 'Exponential'
                answer = math.exp(num)
            else:
                answer = ('ERROR : Please choose one of the available operations !')
        
            sendAnswer = (str(op) + '(' + str(num) + ') = ' + str(answer))
            print ('Answer Generated Successfully')
            
        except:
            print ('Invalid Input')
            sendAnswer = ('Invalid Input')
    
        
        if not data:
            break
            
        s_sock.send(str.encode(sendAnswer))
    s_sock.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",8828))                                   
    print("listening...")
    s.listen(28)                                         
    
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                p = Process(target=process_start, args=(s_sock,))
                p.start()

            except socket.error:

                print('socket error')

            except Exception as e:        
                print("an exception occurred!")
                print(e)
                sys.exit(1)
    finally:
     	   s.close()
