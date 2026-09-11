# JARVIS OS V5 - Versión Final para APK
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.core.window import Window
from datetime import datetime
import webbrowser
import re

# Configuración importante para APK
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('kivy', 'log_level', 'info')
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'multisamples', '0')

Window.softinput_mode = 'below_target'

try:
    from jnius import autoclass
    ANDROID = True
except:
    ANDROID = False

BG_COLOR = (0.005, 0.01, 0.05, 0.9)

class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0.0, 0.65, 1.0, 0.85)
        self.color = (1, 1, 1, 1)
        self.font_size = 19
        self.bold = True
        self.size_hint = (None, None)
        self.size = (260, 72)

class FuturisticScreen(Screen):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        
        with root.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        title_label = Label(
            text=f"[b]{title}[/b]",
            markup=True,
            font_size=34,
            color=(0, 0.8, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.93}
        )
        root.add_widget(title_label)

        self.content = BoxLayout(orientation="vertical", spacing=10, padding=15,
                                size_hint=(0.95, 0.85), pos_hint={'center_x': 0.5, 'center_y': 0.48})
        root.add_widget(self.content)

        home = NeonButton(text="⌂ INICIO")
        home.background_color = (0.25, 0.25, 0.3, 1)
        home.size = (180, 55)
        home.pos_hint = {'center_x': 0.5, 'y': 0.02}
        home.bind(on_press=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

    def go_home(self, instance):
        if self.manager:
            self.manager.current = "home"

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class JarvisApp(App):
    def popup(self, t, m):
        Popup(title=t, content=Label(text=str(m), padding=15), size_hint=(0.9, 0.55)).open()

    def open_app(self, package_name, app_name):
        if not ANDROID:
            self.popup("Modo PC", f"Intentando abrir {app_name}")
            return
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            intent = Intent(Intent.ACTION_MAIN)
            intent.addCategory(Intent.CATEGORY_LAUNCHER)
            intent.setPackage(package_name)
            PythonActivity.mActivity.startActivity(intent)
            self.popup("JARVIS", f"Abriendo {app_name}...")
        except:
            self.popup("Error", f"No se pudo abrir {app_name}\n¿Está instalado?")

    def open_url(self, url, name):
        try:
            webbrowser.open(url)
            self.popup("Navegador", f"Abriendo {name}...")
        except:
            self.popup("Error", "No se pudo abrir el navegador")

    def process_ia_command(self, user_input, chat_label, scroll):
        if not user_input or not user_input.strip():
            return
            
        text = user_input.lower().strip()
        chat_label.text += f"\n[color=00ccff][b]Tú:[/b][/color] {user_input}\n"
        
        response = "Entendido. ¿En qué más te ayudo?"

        if any(g in text for g in ["hola", "buenos", "saludos", "jarvis"]):
            response = "¡Hola! Soy JARVIS OS V5. ¿Qué deseas hacer?"
        
        elif any(p in text for p in ["cómo estás", "que tal"]):
            response = "Estoy funcionando perfectamente, gracias 😊"
        
        elif "qué hora" in text or "que hora" in text:
            response = f"La hora actual es {datetime.now().strftime('%H:%M:%S')}"
        
        elif "qué día" in text or "que día" in text:
            response = f"Hoy es {datetime.now().strftime('%A, %d de %B de %Y')}"

        # Abrir aplicaciones
        elif "whatsapp" in text:
            self.open_app("com.whatsapp", "WhatsApp")
            response = "Abriendo WhatsApp..."
        elif "instagram" in text:
            self.open_app("com.instagram.android", "Instagram")
            response = "Abriendo Instagram..."
        elif "youtube" in text:
            self.open_app("com.google.android.youtube", "YouTube")
            response = "Abriendo YouTube..."
        elif "minecraft" in text:
            self.open_app("com.mojang.minecraftpe", "Minecraft")
            response = "Abriendo Minecraft..."

        # Calculadora
        elif any(op in text for op in ["suma", "resta", "+", "-", "*", "por"]):
            try:
                expr = re.sub(r'[^\d\+\-\*/\.]', '', text)
                if expr:
                    result = eval(expr)
                    response = f"El resultado es: **{result}**"
            except:
                response = "No pude calcular eso. Ejemplo: suma 25 + 30"

        # Búsquedas
        elif "busca en youtube" in text or "youtube" in text:
            query = text.split("youtube", 1)[-1].strip()
            if query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
                response = f"Buscando en YouTube: **{query}**"
        elif "busca" in text or "google" in text:
            query = text.replace("busca", "").replace("google", "").strip()
            if query:
                webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
                response = f"Buscando en Google: **{query}**"

        else:
            response = "Prueba diciendo:\n• abre whatsapp\n• qué hora es\n• suma 45 + 20\n• busca en youtube música"

        chat_label.text += f"[color=00ff88][b]JARVIS:[/b][/color] {response}\n"
        scroll.scroll_y = 0

    def ia_screen(self, screen):
        scroll = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        chat_label = Label(
            text="[color=00ff88][b]JARVIS:[/b][/color] ¡Hola! Prueba comandos como:\n• abre whatsapp\n• qué hora es\n• suma 8 * 12",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            padding=[15, 15]
        )
        chat_label.bind(size=chat_label.setter('text_size'))
        scroll.add_widget(chat_label)

        input_box = BoxLayout(size_hint=(1, 0.3), spacing=10, orientation='vertical', padding=[10,5])
        
        user_input = TextInput(
            hint_text="Escribe aquí y presiona Enter...",
            multiline=False,
            size_hint=(1, 0.65),
            font_size=18
        )
        
        def send_message(instance):
            self.process_ia_command(user_input.text, chat_label, scroll)
            user_input.text = ""

        user_input.bind(on_text_validate=send_message)
        
        send_btn = NeonButton(text="ENVIAR")
        send_btn.size_hint = (1, 0.35)
        send_btn.bind(on_press=send_message)

        input_box.add_widget(user_input)
        input_box.add_widget(send_btn)
        screen.content.add_widget(scroll)
        screen.content.add_widget(input_box)

    def build(self):
        sm = ScreenManager(transition=SlideTransition(duration=0.4))
        sm.add_widget(Home(name="home"))

        pantallas = ["sistema","web","juegos","social","media","util","ia","config"]
        titulos = ["SISTEMA","WEB","JUEGOS","SOCIAL","MULTIMEDIA","UTILIDADES","IA","CONFIGURACIÓN"]

        for title, name in zip(titulos, pantallas):
            screen = FuturisticScreen(title, name=name)
            
            if name == "ia":
                self.ia_screen(screen)
            elif name == "web":
                web_options = [
                    ("🌐 Google", "https://google.com"),
                    ("📺 YouTube", "https://youtube.com"),
                    ("📸 Instagram", "https://instagram.com"),
                    ("🐦 X", "https://x.com")
                ]
                for text, url in web_options:
                    btn = NeonButton(text=text)
                    btn.bind(on_press=lambda x, u=url, t=text: self.open_url(u, t))
                    screen.content.add_widget(btn)
            else:
                screen.content.add_widget(Label(text="Sección en desarrollo", font_size=22))
            
            sm.add_widget(screen)

        return sm

class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        try:
            bg = Image(source='background.jpg', allow_stretch=True, keep_ratio=False, opacity=0.75)
            root.add_widget(bg)
        except:
            with root.canvas.before:
                Color(0.005, 0.01, 0.06, 1)
                self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

        title = Label(text="[b]J.A.R.V.I.S[/b]", markup=True, font_size=50, 
                     color=(0, 0.85, 1, 1), pos_hint={'center_x': 0.5, 'top': 0.9})
        root.add_widget(title)

        subtitle = Label(text="Artificial Assistant OS V5", font_size=20, 
                        color=(0.6, 0.9, 1, 0.8), pos_hint={'center_x': 0.5, 'top': 0.8})
        root.add_widget(subtitle)

        categorias = [
            ("⚙ SISTEMA", "sistema", 0.22, 0.55),
            ("🌐 WEB", "web", 0.78, 0.55),
            ("🎮 JUEGOS", "juegos", 0.18, 0.38),
            ("👥 SOCIAL", "social", 0.82, 0.38),
            ("🎥 MEDIA", "media", 0.25, 0.20),
            ("🛠 UTIL", "util", 0.75, 0.20),
            ("🧠 IA", "ia", 0.5, 0.48),
            ("⚙ CONFIG", "config", 0.5, 0.28)
        ]

        for txt, dest, x, y in categorias:
            btn = NeonButton(text=txt)
            btn.pos_hint = {'center_x': x, 'center_y': y}
            btn.bind(on_press=lambda instance, d=dest: self.change_screen(d))
            root.add_widget(btn)

        self.add_widget(root)

    def update_rect(self, *args):
        if hasattr(self, 'rect'):
            self.rect.pos = self.pos
            self.rect.size = self.size

    def change_screen(self, screen_name):
        if self.manager:
            self.manager.current = screen_name

if __name__ == '__main__':
    JarvisApp().run()