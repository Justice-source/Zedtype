import copy
import pygame
import random

pygame.init()

# Load words from a text file
def load_words(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

wordlist = load_words('english3.txt')

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Zedtype - Typing game in python')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

score = 0

# Load in assets like fonts, sound effects, and music
footer_font = pygame.font.Font('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/fonts/Square.ttf', 30)
pause_font = pygame.font.Font('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/fonts/1up.ttf', 38)
banner_font = pygame.font.Font('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/fonts/1up.ttf', 28)
font = pygame.font.Font('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/fonts/AldotheApache.ttf', 48)

# music and sounds
pygame.mixer.init()
pygame.mixer.music.load('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/sounds/click.mp3')
woosh = pygame.mixer.Sound('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/sounds/Swoosh.mp3')
wrong = pygame.mixer.Sound('C:/Users/JUSTICE/Videos/TYPING GAME PROJECT/assets/sounds/Instrument Strum.mp3')
click.set_volume(0.3)
woosh.set_volume(0.2)
wrong.set_volume(0.3)

# game variables
level = 1
lives = 10
word_objects = []
file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0]) if read else 0  # Fixed to read the high score from the file
file.close()
pz = True
new_level = True
submit = ''
active_string = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
choices = [False, True, False, False, False, False, False]
len_indexes = [2, 4, 6, 8, 10, 12]  # Updated the len_indexes to reflect actual lengths

# Classes for Word
class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    # Functions of the Word class 
    def draw(self):
        color = 'black'
        screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed

# Classes for buttons
class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    # Function of the button class
    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))

# screen outlines for background shapes and title bar areas
def draw_screen():
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (800, HEIGHT - 100), (800, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)

    # Text for showing the current level and player's current input, high score, score, and lives
    screen.blit(footer_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 75))
    screen.blit(footer_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 75))

    # Put pause button here
    pause_btn = Button(890, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    screen.blit(banner_font.render(f'Score: {score}', True, 'black'), (250, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'black'), (550, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'black'), (10, 10))
    return pause_btn.clicked

# Function for how the pause button works
def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resume_btn = Button(160, 200, '>', False, surface)
    resume_btn.draw()

    quit_btn = Button(410, 200, 'X', False, surface)
    quit_btn.draw()
    surface.blit(footer_font.render('MENU', True, 'white'), (110, 110))
    surface.blit(footer_font.render('PLAY!', True, 'white'), (210, 175))
    surface.blit(footer_font.render('QUIT', True, 'white'), (450, 175))
    surface.blit(footer_font.render('Active Letter Lengths:', True, 'white'), (110, 250))

    # Range of the length of words
    for i in range(len(choices)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            choice_commits[i] = not choice_commits[i]
        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i * 80), 350), 35, 5)
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked

# How the levels will increment depending on how your score increases
def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(min(len(choices), len(len_indexes))):
     if choices[i]:
        include.append((len_indexes[i], len_indexes[i] + 2))

    for i in range(level):
        speed = random.randint(3, 3)
        y_pos = random.randint(10 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        while True:
            text = random.choice(wordlist).lower()
            if any(start <= len(text) < end for start, end in include):
                break
        new_word = Word(text, speed, y_pos, x_pos)
        word_objs.append(new_word)
    return word_objs

# Function to check if the answer you typed for the displayed word you chose is correct
def check_answer(scor):
    to_remove = []
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            scor += int(points)
            to_remove.append(wrd)
            woosh.play()
    for wrd in to_remove:
        word_objects.remove(wrd)
    return scor

# Function to check and export high score, if the loop is exited- Your score will be exported to the txt file in the folder
def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open('high_score.txt', 'w') as file:
            file.write(str(int(high_score)))

# Code block that contains the main game loop that is required to keep the game running
# a variable is created to be constantly active until we are ready to exit the game
run = True
while run:
    screen.fill('gray')
    timer.tick(fps)
    pause_butt = draw_screen()
    if pz:
        resume_butt, changes, quit_butt = draw_pause()
        if resume_butt:
            pz = False
        if quit_butt:
            check_high_score()
            run = False
    if new_level and not pz:
        word_objects = generate_level()
        new_level = False
    else:
        to_remove = []
        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
            if w.x_pos < -200:
                to_remove.append(w)
                lives -= 1
        for w in to_remove:
            word_objects.remove(w)
    if len(word_objects) <= 0 and not pz:
        level += 1
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False

        if event.type == pygame.KEYDOWN:
            if not pz:
                if event.unicode.lower() in letters:
                    active_string += event.unicode
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                pz = not pz
        if event.type == pygame.MOUSEBUTTONUP and pz:
            if event.button == 1:
                choices = changes

    if pause_butt:
        pz = True

    if lives < 0:
        pz = True
        level = 1
        lives = 10
        word_objects = []
        new_level = True
        check_high_score()
        score = 0

    pygame.display.flip()
pygame.quit()
