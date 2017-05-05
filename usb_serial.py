#!/usr/bin/env python
# *-* encoding: utf-8 *-*

import serial
from Tkinter import *
from threading import Thread
import matplotlib.pyplot as plt
from array import array
from drawnow import drawnow


class Main():
    def __init__(self, usb, valor):
        self.valor = valor
        self.flag = 0

        self.usb = usb
        t = Thread(target=self.plot_realtime, args=())
        t.start()

        self.janela = Tk()
        self.janela.title('Serial')

        #self.frame = Frame(janela)
        self.botao_liga = Button(self.janela, text='Ligar LED', command=self.liga_led)
        self.botao_liga.pack()

        self.botao_desliga = Button(self.janela, text='Desligar LED', command=self.desliga_led)
        self.botao_desliga.pack()

        self.botao_fechar = Button(self.janela, text='FECHAR', command=self.fechar_tudo)
        self.botao_fechar.pack()

        self.janela.mainloop()

    def plot_realtime(self):
        
        plt.ion()
        count=0
        while True:
            conta = 0
            while (self.usb.inWaiting()==0):
                conta+=1
                if (conta>1000):
                    print 'Conexão falha!'
                    break
                pass
            self.leitura = self.usb.readline()
            print self.leitura
            self.leitura = float(self.leitura)
            self.valor.append(self.leitura)
            drawnow(self.plotar_grafico)
            plt.pause(.00005)
            count+=1
            if(count>50):
                self.valor.pop(0)
            if(self.flag!=0):
                break

        pass

    def plotar_grafico(self):
        plt.ylim([-1,1025]) #min e max de y
        plt.title('Potenciometro')
        plt.plot(self.valor, 'bo-')
        pass

    def liga_led(self):
        self.usb.write('l')  #Envia o ascii 'l'
        pass

    def desliga_led(self):
        self.usb.write('d')  #Envia o ascii 'd'
        pass

    def fechar_tudo(self):
        self.janela.destroy()
        self.flag += 1
        pass

if __name__ == '__main__':
    
    valor = array('f')

    try:
        usb = serial.Serial('/dev/ttyUSB0', 9200, timeout=1)
    except:
        usb = serial.Serial('/dev/ttyUSB1', 9200, timeout=1)
    Main(usb, valor)