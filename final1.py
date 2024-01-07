# necessary libraries
import pygame
import random
import button

# Initialize Pygame
pygame.init()
pygame.mixer.init()# for music

# clock and frames per second
clock = pygame.time.Clock()
fps = 60

# screen dimensions
bottom_panel = 150
screen_width = 700
screen_height = 400 + bottom_panel

# Pygame display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('RayBlade')

# background music
pygame.mixer.music.load('mainmen.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Define game variables
current_user = 1
total_users = 3
action_cooldown = 0
action_wait_time = 100
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

# Define fonts and colors
font = pygame.font.SysFont('Times New Roman', 26)
red = (255, 0, 0)
green = (0, 255, 0)   #for the healthbar

# Load images
background_img = pygame.image.load('image/main1/background.jpg').convert_alpha()
panel_img = pygame.image.load('image/main1/panel.png').convert_alpha()
potion_img = pygame.image.load('image/main1/potion.png').convert_alpha()
restart_img = pygame.image.load('image/main1/restart.png').convert_alpha()
victory_img = pygame.image.load('image/main1/victory.png').convert_alpha()
defeat_img = pygame.image.load('image/main1/defeat.png').convert_alpha()
sword_img = pygame.image.load('image/main1/sword.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (30, 30))#changing size of sword

# Function for drawing text with an outline
def draw_text(text, font, text_col, x, y, size=26, bold=False):
    # Set up font
    font_style = 'Calibri'
    custom_font = pygame.font.SysFont(font_style, size)
    custom_font.set_bold(bold)

    # Render text with black outline
    text_surface = custom_font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x - 1, y - 1))
    screen.blit(text_surface, (x + 1, y - 1))
    screen.blit(text_surface, (x - 1, y + 1))
    screen.blit(text_surface, (x + 1, y + 1))

    # Render the actual text
    text_surface = custom_font.render(text, True, text_col)
    screen.blit(text_surface, (x, y))

# Function for drawing dialogue
def draw_dialogue(dialogue, x, y):
    draw_text(dialogue, font, red, x, y, size=20)

# Function for drawing the background
def draw_bg():
    screen.blit(background_img, (0, 0))

# Function for drawing the panel
def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    
    draw_text(f'{darknight.name} HP: {darknight.hp}', font, red, 40, screen_height - bottom_panel - 320, bold=True, size=23)
    draw_text(f'{monster1.name} HP: {monster1.hp}', font, red, 550, (screen_height - bottom_panel - 320), bold=True, size=23)
    draw_text(f'{monster2.name} HP: {monster2.hp}', font, red, 380, (screen_height - bottom_panel - 320), bold=True, size=23)

