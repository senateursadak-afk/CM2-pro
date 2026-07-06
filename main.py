import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle

# --- PALETTE DE COULEURS HARMONISÉE (STYLE PRESTIGE / ÉDUCATION) ---
COLOR_BG_DARK = get_color_from_hex("#0F172A")      # Bleu nuit très sombre (Fond principal)
COLOR_CARD_BG = get_color_from_hex("#1E293B")      # Bleu ardoise doux (Conteneurs)
COLOR_GOLD = get_color_from_hex("#F59E0B")         # Or Ambré (Éléments clés & Ton Nom)
COLOR_TEXT_MAIN = get_color_from_hex("#F8FAFC")    # Blanc Pur (Textes importants)
COLOR_TEXT_MUTED = get_color_from_hex("#94A3B8")   # Gris Bleu (Labels secondaires)

class GrandBouton(Button):
    def __init__(self, bg_color=COLOR_CARD_BG, **kwargs):
        super().__init__(**kwargs)
        self.font_size = sp(15)
        self.bold = True
        self.background_normal = ""  
        self.background_color = bg_color    
        self.color = COLOR_TEXT_MAIN
        self.size_hint_y = None
        self.height = dp(55)

class CanvasScreen(Screen):
    def update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

# --- PROGRAMME OFFICIEL ---
FICHES_LECONS = {
    "Arithmetique": (
        "[b]CHAPITRE 1 : LES GRANDS NOMBRES ENTIERS[/b]\n"
        "• Classes : Unités, Milliers, Millions, Milliards. Chaque classe a 3 chiffres.\n"
        "• Lecture : On laisse un espace entre les classes.\n\n"
        "[b]CHAPITRE 2 : LES QUATRE OPÉRATIONS SUR LES ENTIERS[/b]\n"
        "• Addition & Soustraction : Bien aligner les unités sous les unités.\n"
        "• Multiplication : Décaler les lignes à chaque chiffre du multiplicateur.\n"
        "• Division : Dividende = (Diviseur x Quotient) + Reste.\n\n"
        "[b]CHAPITRE 3 : LES NOMBRES DÉCIMAUX[/b]\n"
        "• Aligner les virgules verticalement.\n\n"
        "[b]CHAPITRE 4 : LES FRACTIONS[/b]\n"
        "• Fraction d'une grandeur : (Valeur totale x Numérateur) / Dénominateur.\n\n"
        "[b]CHAPITRE 5 : RÈGLE DE TROIS[/b]\n"
        "• Faire d'abord la réduction à l'unité."
    ),
    "Systeme Metrique": (
        "[b]CHAPITRE 1 : LES MESURES DE LONGUEUR[/b]\n"
        "• Unité principale : Le mètre (m).\n"
        "[color=#F59E0B]| km | hm | dam |  m  | dm | cm | mm |[/color]\n\n"
        "[b]CHAPITRE 2 : LES MESURES DE MASSÉ[/b]\n"
        "• Unité principale : Le gramme (g) et le Kilogramme (kg).\n"
        "[color=#F59E0B]|  t  |  q  |  .  | kg | hg | dag |  g  |[/color]\n\n"
        "[b]CHAPITRE 3 : LES MESURES DE CAPACITÉ[/b]\n"
        "• Unité principale : Le litre (L).\n"
        "[color=#F59E0B]| hL | daL |  L  | dL | cL | mL |[/color]\n\n"
        "[b]CHAPITRE 4 : LES MESURES DE SURFACE[/b]\n"
        "[color=#F59E0B]|   km²   |   hm² (ha)   |  dam² (a)   |   m² (ca)   |[/color]\n\n"
        "[b]CHAPITRE 5 : LES MESURES DE VOLUME[/b]\n"
        "• Passerelle d'Or : 1 dm³ = 1 Litre."
    ),
    "Geometrie": (
        "[b]CHAPITRE 1 : LE CARRÉ ET LE RECTANGLE[/b]\n"
        "• Carré : Périmètre = Côté x 4 | Aire = Côté x Côté.\n"
        "• Rectangle : Périmètre = (Longueur + Largeur) x 2 | Aire = Longueur x Largeur.\n\n"
        "[b]CHAPITRE 2 : LE TRIANGLE[/b]\n"
        "• Aire = (Base x Hauteur) / 2.\n\n"
        "[b]CHAPITRE 3 : LE TRAPÈZE[/b]\n"
        "• Aire = ((Grande Base + Petite Base) x Hauteur) / 2.\n\n"
        "[b]CHAPITRE 4 : LE CERCLE ET LE DISQUE[/b]\n"
        "• Périmètre = Diamètre x 3,14 | Aire = Rayon x Rayon x 3,14.\n\n"
        "[b]CHAPITRE 5 : LES SOLIDES[/b]\n"
        "• Cube : Volume = Côté x Côté x Côté.\n"
        "• Pavé Droit : Volume = Longueur x Largeur x Hauteur."
    ),
    "Calculs Pratiques": (
        "[b]CHAPITRE 1 : LES POURCENTAGES[/b]\n"
        "• Prendre x% : (Valeur x Taux) / 100.\n\n"
        "[b]CHAPITRE 2 : LE COMPTE ET LA FACTURE[/b]\n"
        "• Montant Brut = Quantité x Prix unitaire.\n\n"
        "[b]CHAPITRE 3 : MÉCANIQUE COMMERCIALE[/b]\n"
        "• Prix de Revient = Prix d'Achat + Frais.\n"
        "• Bénéfice = Prix de Vente - Prix de Revient.\n\n"
        "[b]CHAPITRE 4 : L'INTÉRÊT ET LE CAPITAL[/b]\n"
        "• Intérêt annuel = (Capital x Taux) / 100.\n\n"
        "[b]CHAPITRE 5 : LA VITESSE MOYENNE[/b]\n"
        "• Distance = Vitesse x Temps | Vitesse = Distance / Temps."
    )
}

