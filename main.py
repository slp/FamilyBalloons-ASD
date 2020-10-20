from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, StringProperty
from kivy.graphics import Rectangle
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.input.shape import ShapeRect
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import *
import random
from functools import partial

class Balloon(Widget):
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def check_collision(self, x, y):
        if (x > self.pos[0]) and x < (self.pos[0] + self.width):
            if y > (self.pos[1] + (self.height / 3)) and y < (self.pos[1] + self.height):
                return True
        return False

class BalloonRed(Balloon):
    pass

class BalloonBlack(Balloon):
    pass

class BalloonBlue(Balloon):
    pass

class BalloonGreen(Balloon):
    pass

class BalloonOrange(Balloon):
    pass

class BalloonPink(Balloon):
    pass

class BalloonWhite(Balloon):
    pass

class BalloonYellow(Balloon):
    pass


balloon_types = [BalloonRed, BalloonBlack, BalloonBlue, BalloonGreen, BalloonOrange, BalloonPink, BalloonWhite, BalloonYellow]

class Cat(Widget):
    name = 'cat'

class Cow(Widget):
    name = 'cow'

class Crocodile(Widget):
    name = 'crocodile'

class Dog(Widget):
    name = 'dog'

class Elephant(Widget):
    name = 'elephant'
    
class Hen(Widget):
    name = 'hen'
    
class Lion(Widget):
    name = 'lion'
    
class Tiger(Widget):
    name = 'tiger'

animal_types = [Cat, Cow, Crocodile, Dog, Elephant, Hen, Lion, Tiger]

class FamilyTata(Widget):
    ratio = 1.5
    name = 'tata'

class FamilyPapa(Widget):
    ratio = 1.33
    name = 'papa'

class FamilyMama(Widget):
    ratio = 1.33
    name = 'mama'

class FamilyYaya(Widget):
    ratio = 1.33
    name = 'yaya'

class FamilyYayo(Widget):
    ratio = 1.33
    name = 'yayo'

class Score(Widget):
    score = NumericProperty(0)
    
    def update_score(self, score):
        self.score += 1

