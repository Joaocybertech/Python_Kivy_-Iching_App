import datetime
import random

class Oraculo:
    def __init__(self):
        self.pergunta = ""

    def set_pergunta(self, pergunta):
        self.pergunta = pergunta
        return pergunta

    def numero_pergunta(self):
        numero = len(self.pergunta.replace(" ",""))
        if numero == 0:
            numero = random.randint(8, 1000)
        elif numero < 8:
            numero += 8
        return numero

    def numero_aleatorio(self):
        return random.randint(8, 1000)

    def numero_hora(self):
        now = datetime.datetime.now()
        return int(now.strftime("%H%M"))

def main():
    oraculo = Oraculo()
    print("Por favor, escolha um método para gerar um número:")
    print("1. A partir de uma pergunta.")
    print("2. De forma aleatória.")
    print("3. A partir da hora atual.")
    choice = input("Escolha uma opção (1-3): ")

    if choice == "1":
        pergunta = input("Por favor, digite sua pergunta: ")
        oraculo.set_pergunta(pergunta)
        numero = oraculo.numero_pergunta()
    elif choice == "2":
        numero = oraculo.numero_aleatorio()
    elif choice == "3":
        numero = oraculo.numero_hora()
    else:
        print("Escolha inválida.")
        return