QUIZ_DATA = {
    "Arithmetique": [
        {"q": "Combien de chiffres contient une classe ?", "r": ["3", "2", "1", "4"], "c": "3"},
        {"q": "Le nombre 1 200 000 se lit :", "r": ["1,2 million", "120 000", "12 millions", "120 millions"], "c": "1,2 million"},
        {"q": "Calcule : 12,5 + 7,25", "r": ["19,75", "19,25", "20,75", "19,5"], "c": "19,75"},
        {"q": "Le tiers de 9000 est :", "r": ["3000", "4500", "300", "1000"], "c": "3000"},
        {"q": "Dans 45 871, quel est le chiffre des dizaines ?", "r": ["7", "8", "5", "4"], "c": "7"}
    ],
    "Systeme Metrique": [
        {"q": "1 km est égal à combien de mètres ?", "r": ["1000 m", "100 m", "10 m", "10000 m"], "c": "1000 m"},
        {"q": "1 tonne vaut combien de kilogrammes ?", "r": ["1000 kg", "100 kg", "500 kg", "2000 kg"], "c": "1000 kg"},
        {"q": "1 Litre correspond exactement à :", "r": ["1 dm³", "10 dm³", "100 dm³", "0,1 dm³"], "c": "1 dm³"},
        {"q": "Dans le tableau des m², combien y a-t-it de colonnes par unité ?", "r": ["2", "1", "3", "4"], "c": "2"},
        {"q": "1 hectare (ha) est égal à :", "r": ["100 dam²", "10 dam²", "1000 dam²", "1 dam²"], "c": "100 dam²"}
    ],
    "Geometrie": [
        {"q": "Quel est le volume d'un cube de 2m de côté ?", "r": ["8 m³", "4 m³", "6 m³", "12 m³"], "c": "8 m³"},
        {"q": "Quelle est la formule du périmètre du carré ?", "r": ["Côté x 4", "Côté x Côté", "L x l", "Côté + 4"], "c": "Côté x 4"},
        {"q": "Quelle est la formule de l'aire du rectangle ?", "r": ["L x l", "L + l", "(L + l) x 2", "L x l x H"], "c": "L x l"},
        {"q": "Combien de côtés possède un triangle ?", "r": ["3", "4", "5", "6"], "c": "3"},
        {"q": "L'aire d'un triangle est : (Base x Hauteur) / ...", "r": ["2", "4", "1", "3"], "c": "2"}
    ],
    "Calculs Pratiques": [
        {"q": "Quelle est la formule de la Vitesse ?", "r": ["Distance / Temps", "Distance x Temps", "Temps / Distance", "Distance + Temps"], "c": "Distance / Temps"},
        {"q": "Combien font 10% de 5000 ?", "r": ["500", "50", "1000", "250"], "c": "500"},
        {"q": "Prix de Vente - Prix de Revient est égal au :", "r": ["Bénéfice", "Perte", "Montant Brut", "Net à payer"], "c": "Bénéfice"},
        {"q": "Que signifie le sigle TVA ?", "r": ["Taxe sur la Valeur Ajoutée", "Taux de Vente Annuel", "Total de Vente Appliqué", "Taxe de Volontariat"], "c": "Taxe sur la Valeur Ajoutée"},
        {"q": "La formule pour trouver la Distance est :", "r": ["Vitesse x Temps", "Vitesse / Temps", "Temps / Vitesse", "Vitesse + Temps"], "c": "Vitesse x Temps"}
    ]
}

