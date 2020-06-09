import kivy
import os
import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage
from kivy.properties import ObjectProperty

Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '200')
Config.write()

class LoginPage(GridLayout):

    def __init__(self, **kwargs):

        super(LoginPage, self).__init__(**kwargs)

        if os.path.isfile("last_inputs.txt"):
            with open("last_inputs.txt", "r") as f:
                d = f.read().split(",")
                last_first_name = d[0]
                last_last_name = d[1]
                last_username = d[2]
        else:
            last_first_name = ""
            last_last_name = ""
            last_username = ""

        self.cols = 2
        self.add_widget(Label(text="First name: "))

        self.first_name = TextInput(text=last_first_name, multiline=False)
        self.add_widget(self.first_name)

        self.add_widget(Label(text="Last name: "))

        self.last_name = TextInput(text=last_last_name, multiline=False)
        self.add_widget(self.last_name)

        self.add_widget(Label(text="Desired username: "))

        self.username = TextInput(text=last_username, multiline=False)
        self.add_widget(self.username)

        self.solver_button = Button(text="Start Hangman Solver!")
        self.solver_button.bind(on_press=self.solver_press)
        self.add_widget(self.solver_button)

        self.start_button = Button(text="Start playing Hangman!")
        self.start_button.bind(on_press=self.start_press)
        self.add_widget(self.start_button)

    def solver_press(self, instance):

        Window.size = (700,350)

        first_name = self.first_name.text
        last_name = self.last_name.text
        username = self.username.text

        print("Starting Hangman Solver for user ", username, "...")

        with open("last_inputs.txt", "w") as f:
            f.write(f"{first_name},{last_name},{username}")

        hangman_game.screen_manager.current = "Solver"

    def start_press(self, instance):

        first_name = self.first_name.text
        last_name = self.last_name.text
        username = self.username.text

        print("Starting Hangman Game for user ", username, "...")

        with open("last_inputs.txt", "w") as f:
            f.write(f"{first_name},{last_name},{username}")

        hangman_game.screen_manager.current = "Language"

class LanguageSelection(BoxLayout):

    def __init__(self, **kwargs):

        super(LanguageSelection, self).__init__(**kwargs)

    def english(self):
        hangman_game.screen_manager.current = "HangmanEnglish"
        Window.size = (1300,700)
    def deutsch(self):
        hangman_game.screen_manager.current = "HangmanDeutsch"
        Window.size = (1300,700)

class HangmanGameEnglish(BoxLayout):

    def __init__(self, **kwargs):

        super(HangmanGameEnglish, self).__init__(**kwargs)

        self.select_word()
        self.underscores = len(self.word)*"_ "

        self.text = "[b][size=80]"+self.underscores+"[/size][/b]"
        self.ids.word.text = self.text

        self.red = [1,0,0,1]
        self.green = [0,1,0,1]

        self.wrong = 0

    def select_word(self):

        self.words = [line.strip("\n") for line in open("hangman_words_en.txt", 'r', encoding='utf-8')]
        self.word = str(random.choice(self.words))
        print(self.word)

    def letter_pressed(self, index):
        self.letter = str(index)

        self.number = self.word.count(self.letter)
        if self.number == 0:
            self.ids[index].background_color = self.red
            self.wrong += 1
            if self.wrong == 1:
                self.ids.im.source = "prog1.jpg"
            elif self.wrong == 2:
                self.ids.im.source = "prog2.jpg"
            elif self.wrong == 3:
                self.ids.im.source = "prog3.jpg"
            elif self.wrong == 4:
                self.ids.im.source = "prog4.jpg"
            elif self.wrong == 5:
                self.ids.im.source = "prog5.jpg"
            elif self.wrong == 6:
                self.ids.im.source = "prog6.jpg"
            elif self.wrong == 7:
                self.ids.im.source = "prog7.jpg"
            elif self.wrong == 8:
                self.ids.im.source = "prog8_hangman.jpg"
                hangman_game.screen_manager.current = "Lost"
        else:
            self.ids[index].background_color = self.green

        self.tick = 0
        if self.number != 0:
            while self.tick < self.number:
                self.location = self.word.find(index)
                print(self.location)

                if self.location == 0:
                    self.underscores = self.underscores[:0] +index+ self.underscores[1:]
                    print(self.underscores)
                    self.text = "[b][size=80]"+self.underscores+"[/size][/b]"
                elif self.location > 0:
                    self.loc = self.location*2
                    self.underscores = self.underscores[:self.loc] +index+ self.underscores[self.loc+1:]
                    print(self.underscores)
                    self.text = "[b][size=80]"+self.underscores+"[/size][/b]"

                self.ids.word.text = self.text
                self.word = self.word.replace(self.word[self.location], " ",1)
                print(self.word)

                if self.underscores.count("_") == 0:
                    hangman_game.screen_manager.current = "Won"


                self.tick += 1

