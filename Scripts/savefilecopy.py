import json
from datetime import datetime
from Meihua import HexagramaInicial, HexagramaMudanca, HexagramaNuclear

class SaveManager:
    def __init__(self):
        self.saved_questions = []
        self.save_counter = 1

    def save_question(self, hexagrama_inicial, hexagrama_nuclear, hexagrama_mudanca, custom_name=""):
        consulta_data = {
            'hexagrama_inicial': hexagrama_inicial.to_dict(),
            'hexagrama_nuclear': hexagrama_nuclear.to_dict(),
            'hexagrama_mudanca': hexagrama_mudanca.to_dict(),
            'saved_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'custom_name': custom_name
        }
        self.saved_questions.append(consulta_data)
        self.save_to_file()

    def save_to_file(self):
        try:
            with open('saved_questions.json', 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        with open('saved_questions.json', 'w') as file:
            all_data = existing_data + self.saved_questions
            json.dump(all_data, file)

    def load_saved_questions(self):
        try:
            with open('saved_questions.json', 'r') as file:
                data = json.load(file)
                self.saved_questions = [
                    {
                        'hexagrama_inicial': HexagramaInicial.from_dict(d['hexagrama_inicial']),
                        'hexagrama_nuclear': HexagramaNuclear.from_dict(d['hexagrama_nuclear']),
                        'hexagrama_mudanca': HexagramaMudanca.from_dict(d['hexagrama_mudanca']),
                        'saved_date': d['saved_date'],
                        'custom_name': d['custom_name']
                    } 
                    for d in data
                ]

        except FileNotFoundError:
            self.saved_questions = []
        return self.saved_questions