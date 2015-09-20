# coding=utf-8
# Mini-project #7 - Spaceship
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

__author__ = 'João Silva'

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
friction = 0.05


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, thrust_sound):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrust_sound = thrust_sound
        self.thrust_sound.set_volume(0.7)
        self.accelerate_reduce_factor = 0.4

    def draw(self, canvas):
        center = [self.image_center[0], self.image_center[1]]
        if self.thrust:
            center[0] += self.image_size[0]
        canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        if self.thrust:
            self._accelerate()
        self._friction()
        self._move()

    def _move(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

    def enable_thrust(self):
        self.thrust_sound.play()
        self.thrust = True

    def disable_thrust(self):
        self.thrust_sound.rewind()
        self.thrust = False

    def _accelerate(self):
        acceleration = angle_to_vector(self.angle)
        self.vel[0] += (acceleration[0] * self.accelerate_reduce_factor)
        self.vel[1] += (acceleration[1] * self.accelerate_reduce_factor)

    def _friction(self):
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)

    def rotate_anti_clockwise(self):
        self.angle_vel -= 0.1

    def rotate_clockwise(self):
        self.angle_vel += 0.1

    def stop_rotate(self):
        self.angle_vel = 0

    def shoot(self):
        global a_missile
        vector = angle_to_vector(my_ship.angle)
        a_missile = Sprite((my_ship.pos[0] + my_ship.radius * vector[0], my_ship.pos[1] + my_ship.radius * vector[1]),
                           (my_ship.vel[0] + vector[0] * 10, my_ship.vel[1] + vector[1] * 10),
                           0,
                           0,
                           missile_image,
                           missile_info,
                           missile_sound)


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def _move(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

    def update(self):
        self.angle += self.angle_vel
        self._move()


def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    # Text
    size = 30
    font = 'sans-serif'

    # Lives
    canvas.draw_text('Lives', (20, 20 + size * 3.0 / 4), size, 'White', font)
    canvas.draw_text(str(lives), (20, 20 + size * 7.0 / 4), size, 'White', font)

    # Score
    text = 'Score'
    width = frame.get_canvas_textwidth(text, size, font)
    canvas.draw_text(text, (WIDTH - 20 - width, 20 + size * 3.0 / 4), size, 'White', font)

    text = str(score)
    width = frame.get_canvas_textwidth(text, size, font)
    canvas.draw_text(text, (WIDTH - 20 - width, 20 + size * 7.0 / 4), size, 'White', font)


# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    a_rock = Sprite(
        (random.randrange(WIDTH), random.randrange(HEIGHT)),
        (random.randrange(-5, 5), random.randrange(-5, 5)),
        0,
        (random.random() - 0.5) / 10.0,
        asteroid_image,
        asteroid_info)


def key_down_handler(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.enable_thrust()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate_clockwise()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.rotate_anti_clockwise()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()


def key_up_handler(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.disable_thrust()
    elif (key == simplegui.KEY_MAP["right"]) or (key == simplegui.KEY_MAP["left"]):
        my_ship.stop_rotate()


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