class FamilyBalloonGame(Widget):
    score = ObjectProperty(None)
    game_mode = 0
    local_score = 0
    velocity = dp(2)
    velocity_delta = dp(1)
    velocity_max = velocity * 4
    parallel = 2
    diff_delta = 0
    diff_target = 2
    taps = 2
    balloon_missed = False

    family_turn = 0
    balloon_list = [ ]

    change_to_family_mode = False
    change_to_balloon_mode = False
    
    music = SoundLoader.load('music/intro.ogg')
    sound_search_for = SoundLoader.load('sounds/search_for.wav')
    sound_tata = SoundLoader.load('sounds/tata.wav')
    sound_papa = SoundLoader.load('sounds/papa.wav')
    sound_mama = SoundLoader.load('sounds/mama.wav')
    sound_yaya = SoundLoader.load('sounds/yaya.wav')
    sound_yayo = SoundLoader.load('sounds/yayo.wav')
    
    sound_pop = SoundLoader.load('sounds/pop.wav')
    sound_cat = SoundLoader.load('sounds/cat.wav')
    sound_cow = SoundLoader.load('sounds/cow.wav')
    sound_crocodile = SoundLoader.load('sounds/crocodile.wav')
    sound_dog = SoundLoader.load('sounds/dog.wav')
    sound_elephant = SoundLoader.load('sounds/elephant.wav')
    sound_hen = SoundLoader.load('sounds/hen.wav')
    sound_lion = SoundLoader.load('sounds/lion.wav')
    sound_tiger = SoundLoader.load('sounds/tiger.wav')

    sound_dict = { 'cat': sound_cat,
                   'cow': sound_cow,
                   'crocodile': sound_crocodile,
                   'dog': sound_dog,
                   'elephant': sound_elephant,
                   'hen': sound_hen,
                   'lion': sound_lion,
                   'tiger': sound_tiger }

    family_sound_dict = { 'tata': sound_tata,
                          'papa': sound_papa,
                          'mama': sound_mama,
                          'yaya': sound_yaya,
                          'yayo': sound_yayo }

    family_list = [ ]

    def play_sound(self, sound, dt):
        sound.play()

    def spawn_balloon(self, dt):
        if self.game_mode == 0:
            num = random.randint(1, self.parallel)
            for i in range(num):
                width = self.size[0]
                height = self.size[1]
                balloon = balloon_types[random.randint(0, len(balloon_types)-1)]()
                balloon.velocity = (0, self.velocity)
                max_pos = int(width - balloon.width)
                if max_pos < 0:
                    max_pos = width / 5
                balloon.pos = (random.randint(0, max_pos), -balloon.height + (i * dp(-20)))
                self.balloon_list.append(balloon)
                self.add_widget(balloon)

    def spawn_price(self, pos):
        self.sound_pop.play()
        price = animal_types[random.randint(0, len(animal_types)-1)]()
        price.pos = pos
        price.pos[1] += dp(50)
        self.add_widget(price)
        Clock.schedule_once(partial(self.play_sound, self.sound_dict[price.name]), self.sound_pop.length)
        Clock.schedule_once(partial(self.remove_price, price), 1)

    def remove_price(self, price, dt):
        self.remove_widget(price)

    def start(self, target, velocity, velocity_delta, parallel, taps, enable_music, family_list):
        self.diff_target = target
        self.velocity = dp(velocity)
        self.velocity_delta = dp(velocity_delta)
        self.velocity_max = self.velocity * 4
        self.parallel = parallel
        self.taps = taps
        self.family_list = family_list

        if enable_music:
            self.music.volume = 0.1
            self.music.loop = True
            self.music.play()

    def update(self, dt):
        if self.game_mode != 1:
            for i, balloon in enumerate(self.balloon_list):
                balloon.move()
                if balloon.pos[1] >= self.height:
                    self.remove_widget(balloon)
                    del self.balloon_list[i]
                    self.balloon_missed = True

    def change_to_family_mode(self):
        for i, balloon in enumerate(self.balloon_list):
            self.remove_widget(balloon)
        balloon_list = [ ]

        self.member = self.family_list[self.family_turn]()
        self.family_turn += 1
        if self.family_turn == len(self.family_list):
            self.family_turn = 0
        h = self.height * 80 / 100
        w = h * self.member.ratio
        self.member.size = (w, h)
        self.member.pos = ((self.width - w) / 2, (self.height - h) / 2)
        self.add_widget(self.member)
        self.game_mode = 1
        self.sound_search_for.play()
        Clock.schedule_once(partial(self.play_sound, self.family_sound_dict[self.member.name]), self.sound_search_for.length + 0.3)

    def on_touch_down(self, touch):
        if self.game_mode == 1:
            if self.member.collide_point(touch.pos[0], touch.pos[1]):
                sound = self.family_sound_dict[self.member.name]
                sound.play()
            elif self.taps == 2 and touch.is_double_tap:
                self.remove_widget(self.member)
                self.game_mode = 0
            elif self.taps == 3 and touch.is_triple_tap:
                self.remove_widget(self.member)
                self.game_mode = 0
        else:
            for balloon in reversed(self.balloon_list):
                if balloon.check_collision(touch.pos[0], touch.pos[1]):
                    self.remove_widget(balloon)
                    self.balloon_list.remove(balloon)
                    
                    self.local_score += 1
                    self.score.update_score(self.local_score)

                    self.diff_delta += 1
                    if self.diff_delta == self.diff_target:
                        if not self.balloon_missed and self.velocity < self.velocity_max:
                            self.velocity += self.velocity_delta
                        self.balloon_missed = False
                        self.diff_delta = 0
                        if len(self.family_list) != 0:
                            self.change_to_family_mode()
                        else:
                            self.spawn_price(balloon.pos)
                    else:
                        self.spawn_price(balloon.pos)
                    break