class HangmanGameDeutsch(BoxLayout):

    def __init__(self, **kwargs):

        super(HangmanGameDeutsch, self).__init__(**kwargs)

        self.select_word()
        self.underscores = len(self.word)*"_ "

        self.text = "[b][size=80]"+self.underscores+"[/size][/b]"
        self.ids.word.text = self.text

        self.red = [1,0,0,1]
        self.green = [0,1,0,1]

        self.wrong = 0

    def select_word(self):

        self.words = [line.strip("\n") for line in open("hangman_words_de.txt", 'r', encoding='utf-8')]
        self.word = str(random.choice(self.words)).lower()
        self.word_for_later = self.word
        print(self.word)

    def letter_pressed(self, index):
        self.letter = str(index)

        self.number = self.word.count(self.letter)
        if self.number == 0:
            self.ids[index].background_color = self.red
            self.wrong += 1
            if self.wrong == 1:
                self.ids.im.source = "prog1.jpg"
            elif self.wrong == 2:
                self.ids.im.source = "prog2.jpg"
            elif self.wrong == 3:
                self.ids.im.source = "prog3.jpg"
            elif self.wrong == 4:
                self.ids.im.source = "prog4.jpg"
            elif self.wrong == 5:
                self.ids.im.source = "prog5.jpg"
            elif self.wrong == 6:
                self.ids.im.source = "prog6.jpg"
            elif self.wrong == 7:
                self.ids.im.source = "prog7.jpg"
            elif self.wrong == 8:
                self.ids.im.source = "prog8_hangman.jpg"
                hangman_game.screen_manager.current = "Lost"

                self.labeltext = "Your word was: " + self.word_for_later + "!"
        else:
            self.ids[index].background_color = self.green

        self.tick = 0
        if self.number != 0:
            while self.tick < self.number:
                self.location = self.word.find(index)
                print(self.location)

                if self.location == 0:
                    self.underscores = self.underscores[:0] +index+ self.underscores[1:]
                    print(self.underscores)
                    self.text = "[b][size=80]"+self.underscores+"[/size][/b]"
                elif self.location > 0:
                    self.loc = self.location*2
                    self.underscores = self.underscores[:self.loc] +index+ self.underscores[self.loc+1:]
                    print(self.underscores)
                    self.text = "[b][size=80]"+self.underscores+"[/size][/b]"

                self.ids.word.text = self.text
                self.word = self.word.replace(self.word[self.location], " ",1)
                print(self.word)

                if self.underscores.count("_") == 0:
                    hangman_game.screen_manager.current = "Won"


                self.tick += 1

