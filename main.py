from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import random
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout



class background(RelativeLayout):
    def __init__(self, **kwargs):
        super(background, self).__init__(**kwargs)
        Window.clearcolor=(0.1,0.1,0.1,1)

class SnakeGame(GridLayout):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.hscore=0
        self.score =0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.cols = 10
        self.snake = [(5, 7), (5, 8)]
        self.direction = (0, -1)  #
        self.food_position = self.generate_food()
        self.buffer = self.direction
        self.size_hint=(None, None)
        self.size = (800, 600)
        for row in range(self.cols):
            for col in range(self.cols):
                button = Button()
                button.background_color = (0, 0, 0, 1)
                self.add_widget(button)
        Clock.schedule_interval(self.update, 0.25)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.buffer == self.direction:
            if keycode[1] in ('w', 'up'):
                self.buffer = (1, 0)
            elif keycode[1] in ('s', 'down'):
                self.buffer = (-1, 0)
            elif keycode[1] in ('a', 'left'):
                self.buffer = (0, 1)
            elif keycode[1] in ('d', 'right'):
                self.buffer = (0, -1)

            if (self.buffer[0] + self.direction[0] == 0) or (self.buffer[1] + self.direction[1] == 0):
                    self.buffer = self.direction

            return True

    def generate_food(self):
        while True:
            position = (random.randint(0, self.cols - 1), random.randint(0, self.cols - 1))
            if position not in self.snake:
                return position

    def update(self, dt):
        self.direction = self.buffer
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if (
                new_head[0] < 0 or new_head[0] >= self.cols or
                new_head[1] < 0 or new_head[1] >= self.cols or
                new_head in self.snake
        ):
            if self.hscore <= self.score:
                self.hscore = self.score
            self.score=0
            self.buffer = (0, -1)
            self.snake = [(5, 7), (5, 8)]
            self.food_position = self.generate_food()

        else:
            self.snake.insert(0, new_head)


            if new_head == self.food_position:
                self.food_position = self.generate_food()
                self.score+=1

            else:
                self.snake.pop()


        for i,button in enumerate(self.children):
            if i==99:
                button.text="High Score:"
                button.font_size = "15sp"

            elif i==98:
                button.text=(f'{self.hscore}')
                button.font_size = "15sp"
            elif i==89:
                button.text = "Score:"
                button.font_size = "15sp"
            elif i ==88:
                button.text=(f'{self.score}')
                button.font_size = "15sp"

            button.background_color = (0, 0, 0, 1)

        for position in self.snake:
            index = position[0] * self.cols + position[1]
            self.children[index].background_color = (0, 1, 0, 1)

        index = self.food_position[0] * self.cols + self.food_position[1]
        self.children[index].background_color = (1, 0, 0, 1)


class SnakeApp(App):
    def build(self):
        layout = background()
        game = SnakeGame(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(game)
        return layout


if __name__ == '__main__':
    SnakeApp().run()