# Class definition for user
class User():
    def __init__(self, x, y, name, max_hp, strength, potions):
        # Initialize user attributes
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  
        self.update_time = pygame.time.get_ticks()

        # Load idle images
        temp_list = []
        for i in range(24):
            img = pygame.image.load(f'image/main1/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0.4))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(24):
            img = pygame.image.load(f'image/main1/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0.4))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load hurt images
        temp_list = []
        for i in range(24):
            img = pygame.image.load(f'image/main1/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0.4))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load death images
        temp_list = []
        for i in range(24):
            img = pygame.image.load(f'image/main1/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Update user's animation and handle cooldown
        animation_cooldown = 50

        # Update image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # Set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Perform attack on the target and handle animations
        rand = random.randint(-3, 8)
        damage = self.strength + rand
        target.hp -= damage
        target.hurt()

        # Check if the target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        # Attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # Handle hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # Handle death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        # Reset user attributes
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        # Draw the user on the screen
        screen.blit(self.image, self.rect)

# Class definition for HealthBar
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        # Initialize HealthBar attributes
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, current_hp):
        # Draw the health bar on the screen
        ratio = current_hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

# Create instances of user and HealthBar
darknight = User(200, 260, 'DarKnight', 30, 12, 3)
monster1 = User(500, 270, 'monster', 20, 5, 1)
monster2 = User(400, 270, 'monster', 20, 5, 1)

monster_list = [monster1, monster2]

darknight_health_bar = HealthBar(40, screen_height - bottom_panel - 290, darknight.hp, darknight.max_hp)
monster1_health_bar = HealthBar(550, screen_height - bottom_panel - 290, monster1.hp, monster1.max_hp)
monster2_health_bar = HealthBar(380, screen_height - bottom_panel - 290, monster2.hp, monster2.max_hp)

# Create buttons
potion_button = button.Button(screen, 70, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 300, 100, restart_img, 120, 50)

# Define starting time
start_time = pygame.time.get_ticks()

# Function to draw the timer
def draw_timer():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = f'Time: {minutes:02d}:{seconds:02d}'
    draw_text(timer_text, font, red, screen_width // 2 - 60, 10)

# Variables for tracking wave progress
current_wave = 1
max_waves = 5

# Main game loop
run = True
while run:
    clock.tick(fps)

    draw_bg()
    draw_panel()
    darknight_health_bar.draw(darknight.hp)
    monster1_health_bar.draw(monster1.hp)
    monster2_health_bar.draw(monster2.hp)

    # Display the current wave in the top left corner
    draw_text(f'Wave: {current_wave}/{max_waves}', font, red, 10, 10)

    darknight.update()
    darknight.draw()

    # Check if monsters reach 50% HP and display dialogue
    for monster in monster_list:
        if 0.5 * monster.max_hp <= monster.hp < monster.max_hp:
            draw_dialogue(f"{monster.name}: Foolish Human", 100, screen_height - bottom_panel + 15)

        monster.update()
        monster.draw()
    
    draw_timer()
    # this is variables for the actions
    attack = False
    potion = False
    target = None
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, monster in enumerate(monster_list):
        # If the mouse is over a monster it will show a sword 
        if monster.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)
            if clicked == True and monster.alive == True:
                attack = True
                target = monster_list[count]
    # for if the potion button is clicked
    if potion_button.draw():
        potion = True
    draw_text(str(darknight.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:
        if darknight.alive == True:
            if current_user == 1:
                action_cooldown += 1
                 # If monster's HP is below 50% and it has potions it will use it 
                if action_cooldown >= action_wait_time:
                    if attack == True and target != None:
                        darknight.attack(target)
                        current_user += 1
                        action_cooldown = 0
                        # If the potion is selected it will check if there are potions available and if there is it will use it 
                    if potion == True:
                        if darknight.potions > 0:
                            if darknight.max_hp - darknight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = darknight.max_hp - darknight.hp
                            darknight.hp += heal_amount
                            darknight.potions -= 1
                            current_user += 1
                            action_cooldown = 0
        else:
            # If darknight is defeated it will set game over state to -1
            game_over = -1

        for count, monster in enumerate(monster_list):
            if current_user == 2 + count:
                if monster.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        if (monster.hp / monster.max_hp) < 0.5 and monster.potions > 0:
                            if monster.max_hp - monster.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = monster.max_hp - monster.hp
                            monster.hp += heal_amount
                            monster.potions -= 1
                            current_user += 1
                            action_cooldown = 0
                        else:
                            # If conditions arent met, monster attack
                            monster.attack(darknight)
                            current_user += 1
                            action_cooldown = 0
                else:
                    # If the monster is defeated, move to the next turn
                    current_user += 1
# Reset turn counter after darknight and monsters have taken their turns
        if current_user > total_users:
            current_user = 1
# Check the number of alive monsters
    alive_monsters = 0
    for monster in monster_list:
        if monster.alive == True:
            alive_monsters += 1
    if alive_monsters == 0:
        current_wave += 1
        if current_wave > max_waves:
            game_over = 1
        else:
            # Reset the users for the next wave
            for monster in monster_list:
                monster.reset()
            darknight.reset()
            current_user = 1

        if current_wave == 5:
            # Stop the current music
            pygame.mixer.music.stop()

            # Load and play new music for wave 5
            pygame.mixer.music.load('startmen.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

# Display victory or defeat images and check for restart button click
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (-300, -300))
        if game_over == -1:
            screen.blit(defeat_img, (250, 200))
        if restart_button.draw():
            darknight.reset()
            for monster in monster_list:
                monster.reset()
            current_user = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