class SolverGame(BoxLayout):

    def __init__(self, **kwargs):

        super(SolverGame, self).__init__(**kwargs)

        self.im = Image(source='prog0.jpg')
        self.add_widget(self.im)

        self.click = 0
        self.ids.submit.bind(on_press=self.submit_press)
        self.already_guessed = []

        self.tick = 0
        self.false_guesses = 0
        self.right_guesses = 0

    def submit_press(self, instance):

        if self.false_guesses == 8:

            if self.current_answer.lower() == "no":
                hangman_game.screen_manager.current = "WonSolv"
            else:
                self.tick = 2

        self.click += 1

        if self.tick == 0:

            self.current_answer = self.ids.answer.text
            self.ids.answer.text = ""
            print(self.current_answer)

            if self.current_answer.lower() == "de":
                self.list = [line.strip("\n") for line in open("wordlist_de.txt", 'r', encoding='utf-8')]
                print(len(self.list), "posibilities left...")
                self.wordlist = [x.lower() for x in self.list]
                self.tick += 1
                self.change_question()
                return
            elif self.current_answer.lower() == "en":
                self.list = [line.strip("\n") for line in open("wordlist_en.txt", 'r', encoding='utf-8')]
                print(len(self.list), "posibilities left...")
                self.wordlist = [x.lower() for x in self.list]
                self.tick += 1
                self.change_question()
                return

        elif self.tick == 1:

            self.current_answer = self.ids.answer.text
            self.ids.answer.text = ""
            print(self.current_answer)

            self.ids.question.text = "How many characters are in your word? (num)"

            self.wordlength = int(self.current_answer)

            self.newpos = []
            self.thelist = []
            self.count = 0
            self.found = 0

            for word in self.wordlist:
                if len(word) == self.wordlength:

                    self.found += 1
                    self.newpos.append(word)

                self.count += 1
                print("scanning... ", float("{0:.2f}".format(self.count/len(self.wordlist)*100)), " percent done:", "found", self.found, "words", end="\r")

            self.thelist = self.newpos
            print("\n", "There are currently ", len(self.thelist), "posibilities...")

            self.tick = 2

            self.click = 2
            self.get_char()
            print(self.char)
            self.change_question()

        elif self.tick == 10:
            self.current_answer = self.ids.answer.text
            self.ids.answer.text = ""
            print(self.current_answer)
            if self.current_answer.lower() == "yes":
                self.tick = 2
            elif self.current_answer.lower() == "no":
                hangman_game.screen_manager.current = "WonSolv"

        else:

            self.tick += 1

            self.current_answer = self.ids.answer.text
            self.ids.answer.text = ""
            print(self.current_answer)

            if self.tick == 5:

                newlist = []
                for word in self.thelist:
                    self.number = word.count(self.char)
                    if self.number == int(self.current_answer):
                        newlist.append(word)

                self.thelist = newlist

                self.already_guessed.append(self.char)
                self.get_char()
                self.change_question()
                self.tick = 2
                print("\n", "There are currently ", len(self.thelist), "posibilities...")
                self.right_guesses = self.right_guesses + int(self.current_answer)
                print(self.thelist)


            if self.current_answer.lower() == "yes":

                self.tick = 4
                self.ids.question.text = "How often?"

            elif self.current_answer.lower() == "no":
                self.newlist = []
                for word in self.thelist:
                    self.number = word.count(self.char)
                    if self.number == 0:
                        self.newlist.append(word)

                self.thelist = self.newlist
                self.false_guesses += 1

                self.tick = 2
                print("\n", "There are currently ", len(self.thelist), "posibilities...")
                print(self.thelist)
                self.already_guessed.append(self.char)
                self.get_char()
                self.change_question()

            if self.false_guesses > 0:
                if self.false_guesses == 1:
                    self.im.source='prog1.jpg'
                    self.im.allow_stretch=True
                elif self.false_guesses == 2:
                    self.im.source='prog2.jpg'
                elif self.false_guesses == 3:
                    self.im.source='prog3.jpg'
                elif self.false_guesses == 4:
                    self.im.source='prog4.jpg'
                elif self.false_guesses == 5:
                    self.im.source='prog5.jpg'
                elif self.false_guesses == 6:
                    self.im.source='prog6.jpg'
                elif self.false_guesses == 7:
                    self.im.source='prog7.jpg'
                elif self.false_guesses == 8:
                    self.im.source='prog8_solver.jpg'
                    self.change_question()

            if self.right_guesses == self.wordlength or len(self.thelist) == 1:
                if len(self.thelist) == 1:
                    self.ids.question.text = "Is this your word: " + str(self.thelist) + "? (YES/NO)"
                    self.tick = 10
                else:
                    self.ids.question.text = "Is your word one of these: " + str(self.thelist) + "? (YES/NO)"
                    self.tick = 10



    def change_question(self):
        if self.click == 1:
            self.ids.question.text = "How many characters are in your word? (num)"
        elif self.click > 1:
            self.ids.question.text = "Does your word have the letter " + str(self.char) + " in it? (YES/NO)"
        else:
            self.ids.question.text = "How often?"

        if self.false_guesses == 8:
            self.ids.question.text = "You win! Do you want to continue? (YES/NO)"

    def get_char(self):

        co = [0] * 256
        max = -1
        c = ""

        for word in self.thelist:
            for i in word:
                co[ord(i)]+=1;
                for i in self.already_guessed:
                    co[ord(i)] = 0

            for i in word:
                if max < co[ord(i)]:
                    max = co[ord(i)]
                    c = i

        self.char = str(c)

