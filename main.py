import random

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


class MatrixGame(App):

    def build(self):
        Window.clearcolor = (0.04, 0.07, 0.09, 1)

        self.score = 0
        self.q_no = 0
        self.time_left = 60
        self.correct = None
        self.answer_locked = False
        self.timer_event = None

        self.home_screen()

        return self.root

    # ================= HOME =================

    def home_screen(self):

        self.root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="MATRIX",
            font_size="38sp",
            bold=True,
            color=(0, 0.85, 1, 1)
        )

        subtitle = Label(
            text="Micro Project for\nChaitanya Shinde",
            font_size="20sp",
            bold=True
        )

        info = Label(
            text="MATRIX PUZZLE\n\n"
                 "Correct Answer  +10\n"
                 "Wrong Answer      0\n"
                 "Time               60 sec\n"
                 "Unlimited Questions",
            font_size="17sp"
        )

        start = Button(
            text="START GAME",
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=65
        )

        start.bind(on_press=self.start_game)

        self.root.add_widget(title)
        self.root.add_widget(subtitle)
        self.root.add_widget(info)
        self.root.add_widget(start)

    # ================= START =================

    def start_game(self, instance):

        self.score = 0
        self.q_no = 0

        self.game_screen()
        self.next_question()

    # ================= GAME SCREEN =================

    def game_screen(self):

        self.root.clear_widgets()

        main = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        top = BoxLayout(
            size_hint_y=None,
            height=50
        )

        self.title_label = Label(
            text="MATRIX",
            font_size="25sp",
            bold=True,
            color=(0, 0.85, 1, 1)
        )

        self.score_label = Label(
            text="Score: 0",
            font_size="18sp",
            bold=True,
            color=(0.2, 1, 0.4, 1)
        )

        top.add_widget(self.title_label)
        top.add_widget(self.score_label)

        self.q_label = Label(
            text="Question 1",
            font_size="19sp",
            bold=True,
            size_hint_y=None,
            height=40
        )

        self.timer_label = Label(
            text="TIME: 60",
            font_size="22sp",
            bold=True,
            color=(1, 0.8, 0.2, 1),
            size_hint_y=None,
            height=45
        )

        self.matrix_label = Label(
            text="",
            font_size="22sp",
            bold=True,
            halign="center"
        )

        self.answer_title = Label(
            text="SELECT CORRECT MATRIX",
            font_size="15sp",
            bold=True,
            color=(0, 0.85, 1, 1),
            size_hint_y=None,
            height=35
        )

        self.answer_grid = GridLayout(
            cols=2,
            spacing=7,
            size_hint_y=0.9
        )

        main.add_widget(top)
        main.add_widget(self.q_label)
        main.add_widget(self.timer_label)
        main.add_widget(self.matrix_label)
        main.add_widget(self.answer_title)
        main.add_widget(self.answer_grid)

        self.root.add_widget(main)

    # ================= QUESTION =================

    def make_question(self):

        A = [random.randint(1, 9) for _ in range(4)]
        B = [random.randint(1, 9) for _ in range(4)]

        operation = random.choice(["+", "-"])

        if operation == "+":

            answer = tuple(
                A[i] + B[i] for i in range(4)
            )

        else:

            for i in range(4):

                if A[i] < B[i]:
                    A[i], B[i] = B[i], A[i]

            answer = tuple(
                A[i] - B[i] for i in range(4)
            )

        return tuple(A), tuple(B), operation, answer

    # ================= NEXT QUESTION =================

    def next_question(self):

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        self.q_no += 1
        self.time_left = 60
        self.answer_locked = False

        A, B, op, answer = self.make_question()

        self.correct = answer

        self.q_label.text = f"Question {self.q_no}"
        self.score_label.text = f"Score: {self.score}"

        self.matrix_label.text = (
            f"[ {A[0]}   {A[1]} ]\n"
            f"[ {A[2]}   {A[3]} ]\n\n"
            f"          {op}\n\n"
            f"[ {B[0]}   {B[1]} ]\n"
            f"[ {B[2]}   {B[3]} ]"
        )

        self.answer_grid.clear_widgets()

        choices = [answer]

        while len(choices) < 6:

            wrong = list(answer)

            position = random.randint(0, 3)

            change = random.choice(
                [-3, -2, -1, 1, 2, 3]
            )

            wrong[position] = max(
                0,
                wrong[position] + change
            )

            wrong = tuple(wrong)

            if wrong not in choices:
                choices.append(wrong)

        random.shuffle(choices)

        for choice in choices:

            text = (
                f"[ {choice[0]}   {choice[1]} ]\n"
                f"[ {choice[2]}   {choice[3]} ]"
            )

            btn = Button(
                text=text,
                font_size="15sp",
                bold=True
            )

            btn.bind(
                on_press=lambda instance,
                x=choice: self.check_answer(x)
            )

            self.answer_grid.add_widget(btn)

        self.timer_event = Clock.schedule_interval(
            self.update_timer,
            1
        )

    # ================= TIMER =================

    def update_timer(self, dt):

        if self.answer_locked:
            return

        self.timer_label.text = f"TIME: {self.time_left}"

        if self.time_left <= 10:
            self.timer_label.color = (1, 0.2, 0.3, 1)
        else:
            self.timer_label.color = (1, 0.8, 0.2, 1)

        if self.time_left <= 0:

            self.answer_locked = True

            if self.timer_event:
                self.timer_event.cancel()
                self.timer_event = None

            self.show_wrong(
                None,
                "TIME UP"
            )

            return

        self.time_left -= 1

    # ================= CHECK ANSWER =================

    def check_answer(self, selected):

        if self.answer_locked:
            return

        self.answer_locked = True

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        if selected == self.correct:

            self.score += 10
            self.score_label.text = f"Score: {self.score}"

            Clock.schedule_once(
                lambda dt: self.next_question(),
                0.4
            )

        else:

            self.show_wrong(
                selected,
                "WRONG"
            )

    # ================= WRONG SCREEN =================

    def show_wrong(self, selected, reason):

        self.root.clear_widgets()

        screen = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=12
        )

        joker = Label(
            text="JOKER",
            font_size="42sp",
            bold=True,
            color=(1, 0.8, 0.2, 1)
        )

        if reason == "TIME UP":

            result = Label(
                text="TIME UP!",
                font_size="28sp",
                bold=True,
                color=(1, 0.2, 0.3, 1)
            )

            your_answer = "No Answer"

        else:

            result = Label(
                text="WRONG ANSWER!",
                font_size="27sp",
                bold=True,
                color=(1, 0.2, 0.3, 1)
            )

            your_answer = (
                f"[ {selected[0]}   {selected[1]} ]\n"
                f"[ {selected[2]}   {selected[3]} ]"
            )

        your = Label(
            text=f"YOUR ANSWER\n\n{your_answer}",
            font_size="18sp",
            bold=True
        )

        correct = Label(
            text=(
                "CORRECT ANSWER\n\n"
                f"[ {self.correct[0]}   {self.correct[1]} ]\n"
                f"[ {self.correct[2]}   {self.correct[3]} ]"
            ),
            font_size="19sp",
            bold=True,
            color=(0.2, 1, 0.4, 1)
        )

        score = Label(
            text=f"Score: {self.score}",
            font_size="21sp",
            bold=True
        )

        next_btn = Button(
            text="NEXT QUESTION",
            font_size="21sp",
            bold=True,
            size_hint_y=None,
            height=65
        )

        next_btn.bind(
            on_press=lambda instance:
            self.next_after_wrong()
        )

        screen.add_widget(joker)
        screen.add_widget(result)
        screen.add_widget(your)
        screen.add_widget(correct)
        screen.add_widget(score)
        screen.add_widget(next_btn)

        self.root.add_widget(screen)

    # ================= NEXT AFTER WRONG =================

    def next_after_wrong(self):

        self.game_screen()
        self.next_question()


MatrixGame().run()