import os
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from métodos_de_pergunta import Oraculo
from Meihua import HexagramaInicial, HexagramaNuclear, HexagramaMudanca
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from savefilecopy import SaveManager
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.button import Button
from datetime import datetime
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import json
import webbrowser
font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Roboto-Medium.ttf")
LabelBase.register("roboto", font_path)
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
       
        def open_google_docs(instance):
            webbrowser.open('https://docs.google.com/document/d/19C_B2cRXr7-4B6ZA6YTUQrZ-dZ5FFMSyCq1gtSs2X9c/edit?usp=sharing')
        with self.canvas.before:
            Color(196/255, 229/255, 254/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        relative_layout = RelativeLayout()
        
        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5})
        
        learn_button = MDRaisedButton(text='Aprenda a usar o app', size_hint=(1, 0.02), on_release=open_google_docs)
        learn_button.md_bg_color = [65/255, 105/255, 225/255, 1]
        learn_button.font_size = '18sp'
        layout.add_widget(learn_button)

        method_spinner = Spinner(
            text='ESCOLHA O MÉTODO ',
            values=(
                'BASEADO NA PERGUNTA',
                'ALEATÓRIO',
                'APARTIR DA HORA ATUAL'
            ),
            size_hint=(1, 0.06),
            font_name='roboto',
            font_size='22sp',
            color=[1, 1, 1, 1]   
        )
        layout.add_widget(method_spinner)


        question_input = MDTextField(hint_text='Digite sua pergunta', size_hint=(1, 0.5))
        question_input.color = [0, 0, 0, 1]  
        question_input.line_color_normal = [0, 0, 0, 1] 
        question_input.line_color_focus = [0, 0, 0, 1] 
        question_input.font_name = "roboto"
        question_input.font_size = '24sp'
        layout.add_widget(question_input)

        calculate_button = MDRaisedButton(text='Calcular', size_hint=(1, 0.03))
        calculate_button.md_bg_color = [65/255, 105/255, 225/255, 1]  
        calculate_button.font_size = '18sp'
        calculate_button.bind(on_press=lambda instance: self.calculate_iching(method_spinner.text, question_input.text))
        layout.add_widget(calculate_button)

        saved_button = MDRaisedButton(text='Ver Questões Salvas',size_hint=(1, 0.03), on_release=self.open_saved_questions)
        saved_button.md_bg_color = [65/255, 105/255, 225/255, 1]  
        saved_button.font_size = '18sp'
        layout.add_widget(saved_button)

        relative_layout.add_widget(layout)
        self.add_widget(relative_layout)

    def open_saved_questions(self, instance):
            app = MDApp.get_running_app()
            screen_manager = app.root

            
            screen_manager.transition = SlideTransition(direction='left')
            screen_manager.current = 'save_screen'

    
    def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

    def calculate_iching(self, choice, pergunta):
       
        oraculo = Oraculo()
        if choice == "BASEADO NA PERGUNTA":
            oraculo.set_pergunta(pergunta)
            numero = oraculo.numero_pergunta()
        elif choice == "ALEATÓRIO":
            numero = oraculo.numero_aleatorio()
        elif choice == "APARTIR DA HORA ATUAL":
            numero = oraculo.numero_hora()
        else:
            
            return

        hora = oraculo.numero_hora()
        hexagrama_inicial = HexagramaInicial(numero, hora)
        hexagrama_nuclear = HexagramaNuclear(numero, hora)
        hexagrama_mudanca = HexagramaMudanca(numero, hora)

        
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.current = 'result_screen'

        
        result_screen = screen_manager.get_screen('result_screen')
        result_screen.update_result(hexagrama_inicial, hexagrama_nuclear, hexagrama_mudanca)