class WonPageSolver(BoxLayout):

    def __init__(self, **kwargs):

        super(WonPageSolver, self).__init__(**kwargs)

    def again(self):
        hangman_game.screen_manager.current = "Solver"

    def menu(self):
        hangman_game.screen_manager.current = "Login"

class WonPage(BoxLayout):

    def __init__(self, **kwargs):

        super(WonPage, self).__init__(**kwargs)

    def again(self):
        hangman_game.screen_manager.current = "Language"
    def menu(self):
        hangman_game.screen_manager.current = "Login"

class LostPageSolver(BoxLayout):

    def __init__(self, **kwargs):

        super(LostPageSolver, self).__init__(**kwargs)

    def menu(self):
        hangman_game.screen_manager.current = "Login"

class LostPage(BoxLayout):

    def __init__(self, **kwargs):

        super(LostPage, self).__init__(**kwargs)

    def menu(self):
        hangman_game.screen_manager.current = "Login"

class HangmanApp(App):
    def build(self):

        self.screen_manager = ScreenManager()

        self.login_page = LoginPage()
        screen = Screen(name="Login")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        self.solver_page = SolverGame()
        screen = Screen(name="Solver")
        screen.add_widget(self.solver_page)
        self.screen_manager.add_widget(screen)

        self.won_page_solver = WonPageSolver()
        screen = Screen(name="WonSolv")
        screen.add_widget(self.won_page_solver)
        self.screen_manager.add_widget(screen)

        self.language_selection = LanguageSelection()
        screen = Screen(name="Language")
        screen.add_widget(self.language_selection)
        self.screen_manager.add_widget(screen)

        self.hangman_game_en = HangmanGameEnglish()
        screen = Screen(name="HangmanEnglish")
        screen.add_widget(self.hangman_game_en)
        self.screen_manager.add_widget(screen)

        self.hangman_game_de = HangmanGameDeutsch()
        screen = Screen(name="HangmanDeutsch")
        screen.add_widget(self.hangman_game_de)
        self.screen_manager.add_widget(screen)

        self.won_page = WonPage()
        screen = Screen(name="Won")
        screen.add_widget(self.won_page)
        self.screen_manager.add_widget(screen)

        self.lost_page = LostPage()
        screen = Screen(name="Lost")
        screen.add_widget(self.lost_page)
        self.screen_manager.add_widget(screen)

        self.lost_page_solver = LostPageSolver()
        screen = Screen(name="LostSolv")
        screen.add_widget(self.lost_page_solver)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":

    hangman_game = HangmanApp()
    hangman_game.run()
