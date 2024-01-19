import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NormalBird"

BIRD_SPEED = 6
BIRD_SPEED_ANGLE = 6
GRAVITATION = 0.4

PIPE_SPEED = 4


class Animate(arcade.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time):
        self.time += delta_time

        if self.time >= 0.1:
            self.time = 0

            if self.i == len(self.textures) - 1:

                self.i = 0

            else:

                self.i += 1

                self.set_texture(self.i)


class Bird(Animate):
    def __init__(self):
        super().__init__("bird/CUstombird-downflap.png", 2.5)
        self.append_texture(arcade.load_texture("bird/Custombird-midflap.png"))
        self.append_texture(arcade.load_texture("bird/Custombird-upflap.png"))

        self.center_x = 70
        self.center_y = SCREEN_HEIGHT / 2

        self.angle = 0

    def update(self):
        self.center_y += self.change_y
        self.change_y -= GRAVITATION

        """collisions for screen"""
        if self.center_y > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        if self.center_y < 0:
            self.center_y = 0

        """angle"""
        self.angle += self.change_angle
        self.change_angle -= 0.4

        if self.angle <= -45:
            self.angle = -45

        if self.angle >= 45:
            self.angle = 30


class Pipes(arcade.Sprite):
    def __init__(self):
        super().__init__("dubble-pipe.png", 3)

    def update(self):
        self.center_x -= self.change_x
        self.change_x = 2

        if self.center_x <= -60:
            self.remove_from_sprite_lists()


class Coin(Animate):
    def __init__(self):
        super().__init__("coin/coin-1.png", 2.5)
        """Frames"""
        self.append_texture(arcade.load_texture("coin/coin-2.png"))
        self.append_texture(arcade.load_texture("coin/coin-3.png"))
        self.append_texture(arcade.load_texture("coin/coin-4.png"))
        self.append_texture(arcade.load_texture("coin/coin-5.png"))
        self.append_texture(arcade.load_texture("coin/coin-6.png"))
        self.append_texture(arcade.load_texture("coin/coin-5.png"))
        self.append_texture(arcade.load_texture("coin/coin-4.png"))
        self.append_texture(arcade.load_texture("coin/coin-3.png"))
        self.append_texture(arcade.load_texture("coin/coin-2.png"))

        self.center_x = SCREEN_WIDTH

        self.change_x = 2

    def update(self):
        self.center_x -= self.change_x

        if self.center_x <= -60:
            self.remove_from_sprite_lists()



class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        """Bg"""
        self.bg = arcade.load_texture("custom-bg.png")

        """Sprites"""
        self.bird = Bird()
        self.coin = Coin()
        self.coin_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        """clock"""
        self.fps_counter = 0

    def setup(self):
        for i in range(6):
            pipe = Pipes()
            pipe.center_y = random.randint(200, 400)
            pipe.center_x = (160 * i) + SCREEN_WIDTH

            self.pipe_list.append(pipe)

        for i in range(6):
            second_pipe = self.pipe_list[i]
            coin = Coin()
            coin.center_x = second_pipe.center_x
            coin.center_y = second_pipe.center_y

            self.coin_list.append(coin)

    def on_draw(self):
        self.clear()
        """Bg"""
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT, self.bg)

        """Sprites"""
        self.coin_list.draw()
        self.bird.draw()
        self.pipe_list.draw()  # list instead of a one pipe

    def update(self, delta_time):
        """Bird"""
        self.bird.update_animation(delta_time)
        self.bird.update()

        """Pipes"""
        self.pipe_list.update()  # update all the sprites in the pipe list

        # spawn mechanic
        self.fps_counter += 1
        if self.fps_counter >= 480:  # here you can adjust the time between list spawn, 60 fps = 1 second
            self.fps_counter = 0

            self.setup()

        """coin"""
        self.coin_list.update()
        self.coin.update_animation(delta_time)
        self.coin_list.update_animation()
        if self.fps_counter >= 480:  #  here you can adjust the time between list spawn, 60 fps = 1 second
            self.fps_counter = 0

            self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.bird.change_y = BIRD_SPEED

            self.bird.change_angle = BIRD_SPEED_ANGLE


my_game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

my_game.setup()
arcade.run()