class FamilyBalloonIntro(Image):
    target = 20
    velocity = 2
    velocitydelta = 0
    parallel = 2
    taps = 2

    def __init__(self, **kwargs):
        super(FamilyBalloonIntro, self).__init__(source="images/background.png", **kwargs)
        self.target10_btn.bind(on_press=self.toggle_target10)
        self.target20_btn.bind(on_press=self.toggle_target20)
        self.target30_btn.bind(on_press=self.toggle_target30)
        self.target20_btn.state = 'down'

        self.velocity1_btn.bind(on_press=self.toggle_velocity1)
        self.velocity2_btn.bind(on_press=self.toggle_velocity2)
        self.velocity3_btn.bind(on_press=self.toggle_velocity3)
        self.velocity2_btn.state = 'down'

        self.velocitydelta0_btn.bind(on_press=self.toggle_velocitydelta0)
        self.velocitydelta1_btn.bind(on_press=self.toggle_velocitydelta1)
        self.velocitydelta2_btn.bind(on_press=self.toggle_velocitydelta2)
        self.velocitydelta3_btn.bind(on_press=self.toggle_velocitydelta3)
        self.velocitydelta0_btn.state = 'down'

        self.parallel1_btn.bind(on_press=self.toggle_parallel1)
        self.parallel2_btn.bind(on_press=self.toggle_parallel2)
        self.parallel3_btn.bind(on_press=self.toggle_parallel3)
        self.parallel2_btn.state = 'down'

        self.taps2_btn.bind(on_press=self.toggle_taps2)
        self.taps3_btn.bind(on_press=self.toggle_taps3)
        self.taps2_btn.state = 'down'

    def toggle_target10(self, *largs):
        if self.target10_btn.state == 'normal':
            self.target10_btn.state = 'down'
        self.target20_btn.state = 'normal'
        self.target30_btn.state = 'normal'
        self.target = 10

    def toggle_target20(self, *largs):
        if self.target20_btn.state == 'normal':
            self.target20_btn.state = 'down'
        self.target10_btn.state = 'normal'
        self.target30_btn.state = 'normal'
        self.target = 20

    def toggle_target30(self, *largs):
        if self.target30_btn.state == 'normal':
            self.target30_btn.state = 'down'
        self.target10_btn.state = 'normal'
        self.target20_btn.state = 'normal'
        self.target = 30

    def toggle_velocity1(self, *largs):
        if self.velocity1_btn.state == 'normal':
            self.velocity1_btn.state = 'down'
        self.velocity2_btn.state = 'normal'
        self.velocity3_btn.state = 'normal'
        self.velocity = 1

    def toggle_velocity2(self, *largs):
        if self.velocity2_btn.state == 'normal':
            self.velocity2_btn.state = 'down'
        self.velocity1_btn.state = 'normal'
        self.velocity3_btn.state = 'normal'
        self.velocity = 2

    def toggle_velocity3(self, *largs):
        if self.velocity3_btn.state == 'normal':
            self.velocity3_btn.state = 'down'
        self.velocity1_btn.state = 'normal'
        self.velocity2_btn.state = 'normal'
        self.velocity = 3

    def toggle_velocitydelta0(self, *largs):
        if self.velocitydelta0_btn.state == 'normal':
            self.velocitydelta0_btn.state = 'down'
        self.velocitydelta1_btn.state = 'normal'
        self.velocitydelta2_btn.state = 'normal'
        self.velocitydelta3_btn.state = 'normal'
        self.velocitydelta = 0

    def toggle_velocitydelta1(self, *largs):
        if self.velocitydelta1_btn.state == 'normal':
            self.velocitydelta1_btn.state = 'down'
        self.velocitydelta0_btn.state = 'normal'
        self.velocitydelta2_btn.state = 'normal'
        self.velocitydelta3_btn.state = 'normal'
        self.velocitydelta = 1

    def toggle_velocitydelta2(self, *largs):
        if self.velocitydelta2_btn.state == 'normal':
            self.velocitydelta2_btn.state = 'down'
        self.velocitydelta0_btn.state = 'normal'
        self.velocitydelta1_btn.state = 'normal'
        self.velocitydelta3_btn.state = 'normal'
        self.velocitydelta = 2

    def toggle_velocitydelta3(self, *largs):
        if self.velocitydelta3_btn.state == 'normal':
            self.velocitydelta3_btn.state = 'down'
        self.velocitydelta0_btn.state = 'normal'
        self.velocitydelta1_btn.state = 'normal'
        self.velocitydelta2_btn.state = 'normal'
        self.velocitydelta = 3

    def toggle_parallel1(self, *largs):
        if self.parallel1_btn.state == 'normal':
            self.parallel1_btn.state = 'down'
        self.parallel2_btn.state = 'normal'
        self.parallel3_btn.state = 'normal'
        self.parallel = 1

    def toggle_parallel2(self, *largs):
        if self.parallel2_btn.state == 'normal':
            self.parallel2_btn.state = 'down'
        self.parallel1_btn.state = 'normal'
        self.parallel3_btn.state = 'normal'
        self.parallel = 2

    def toggle_parallel3(self, *largs):
        if self.parallel3_btn.state == 'normal':
            self.parallel3_btn.state = 'down'
        self.parallel1_btn.state = 'normal'
        self.parallel2_btn.state = 'normal'
        self.parallel = 3

    def toggle_taps2(self, *largs):
        if self.taps2_btn.state == 'normal':
            self.taps2_btn.state = 'down'
        self.taps3_btn.state = 'normal'
        self.taps = 2

    def toggle_taps3(self, *largs):
        if self.taps3_btn.state == 'normal':
            self.taps3_btn.state = 'down'
        self.taps2_btn.state = 'normal'
        self.taps = 3

    def is_music_enabled(self, *largs):
        if self.music_btn.state == 'down':
            return True
        return False

    def get_family_list(self):
        family_list = [ ]
        if self.mama_btn.state == 'down':
            family_list.append(FamilyMama)
        if self.papa_btn.state == 'down':
            family_list.append(FamilyPapa)
        if self.tata_btn.state == 'down':
            family_list.append(FamilyTata)
        if self.yaya_btn.state == 'down':
            family_list.append(FamilyYaya)
        if self.yayo_btn.state == 'down':
            family_list.append(FamilyYayo)
        return family_list