class SavedQuestionsScreen(Screen):
    def __init__(self, saved_questions, **kwargs):
        super(SavedQuestionsScreen, self).__init__(**kwargs)
        self.saved_questions = saved_questions
        with self.canvas.before:
            Color(196/255, 229/255, 254/255, 1)   

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size    
    def on_pre_enter(self):
        save_manager = SaveManager()  
        self.saved_questions = save_manager.load_saved_questions()  
        self.update_saved_questions(self.saved_questions)  
    
   
    def update_saved_questions(self, saved_questions):
        self.saved_questions = saved_questions
        self.scroll = ScrollView()
        self.layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.main_layout = BoxLayout(orientation='vertical',pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.clear_widgets() 
        if saved_questions:  
            for question in saved_questions:
                custom_name = question.get('custom_name')
                if custom_name:
                    button_text = custom_name
                    button_text = f"{custom_name}"
                else:
                    saved_date = question.get('saved_date')
                    if saved_date is not None:
                        formatted_date = datetime.strptime(saved_date, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                        button_text = f"Consulta feita em {formatted_date}"

                button = MDRaisedButton(text=button_text, on_release=lambda instance, q=question: self.open_question_botoes(q), size_hint=(1, None), height=dp(40), theme_text_color="Custom", text_color=(1, 1, 1, 1), md_bg_color=(65/255, 105/255, 225/255, 1))

                
                button_delete = MDRaisedButton(text="Excluir", on_release=lambda instance, q=question: self.delete_question(q), size_hint=(None, None))

                button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(40),pos_hint={'center_x': 0.5})
                button_layout.add_widget(button)
                
                button_layout.add_widget(button_delete)

                self.layout.add_widget(button_layout)   
        else: 
            self.layout.add_widget(MDLabel(text='Nenhuma pergunta salva.', halign="center"))

        
        
        self.scroll.add_widget(self.layout) 
        self.main_layout.add_widget(self.scroll)
        more_question_button = MDRaisedButton(text='Voltar à tela inicial', on_release=self.go_to_home_screen, size_hint=(1, None), height=dp(50), theme_text_color="Custom", text_color=(1, 1, 1, 1), md_bg_color=(65/255, 105/255, 225/255, 1),pos_hint={'center_x': 0.5})
        
        self.main_layout.add_widget(more_question_button)
        
        self.add_widget(self.main_layout)
    def go_to_home_screen(self, instance):
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.transition.direction = 'right'
        screen_manager.current = 'home_screen'
        
    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
    def open_question_botoes(self, question):
        
        screen_manager = MeihuaApp.sm
        result_screen = screen_manager.get_screen('result_screen')
        
        result_screen.hexagrama_inicial = question['hexagrama_inicial']
        result_screen.hexagrama_nuclear = question['hexagrama_nuclear']
        result_screen.hexagrama_mudanca = question['hexagrama_mudanca']
        result_screen.update_result(result_screen.hexagrama_inicial, result_screen.hexagrama_nuclear, result_screen.hexagrama_mudanca)
        screen_manager.transition = SlideTransition(direction='left')
        screen_manager.current = 'result_screen'  
    def delete_question(self, question):
        
        for saved_question in self.saved_questions:
            if saved_question['saved_date'] == question['saved_date']: 
                self.saved_questions.remove(saved_question)
                break

        
        with open('saved_questions.json', 'r') as file:
            all_data = json.load(file)

      
        for data in all_data:
            if data['saved_date'] == question['saved_date']:
                all_data.remove(data)
                break

        
        with open('saved_questions.json', 'w') as file:
            json.dump(all_data, file)

    
        self.update_saved_questions(self.saved_questions)

class ResultScreen(Screen): 
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.hexagrama_inicial = None
        self.hexagrama_nuclear = None
        self.hexagrama_mudanca = None
        with self.canvas.before:
            Color(196/255, 229/ 255, 254/255, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        scroll = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        self.output_label4 = MDLabel(
            text="Inicial:",
            font_name='roboto',
            font_size='24sp',
            halign='center',
            size_hint=(1, None),
            height=50,
            markup=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1)  
        )
        self.output_label1 = MDLabel(
            text="",
            font_name='roboto',
            font_size='40sp',
            halign='center',
            size_hint=(1, None),
            height=200,
            markup=True,
            theme_text_color='Custom',
            text_color=(65/255, 105/255, 225/255, 1) 
        )
        self.output_label5 = MDLabel(
            text="Nuclear:",
            font_name='roboto',
            font_size='24sp',
            halign='center',
            size_hint=(1, None),
            height=50,
            markup=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1)  
        )
        self.output_label2 = MDLabel(
            text="",
            font_name='roboto',
            font_size='40sp',
            halign='center',
            size_hint=(1, None),
            height=200,
            markup=True,
            theme_text_color='Custom',
            text_color=(65/255, 105/255, 225/255, 1) 
        )
        self.output_label6 = MDLabel(
            text="Mudança:",
            font_name='roboto',
            font_size='24sp',
            halign='center',
            size_hint=(1, None),
            height=50,
            markup=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1)  
        )
        self.output_label3 = MDLabel(
            text="",
            font_name='roboto',
            font_size='40sp',
            halign='center',
            size_hint=(1, None),
            height=200,
            markup=True,
            theme_text_color='Custom',
            text_color=(65/255, 105/255, 225/255, 1)   
        )

        more_question_button = MDRaisedButton(text='Voltar a tela inicial', size_hint=(1, 0.08), font_name='roboto', font_size='18sp')
        more_question_button.bind(on_press=self.go_to_home_screen)

        save_question_button = MDRaisedButton(text='Salvar pergunta', size_hint=(1, 0.08), font_name='roboto', font_size='18sp')
        save_question_button.bind(on_press=self.save_question_button_pressed)
        save_question_button.md_bg_color = [65/255, 105/255, 225/255, 1]  
        more_question_button.md_bg_color = [65/255, 105/255, 225/255, 1]  
        layout.add_widget(self.output_label4)
        layout.add_widget(self.output_label1)
        layout.add_widget(self.output_label5)
        layout.add_widget(self.output_label2)
        layout.add_widget(self.output_label6)
        layout.add_widget(self.output_label3)
        layout.add_widget(more_question_button)
        layout.add_widget(save_question_button)
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def update_result(self, hexagrama_inicial, hexagrama_nuclear, hexagrama_mudanca):
        self.output_label4.text = f"Hexagrama Inicial (início): {hexagrama_inicial.nome_hexagrama}"
        self.output_label1.text = f"{hexagrama_inicial}"
        self.output_label5.text = f"Hexagrama Nuclear (desenrolar): {hexagrama_nuclear.nome_hexagrama_nuclear}"
        self.output_label2.text = f"{hexagrama_nuclear}"
        self.output_label6.text = f"Hexagrama final(conclusão): {hexagrama_mudanca.nome_hexagrama_mudado}"
        self.output_label3.text = f"{hexagrama_mudanca}"
        self.output_label4.md_bg_color = [65/255, 105/255, 225/255, 1]  
        self.output_label5.md_bg_color = [65/255, 105/255, 225/255, 1]  
        self.output_label6.md_bg_color = [65/255, 105/255, 225/255, 1] 
        self.output_label3.font_name = 'roboto'
        self.output_label3.font_size = '23sp'
        self.output_label2.font_name = 'roboto'
        self.output_label2.font_size = '23sp'
        self.output_label1.font_name = 'roboto'
        self.output_label1.font_size = '23sp'
        self.hexagrama_inicial = hexagrama_inicial
        self.hexagrama_nuclear = hexagrama_nuclear
        self.hexagrama_mudanca = hexagrama_mudanca

    def save_question_button_pressed(self, instance):
        if self.hexagrama_inicial is not None and self.hexagrama_nuclear is not None and self.hexagrama_mudanca is not None:
            box = BoxLayout(orientation='vertical')
            text_input = TextInput()  
            save_button = Button(text='Salvar')  
            box.add_widget(text_input)
            box.add_widget(save_button)
            popup = Popup(title='Digite o nome da consulta', content=box, size_hint=(None, None), size=(400, 200))

            def save_and_dismiss(button_instance):  
                custom_name = text_input.text  
                save_manager = SaveManager()
                save_manager.save_question(self.hexagrama_inicial, self.hexagrama_nuclear, self.hexagrama_mudanca, custom_name)  
                popup.dismiss()    
            
            save_button.bind(on_release=save_and_dismiss)  

            popup.open()  


    def go_to_home_screen(self, instance):
        app = MDApp.get_running_app()
        screen_manager = app.root
        screen_manager.current = 'home_screen'

class MeihuaApp(MDApp):
    sm = ScreenManager()
    def build(self):
        Window.icon = 'meu_icone.ico'
        self.icon='meu_icone.ico'
        self.sm.add_widget(HomeScreen(name='home_screen'))
        self.sm.add_widget(ResultScreen(name='result_screen'))
        self.sm.add_widget(SavedQuestionsScreen(saved_questions=[], name='save_screen'))
        return self.sm
          

if __name__ == '__main__':
    MeihuaApp().run()
