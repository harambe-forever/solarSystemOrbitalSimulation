import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (100, 149, 237)
red = (188, 39, 50)
gray = (80, 78, 81)

font = pygame.font.SysFont("comicsans", 16)


def main():
    run = True
    clk = pygame.time.Clock()

    # sun is not a planet but whatever, kutleyi wiki'den caldim
    sun = Planet(0, 0, 30, yellow, 1.98892 * 10**30)
    sun.sun = True
    # bi y degeri baslangic velocity olarak verilmeli yoksa dumduz gunese dogru gidip ekrandan cikiolar ne alaka yani?
    earth = Planet(-1 * Planet.AU, 0, 16, blue, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000  # km cinsindendi metre yapiyoz, m/s seklinde
    mars = Planet(-1.524 * Planet.AU, 0, 12, red, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, gray, 0.330 * 10**24)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 1, 14, white, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    planets = [sun, earth, mars, mercury, venus]

    while run:
        clk.tick(60)
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        pygame.display.update()
    pygame.quit()


class Planet:
    # astronomical units, 149 milyon km ama metre cinsinden
    AU = (149.6e6 * 1000)
    # gravitational constant, yerçekimi sabiti
    G = 6.67428e-11
    # olcek, 150 milyon kilometreyi 800x800 ekranina nasil sigdirayim ??
    SCALE = 250/AU  # 1AU = 100 px
    # izlemek istedigin zamani hizlandiran sabit
    # 1 gune denk geliyor, YORUNGEYI DAHA IYI ANLAMAK ICIN ZAMAN SABITINI 1800*24 yapabilirsin
    TIMESTEP = 3600*24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + (WIDTH / 2)
        y = self.y * self.SCALE + (HEIGHT / 2)

        if len(self.orbit) > 2:
            # yorunuge cizimi icin eski posizyonnu tutuyoz ve ekranda cizgi halinde yeni pozisyon ile birlestiriyoz boylece yorunge goruntusu olusuyor
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(WIN, self.color, False, updated_points)

        pygame.draw.circle(WIN, self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = font.render(
                f"{round(self.distance_to_sun/1000, 1)}km", 1, white)
            WIN.blit(distance_text, (x - distance_text.get_width() /
                                     2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * ((self.mass * other.mass) /
                          distance**2)  # f bulma islemi. sslere bak orda acikliom

        # arc tan islemi. sslere bak acikliom orda
        angle = math.atan2(distance_y, distance_x)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0  # diger gezegenlerin de etkisini hesapliyoz
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # f = ma amk bunu bilmiyosan liseye geri don
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


main()