class ScreenFader(Widget):
    alpha = NumericProperty(0.0)
    
    def __init__(self, alpha=0, **kwargs):
        super(ScreenFader, self).__init__(**kwargs)
        self.bind(alpha=self.on_alpha)
        self.alpha = alpha
            
    def on_alpha(self, instance, value):
        # Probably there is more efficient approach. Tried other ways, 
        # didnt work. Stuck with this.
        self.canvas.clear()
        with self.canvas:
            Color(0,0,0, value)
            Rectangle(pos=self.pos, size=self.size)                           

class FamilyBalloonApp(App):
    intro = None
    game = None
    fader = None
    
    def build(self):
        Builder.load_file("intro.kv")
        self.intro = FamilyBalloonIntro()
        self.intro.go_btn.bind(on_release=self._transition_outof_intro)
        return self.intro

    def _transition_outof_intro(self, *args):
        self.fader = ScreenFader(size=Window.size)
        Window.add_widget(self.fader)
        anim = Animation(alpha = 1.0, d=0.6)
        anim.bind(on_complete=self.start_game)
        anim.start(self.fader)

    def start_game(self, *largs, **kwargs):
        self.root = self.game = FamilyBalloonGame()

        try:
            Window.remove_widget(self.intro)
        except:
            pass
            
        Window.add_widget(self.root)
        
        # Fade in
        Window.remove_widget(self.fader)
        Window.add_widget(self.fader)
        anim = Animation(alpha = 0.0, d=0.8)
        anim.bind(on_complete=lambda instance, value: Window.remove_widget(self.fader))
        anim.start(self.fader)

        self.game.start(self.intro.target, self.intro.velocity, self.intro.velocitydelta, self.intro.parallel, self.intro.taps, self.intro.is_music_enabled(), self.intro.get_family_list())
        self.game.spawn_balloon(0)

        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        Clock.schedule_interval(self.game.spawn_balloon, 1.5)


if __name__ == '__main__':
    FamilyBalloonApp().run()