# --- PAGE DE GARDE ---
class HomeScreen(CanvasScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*COLOR_BG_DARK)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=[dp(24), dp(35), dp(24), dp(24)])
        
        # Titre Unifié avec signature Éditeur
        titre_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(110))
        titre_box.add_widget(Label(text="CM2 PRO", font_size=sp(36), bold=True, color=COLOR_GOLD, halign="center"))
        titre_box.add_widget(Label(text="PREPARATION CEP • BURKINA FASO", font_size=sp(11), bold=True, color=COLOR_TEXT_MUTED, halign="center"))
        titre_box.add_widget(Label(text="par Sénateur Technologie", font_size=sp(12), italic=True, color=COLOR_GOLD, halign="center"))
        layout.add_widget(titre_box)
        
        menu = BoxLayout(orientation='vertical', spacing=dp(12))
        
        b1 = GrandBouton(text="📚  LECONS DU PROGRAMME")
        b1.bind(on_release=lambda x: setattr(self.manager, 'current', 'lessons'))
        
        b2 = GrandBouton(text="🎯  EXERCICES & QUIZ")
        b2.bind(on_release=lambda x: setattr(self.manager, 'current', 'quiz_menu'))
        
        b3 = GrandBouton(text="ℹ️  A PROPOS")
        b3.bind(on_release=lambda x: setattr(self.manager, 'current', 'about'))
        
        b4 = GrandBouton(text="🚪  QUITTER", bg_color=get_color_from_hex("#991B1B"))
        b4.bind(on_release=lambda x: App.get_running_app().stop())
        
        menu.add_widget(b1)
        menu.add_widget(b2)
        menu.add_widget(b3)
        menu.add_widget(b4)
        
        layout.add_widget(menu)
        self.add_widget(layout)

# --- NAVIGATION ---
class LessonsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        self.header = Label(text="PROGRAMME OFFICIEL", font_size=sp(18), bold=True, color=COLOR_GOLD, size_hint_y=None, height=dp(50))
        self.layout_principal.add_widget(self.header)
        
        self.zone_contenu = BoxLayout(orientation='vertical')
        self.afficher_menu_lecons()
        self.layout_principal.add_widget(self.zone_contenu)
        
        self.btn_action_bas = GrandBouton(text="⬅️  RETOUR AU MENU")
        self.btn_action_bas.bind(on_release=self.action_bouton_bas)
        self.layout_principal.add_widget(self.btn_action_bas)
        self.add_widget(self.layout_principal)
        self.mode_lecture = False

    def afficher_menu_lecons(self):
        self.zone_contenu.clear_widgets()
        self.header.text = "PROGRAMME OFFICIEL"
        self.mode_lecture = False
        
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        liste = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        liste.bind(minimum_height=liste.setter('height'))
        
        matieres = [
            ("ARITHMETIQUE", "Arithmetique"),
            ("SYSTEME METRIQUE", "Systeme Metrique"),
            ("GEOMETRIE", "Geometrie"),
            ("CALCULS PRATIQUES", "Calculs Pratiques")
        ]
        for nom, cle in matieres:
            btn = GrandBouton(text=f"📖  {nom}")
            btn.bind(on_release=lambda x, c=cle: self.lire_fiche(c))
            liste.add_widget(btn)
            
        scroll.add_widget(liste)
        self.zone_contenu.add_widget(scroll)

    def lire_fiche(self, matiere):
        self.zone_contenu.clear_widgets()
        self.header.text = matiere.upper()
        self.mode_lecture = True
        self.btn_action_bas.text = "⬅️  RETOUR AUX MATIERES"
        
        scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        lbl = Label(
            text=FICHES_LECONS[matiere], 
            markup=True, 
            font_size=sp(14), 
            size_hint=(None, None), 
            color=[1,1,1,1], 
            halign="left",
            valign="top"
        )
        lbl.bind(texture_size=lambda s, t: setattr(lbl, 'size', (max(t[0], dp(500)), max(t[1], dp(1200)))))
        scroll.add_widget(lbl)
        self.zone_contenu.add_widget(scroll)

    def action_bouton_bas(self, instance):
        if self.mode_lecture:
            self.afficher_menu_lecons()
            self.btn_action_bas.text = "⬅️  RETOUR AU MENU"
        else:
            self.manager.current = "home"

class QuizMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        layout.add_widget(Label(text="SELECTION DU QUIZ", font_size=sp(18), bold=True, color=COLOR_GOLD, size_hint_y=None, height=dp(50)))
        
        zone = BoxLayout(orientation='vertical', spacing=dp(10))
        matieres = [
            ("ARITHMETIQUE", "Arithmetique"),
            ("SYSTEME METRIQUE", "Systeme Metrique"),
            ("GEOMETRIE", "Geometrie"),
            ("CALCULS PRATIQUES", "Calculs Pratiques")
        ]
        for nom, cle in matieres:
            b = GrandBouton(text=f"🎯  {nom}")
            b.bind(on_release=lambda x, c=cle: self.lancer_le_quiz(c))
            zone.add_widget(b)
            
        layout.add_widget(zone)
        btn_annuler = GrandBouton(text="⬅️  RETOUR AU MENU")
        btn_annuler.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_annuler)
        self.add_widget(layout)

    def lancer_le_quiz(self, matiere):
        engine = self.manager.get_screen('quiz_engine')
        engine.demarrer_session(matiere)
        self.manager.current = "quiz_engine"

class QuizEngineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        self.barre = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        self.lbl_score = Label(text="Score: 0/0", font_size=sp(14), bold=True, color=COLOR_TEXT_MAIN)
        self.lbl_chrono = Label(text="30s", font_size=sp(14), bold=True, color=COLOR_GOLD)
        self.barre.add_widget(self.lbl_score)
        self.barre.add_widget(self.lbl_chrono)
        self.layout_principal.add_widget(self.barre)
        
        self.lbl_question = Label(text="", font_size=sp(16), bold=True, color=COLOR_TEXT_MAIN, halign="center")
        self.lbl_question.bind(size=lambda s, w: setattr(self.lbl_question, 'text_size', (w[0], None)))
        self.layout_principal.add_widget(self.lbl_question)
        
        self.zone_reponses = BoxLayout(orientation='vertical', spacing=dp(8))
        self.boutons_reponses = []
        for i in range(4):
            b = GrandBouton(text="", bg_color=COLOR_CARD_BG)
            b.bind(on_release=self.verifier_reponse)
            self.boutons_reponses.append(b)
            self.zone_reponses.add_widget(b)
        self.layout_principal.add_widget(self.zone_reponses)
        
        self.btn_bas = GrandBouton(text="ABANDONNER")
        self.btn_bas.bind(on_release=self.action_btn_bas)
        self.layout_principal.add_widget(self.btn_bas)
        self.add_widget(self.layout_principal)
        
        self.evenement_chrono = None

    def demarrer_session(self, matiere):
        self.questions_session = list(QUIZ_DATA[matiere])
        random.shuffle(self.questions_session)
        self.index_actuel = 0
        self.points = 0
        self.btn_bas.text = "ABANDONNER"
        self.charger_question()

    def charger_question(self):
        self.reponse_verrouillee = False
        if self.evenement_chrono:
            Clock.unschedule(self.evenement_chrono)
            
        if self.index_actuel >= len(self.questions_session):
            self.lbl_question.text = f"Quiz termine !\nScore Final : {self.points} / {len(self.questions_session)}"
            self.zone_reponses.clear_widgets()
            self.btn_bas.text = "RETOUR"
            return
            
        if not self.zone_reponses.children:
            for b in self.boutons_reponses:
                self.zone_reponses.add_widget(b)
                
        self.donnee_q = self.questions_session[self.index_actuel]
        self.lbl_score.text = f"Question {self.index_actuel + 1}/{len(self.questions_session)}"
        self.lbl_question.text = self.donnee_q["q"]
        
        choix = list(self.donnee_q["r"])
        random.shuffle(choix)
        for i, b in enumerate(self.boutons_reponses):
            b.text = choix[i]
            b.background_color = COLOR_CARD_BG
            
        self.temps_restant = 30
        self.lbl_chrono.text = f"{self.temps_restant}s"
        self.evenement_chrono = Clock.schedule_interval(self.top_chrono, 1)

    def top_chrono(self, dt):
        self.temps_restant -= 1
        self.lbl_chrono.text = f"{self.temps_restant}s"
        if self.temps_restant <= 0:
            Clock.unschedule(self.evenement_chrono)
            self.reponse_verrouillee = True
            for b in self.boutons_reponses:
                if b.text == self.donnee_q["c"]:
                    b.background_color = get_color_from_hex("#15803D")
            self.btn_bas.text = "SUIVANT"

    def verifier_reponse(self, instance):
        if self.reponse_verrouillee:
            return
        self.reponse_verrouillee = True
        Clock.unschedule(self.evenement_chrono)
        
        bonne = self.donnee_q["c"]
        if instance.text == bonne:
            instance.background_color = get_color_from_hex("#15803D")
            self.points += 1
        else:
            instance.background_color = get_color_from_hex("#991B1B")
            for b in self.boutons_reponses:
                if b.text == bonne:
                    b.background_color = get_color_from_hex("#15803D")
        self.btn_bas.text = "SUIVANT"

    def action_btn_bas(self, instance):
        if self.btn_bas.text == "SUIVANT":
            self.index_actuel += 1
            self.charger_question()
        else:
            if self.evenement_chrono:
                Clock.unschedule(self.evenement_chrono)
            self.manager.current = "quiz_menu"


