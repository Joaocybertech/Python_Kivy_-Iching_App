import dicionario_hexagrama
from datetime import datetime
class IChingCalculator:
        
        def __init__(self, numero, hora, custom_name=''):
            self.trigrama1, self.trigrama2, self.linha_movel = self.calcula_trigramas_e_linha(numero, hora)
            self.custom_name = custom_name

        def hora_animal_chines(self):
            now_local = datetime.now()
            hora = now_local.hour
            minuto = now_local.minute

            if (23 <= hora and minuto >= 0) or (0 <= hora < 1):
                return 1  # Rato
            elif 1 <= hora < 3:
                return  2  # Boi
            elif 3 <= hora < 5:
                return 3  # Tigre
            elif 5 <= hora < 7:
                return 4  # Coelho
            elif 7 <= hora < 9:
                return 5  # Dragão
            elif 9 <= hora < 11:
                return 6  # Serpente
            elif 11 <= hora < 13:
                return 7  # Cavalo
            elif 13 <= hora < 15:
                return 8  # Cabra
            elif 15 <= hora < 17:
                return 9  # Macaco
            elif 17 <= hora < 19:
                return 10  # Galo
            elif 19 <= hora < 21:
                return 11  # Cachorro
            elif 21 <= hora < 23:
                return 12  # Porco
        
        def calcula_trigramas_e_linha(self, numero, hora):
            hora = self.hora_animal_chines ()
            primeiro_trigrama = numero % 8
            segundo_numero = numero + hora
            segundo_trigrama = segundo_numero % 8
            linha_movel = segundo_numero % 6
            if linha_movel == 0: 
                linha_movel = 6
            return primeiro_trigrama, segundo_trigrama, linha_movel, 
        
        def trigramas(self, trigrama1, trigrama2):
                trigramas = {
                    0: ('Terra', '-- --', '-- --', '-- --'),
                    1: ('Céu', '-----', '-----', '-----'),
                    2: ('Lago', '-- --', '-----', '-----'),
                    3: ('Fogo', '-----', '-- --', '-----'),
                    4: ('Trovão', '-- --', '-- --', '-----'),
                    5: ('Vento', '-----', '-----', '-- --'),
                    6: ('Água', '-- --', '-----', '-- --'),
                    7: ('Montanha', '-----', '-- --', '-- --'),
            }   
                nome1, linha1_1, linha2_1, linha3_1 = trigramas[trigrama1]
                nome2, linha1_2, linha2_2, linha3_2 = trigramas[trigrama2]
                return nome1, linha1_1, linha2_1, linha3_1, nome2, linha1_2, linha2_2, linha3_2
        def linhas_para_trigrama(self, linhas):
              inverso_trigramas = {
                 ('-- --', '-- --', '-- --'): 0,
                        ('-----', '-----', '-----'): 1,
                        ('-- --', '-----', '-----'): 2,
                        ('-----', '-- --', '-----'): 3,
                        ('-- --', '-- --', '-----'): 4,
                     ('-----', '-----', '-- --'): 5,
                    ('-- --', '-----', '-- --'): 6,
                 ('-----', '-- --', '-- --'): 7,
                     }
              return inverso_trigramas[linhas]

class HexagramaInicial(IChingCalculator):
        def __init__(self, numero, hora, custom_name=''):
            super().__init__(numero, hora,custom_name='')
            self.hexagrama = dicionario_hexagrama.Hexagrama() 
            
            nome1, linha1_1, linha2_1, linha3_1, nome2, linha1_2, linha2_2, linha3_2 = super().trigramas(self.trigrama1, self.trigrama2)
            self.linhas = [linha3_2, linha2_2, linha1_2, linha3_1, linha2_1, linha1_1,]
            self.numero = numero  
            self.hora = hora  
            if self.linha_movel == 6:  
                self.linhas[-1] = self.linhas[-1] + " X"
            elif self.linha_movel == 5:  
                self.linhas[-2] = self.linhas[-2] + " X"
            elif self.linha_movel == 4:  
                self.linhas[-3] = self.linhas[-3] + " X"
            elif self.linha_movel == 3:  
                self.linhas[2] = self.linhas[2] + " X"
            elif self.linha_movel == 2:  
                self.linhas[1] = self.linhas[1] + " X"
            elif self.linha_movel == 1:  
                self.linhas[0] = self.linhas[0] + " X"
            
            self.nome_hexagrama = self.hexagrama.get_nome_hexagrama(self.trigrama2, self.trigrama1)  

        def __str__(self):
             
             hexagrama = '\n'.join(self.linhas[::-1])
             return hexagrama
        def to_dict(self):
            return {
                'numero': self.numero,
                'hora': self.hora,
                'trigrama1': self.trigrama1,
                'trigrama2': self.trigrama2,
                'linha_movel': self.linha_movel,
                'nome_hexagrama': self.nome_hexagrama,
                'linhas': self.linhas
    }
        @classmethod
        def from_dict(cls, data):
            hexagrama_inicial = cls(
                numero=data['numero'],
                hora=data['hora'],
                custom_name=data.get('custom_name', ''))
            hexagrama_inicial.linhas = data['linhas']
            
            hexagrama_inicial.trigrama1 = data['trigrama1']
            hexagrama_inicial.trigrama2 = data['trigrama2']
            hexagrama_inicial.linha_movel = data['linha_movel']
            hexagrama_inicial.nome_hexagrama = data['nome_hexagrama']
            return hexagrama_inicial


