# Игра doodle jump

import pygame
import random
import pickle

WIDTH = 500
HEIGHT = 750
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Глобальные константы
SCORE = 0

# Создаем игру и окно
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 750)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle jump")
clock = pygame.time.Clock()
pygame.mixer.music.load('mystery.wav')
icon = pygame.image.load("icon.png")
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)


# Спрайт игрок
class Player(pygame.sprite.Sprite):
    move = 18
    Is_up = True
    Is_on_platform = True
    move_down = 0

    def __init__(self, x: int, y: int, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player.png').convert_alpha()
        self.right_image = pygame.transform.scale(self.image, (50, 50))
        self.left_image = pygame.transform.flip(self.right_image, 1, 0)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.group = group
        self.current_platform = group.sprites()[0]
        self.fall_sound = pygame.mixer.Sound('fall.wav')
        self.pause = 0

    def update(self, *side: bool):
        global SCORE

        if self.Is_on_platform:
            if self.Is_up and self.move:
                self.rect.y -= self.move
                self.move -= 1
            elif self.rect.y < (self.current_platform.rect.y - 50):
                self.Is_up = False
                self.move += 1
                self.rect.y += self.move
            else:
                self.Is_up = True
            self.move_down = 0
        else:
            if self.pause:
                self.pause -= 1
            else:
                self.pause = FPS // 1.75
                self.fall_sound.play()

            self.Is_up = True
            self.move = 15
            self.move_down += 1
            self.rect.y += self.move_down

        # Меняем изображение
        if side[0]:
            self.rect.x -= 5
            self.image = self.left_image
        elif side[1]:
            self.rect.x += 5
            self.image = self.right_image

        # Если текущая платформа - двигающаяся
        if isinstance(self.current_platform, MovingPlatform):
            if self.current_platform.is_go_right:
                self.rect.x += 5
            else:
                self.rect.x -= 5

        # Перерисовываем персонжа, если он прыгнет влево или вправо
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

        for plat in self.group:
            y = plat.rect.y
            if plat.rect.left - 10 <= self.rect.x <= plat.rect.right + 10 and (
                    (self.rect.y <= y <= self.current_platform.rect.y) or (
                    self.rect.y >= y >= self.current_platform.rect.y)):
                self.Is_on_platform = True
                if self.rect.y < y < self.current_platform.rect.y:
                    SCORE += 1
                    for pl in self.group:
                        pl.rect.y += pl.move
                self.current_platform = plat
                break
            else:
                self.Is_on_platform = False


# Спрайт платформа
class Platform(pygame.sprite.Sprite):
    length = 80
    move = 90

    def __init__(self, group, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('platform.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.length, 23))
        self.rect = self.image.get_rect()
        self.add(group)
        self.group = group

        if num == 0:
            self.rect.center = (WIDTH // 2, HEIGHT // 2)
        elif (self.group.sprites()[num - 1].rect.y - self.move) > 0:
            while abs((x := random.randrange(WIDTH - 3 * self.length)) - self.group.sprites()[num - 1].rect.x) <= 0:
                pass
            self.rect.center = (x, self.group.sprites()[num - 1].rect.y - self.move)
        else:
            while abs((x := random.randrange(WIDTH - 3 * self.length)) - self.group.sprites()[num - 1].rect.x) <= 0:
                pass
            self.rect.center = (x, 0)

    def update(self):
        if self.rect.y >= HEIGHT:
            # Удаляем объект
            self.kill()


# Спрайт двигающаяся платформа
class MovingPlatform(Platform):
    def __init__(self, group, num):
        Platform.__init__(self, group, num)
        self.image = pygame.image.load('moving_platform.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.length, 23))
        self.rect = self.image.get_rect()
        self.is_go_right = True

    def update(self):
        if self.is_go_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

        if self.rect.left > WIDTH:
            self.is_go_right = False
        if self.rect.right < 0:
            self.is_go_right = True

        Platform.update(self)


# Спрайт падающая платформа
class FallingPlatform(Platform):
    def __init__(self, group, num):
        Platform.__init__(self, group, num)

    def update(self):
        Platform.update(self)


# Проверка есть ли платформа сверху
def is_platform_on_up(platforms):
    platform_on_up = False
    for platform in platforms:
        if platform.rect.y == -11:
            platform_on_up = True
            break

    return platform_on_up


# Очистка рекорда
def clear_file():
    file = open("file.dat", "wb")
    file.close()


# Вывести текст
def print_text(message, x, y, font_color=BLACK, font_type=None, font_size=30):
    font = pygame.font.SysFont(font_type, font_size)
    text = font.render(message, True, font_color)
    screen.blit(text, (x, y))


# Пауза
def pause():
    continue_button = Button(230, 70)
    exit_button = Button(135, 70)

    paused = True
    while paused:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        print_text("Пауза в игре", WIDTH // 4, HEIGHT // 4 + HEIGHT // 8, font_size=60)
        continue_button.draw(WIDTH // 4 + WIDTH // 18, HEIGHT // 2, "Продолжить", None, 40)
        exit_button.draw(WIDTH // 3 + WIDTH // 25, HEIGHT // 2 + HEIGHT // 8, "Выйти", game_menu, 40)
        pygame.display.update()
        clock.tick(FPS)


# Кнопка
class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.active_color = GREEN
        # self.inactive_color = YELLOW
        self.draw_effects = False
        self.clear_effects = False
        self.rect_h = 10
        self.rect_w = width

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_sound = pygame.mixer.Sound("button.wav")

        # Координаты в области
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            # pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            # Нажата левая кнопка мыши
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()

        # else:
        #     pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        self.draw_beautiful_rect(mouse[0], mouse[1], x, y)

        print_text(message=message, x=x + 10, y=y + 10, font_type='Times New Roman', font_size=font_size)

    def draw_beautiful_rect(self, mouse_x, mouse_y, x, y):
        if x <= mouse_x <= x + self.width and y <= mouse_y <= y + self.height:
            self.draw_effects = True

        if self.draw_effects:
            if mouse_x < x or mouse_x > x + self.width or mouse_y < y or mouse_y > y + self.height:
                self.clear_effects = True
                self.draw_effects = False

            if self.rect_h < self.height:
                self.rect_h += (self.height - 10) / 40

        if self.clear_effects and not self.draw_effects:
            if self.rect_h > 10:
                self.rect_h -= (self.height - 10) / 40
            else:
                self.clear_effects = False

        draw_y = y + self.height - self.rect_h
        pygame.draw.rect(screen, self.active_color, (x, draw_y, self.rect_w, self.rect_h))


# Главное меню
def game_menu():
    pygame.mixer.music.play(-1)
    background_image = pygame.image.load('menu.jpg').convert_alpha()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    start_button = Button(220, 70)
    reset_score = Button(265, 70)
    exit_button = Button(130, 70)

    menu = True
    while menu:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background_image, (0, 0))
        start_button.draw(WIDTH // 4 + WIDTH // 25, HEIGHT // 4 + HEIGHT // 8, "Начать игру", game_cycle, 40)
        reset_score.draw(WIDTH // 4, HEIGHT // 2, "Сбросить счет", clear_file, 40)
        exit_button.draw(WIDTH // 3 + WIDTH // 25, HEIGHT // 2 + HEIGHT // 8, "Выйти", quit, 40)
        pygame.display.update()
        clock.tick(FPS)

    pygame.mixer.music.stop()
    game_cycle()


# Основной цикл
def game_cycle():
    pygame.mixer.music.stop()
    platforms = pygame.sprite.Group()
    num = len(platforms)
    Platform(platforms, num)
    player = Player(WIDTH // 2, HEIGHT // 2, platforms)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Шрифт и задняя картинка
    background_image = pygame.image.load('background.png').convert_alpha()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Открытие файла и взятие рекорда
    file = open("file.dat", "rb")
    try:
        best = pickle.load(file)
    except EOFError:
        best = 0

    # Цикл игры
    global SCORE
    running = True
    is_left = False
    is_right = False
    SCORE = 0
    platform_on_up = False
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # Ожидание закрытия окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    is_left = True
                    is_right = False
                elif event.key == pygame.K_d:
                    is_right = True
                    is_left = False
                elif event.key == pygame.K_ESCAPE:
                    pause()
            elif event.type == pygame.USEREVENT:
                platform_on_up = is_platform_on_up(platforms)
                if not platform_on_up:
                    num = len(platforms)
                    Platform(platforms, num)
                    platform_on_up = is_platform_on_up(platforms)
                    if random.randrange(5) == 1 and not platform_on_up:
                        num = len(platforms)
                        Platform(platforms, num)
                        platform_on_up = is_platform_on_up(platforms)
                    # elif random.randrange(6) == 1 and not platform_on_up:
                    #     num = len(platforms)
                    #     MovingPlatform(platforms, num)
                    #     platform_on_up = is_platform_on_up(platforms)

        # Обновление
        platforms.update()
        player.update(is_left, is_right)

        # Рендеринг
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        platforms.draw(screen)
        print_text("Счет: " + str(SCORE), 375, 10)
        print_text("Лучшее: " + str(best), 375, 32)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

        if player.rect.y >= HEIGHT:
            running = False

    pygame.quit()

    if SCORE > best:
        file.close()
        file = open("file.dat", "wb")
        pickle.dump(SCORE, file)

    file.close()


# Запуск прграммы, если не в модуле
if __name__ == '__main__':
    game_menu()