# --- ÉCRAN À PROPOS ---
class AboutScreen(CanvasScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*COLOR_BG_DARK) 
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(20))
        
        layout.add_widget(Label(text="CONCEPTEUR APPLICATION", font_size=sp(12), bold=True, color=COLOR_TEXT_MUTED, size_hint_y=None, height=dp(20)))
        
        carte_info = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(20))
        with carte_info.canvas.before:
            Color(*COLOR_CARD_BG) 
            self.carte_rect = Rectangle(size=carte_info.size, pos=carte_info.pos)
        carte_info.bind(size=lambda inst, val: setattr(self.carte_rect, 'size', val), pos=lambda inst, val: setattr(self.carte_rect, 'pos', val))
        
        # NOM
        lbl_nom = Label(text="[b][size=26]SAWADOGO BOUKARE[/size][/b]", markup=True, color=COLOR_GOLD, halign="left", size_hint_y=None, height=dp(35))
        lbl_nom.bind(size=lambda s, w: setattr(lbl_nom, 'text_size', (w[0], None)))
        
        # GRADE
        lbl_grade = Label(text="[b]Professeur Certifié des Écoles[/b]", markup=True, font_size=sp(15), color=COLOR_TEXT_MAIN, halign="left", size_hint_y=None, height=dp(25))
        lbl_grade.bind(size=lambda s, w: setattr(lbl_grade, 'text_size', (w[0], None)))
        
        # Séparateur
        lbl_separation = Label(text="________________________________________", color=COLOR_TEXT_MUTED, font_size=sp(10), halign="left", size_hint_y=None, height=dp(15))
        lbl_separation.bind(size=lambda s, w: setattr(lbl_separation, 'text_size', (w[0], None)))
        
        # Projet & Technologie Éditeur intégrée
        lbl_app = Label(text="[color=#94A3B8]Application :[/color] CM2 PRO (Préparation CEP)", markup=True, font_size=sp(14), halign="left", size_hint_y=None, height=dp(25))
        lbl_app.bind(size=lambda s, w: setattr(lbl_app, 'text_size', (w[0], None)))

        lbl_tech = Label(text="[color=#94A3B8]Développé par :[/color] [b]Sénateur Technologie[/b]", markup=True, font_size=sp(14), halign="left", size_hint_y=None, height=dp(25))
        lbl_tech.bind(size=lambda s, w: setattr(lbl_tech, 'text_size', (w[0], None)))
        
        lbl_contact = Label(text="[color=#94A3B8]Contact :[/color] +226 67 49 15 20", markup=True, font_size=sp(14), halign="left", size
      