class HexagramaNuclear(HexagramaInicial):
    def __init__(self, numero, hora, **kwargs):
        super().__init__(numero, hora, **kwargs)
        linhas_nucleares = [self.linhas[1], self.linhas[2], self.linhas[3], self.linhas[2], self.linhas[3], self.linhas[4]]
        
        self.linhas = [line.replace(" X", "") for line in linhas_nucleares]
        self.numero = numero  
        self.hora = hora  
        self.trigrama_inferior = self.linhas_para_trigrama((self.linhas[2], self.linhas[1], self.linhas[0]))  
        self.trigrama_superior = self.linhas_para_trigrama((self.linhas[5], self.linhas[4], self.linhas[3]))                

        self.nome_hexagrama_nuclear = self.hexagrama.get_nome_hexagrama(self.trigrama_inferior, self.trigrama_superior)

   
    def to_dict(self):
                 return {
                'trigrama_inferior': self.trigrama_inferior,
                'trigrama_superior': self.trigrama_superior,
                'numero': self.numero,
                'hora': self.hora,
                'nome_hexagrama': self.nome_hexagrama_nuclear,
                'linhas': self.linhas
            }

    @classmethod
    def from_dict(cls, data):
                            hexagrama_nuclear = cls(numero=data['numero'],
                                                        hora=data['hora'],
                                                        custom_name=data.get('custom_name', ''))
                            hexagrama_nuclear.trigrama_inferior = data['trigrama_inferior']
                            hexagrama_nuclear.trigrama_superior = data['trigrama_superior']
                            hexagrama_nuclear.linhas = data['linhas']
                            hexagrama_nuclear.nome_hexagrama_nuclear = data ['nome_hexagrama']
                            return hexagrama_nuclear
    def __str__(self):
                     
                        hexagrama = '\n'.join(self.linhas[::-1])
                        return hexagrama
        
class HexagramaMudanca(HexagramaInicial):
        def __init__(self, numero, hora, **kwargs):
            super().__init__(numero, hora, **kwargs)
            linhas_mudadas = self.linhas.copy()
            self.linhas_mudadas = []
            for linha in linhas_mudadas:
                if " X" in linha:  
                    if '-- --' in linha:
                        self.linhas_mudadas.append('-----')
                    elif '-----' in linha:
                        self.linhas_mudadas.append('-- --')
                else:
                    self.linhas_mudadas.append(linha)

           
            
            trigrama1 = self.linhas_para_trigrama((self.linhas_mudadas[2], self.linhas_mudadas[1], self.linhas_mudadas[0]))   
            trigrama2 = self.linhas_para_trigrama((self.linhas_mudadas[5], self.linhas_mudadas[4], self.linhas_mudadas[3])) 
            self.nome_hexagrama_mudado = self.hexagrama.get_nome_hexagrama(trigrama1, trigrama2)   
        def __str__(self):
               
            hexagrama = '\n'.join(self.linhas_mudadas[::-1])  
            return hexagrama
        def to_dict(self):
                return {
                    'numero': self.numero,
                    'hora': self.hora,
                    'linhas_mudadas': self.linhas_mudadas,
                    'nome_hexagrama_mudado': self.nome_hexagrama_mudado,
                }
        @classmethod
        def from_dict(cls, data):
            hexagrama_mudanca = cls(data['numero'], data['hora'])
            hexagrama_mudanca.linhas_mudadas = data['linhas_mudadas']
            hexagrama_mudanca.nome_hexagrama_mudado = data['nome_hexagrama_mudado']
            return hexagrama_mudanca 
