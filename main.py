import pgzero
import math
import random
from pygame import Rect

# Game constants
GRID_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_WIDTH = SCREEN_WIDTH // GRID_SIZE
GAME_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3

class SpriteAnimation:
    def __init__(self, sprite_frames, frame_duration=0.3):
        self.sprite_frames = sprite_frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.frame_timer = 0

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)

    def get_current_sprite(self):
        return self.sprite_frames[self.current_frame]

class Character:
    def __init__(self, x, y, idle_frames, moving_frames):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * GRID_SIZE
        self.pixel_y = y * GRID_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.move_speed = 120
        self.idle_animation = SpriteAnimation(idle_frames, 0.8)
        self.moving_animation = SpriteAnimation(moving_frames, 0.2)

    def update(self, dt):
        if self.moving:
            self.moving_animation.update(dt)
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            distance = math.hypot(dx, dy)
            if distance < 2:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False
                try:
                    sounds.step.stop()
                except:
                    pass
            else:
                move_distance = self.move_speed * dt
                self.pixel_x += (dx / distance) * move_distance
                self.pixel_y += (dy / distance) * move_distance
        else:
            self.idle_animation.update(dt)

    def move_to(self, new_x, new_y, sound_enabled=True):
        if not self.moving:
            self.grid_x = new_x
            self.grid_y = new_y
            self.target_x = new_x * GRID_SIZE
            self.target_y = new_y * GRID_SIZE
            self.moving = True
            if sound_enabled:
                try:
                    if sounds.step.get_num_channels() == 0:
                        sounds.step.play(-1)
                except:
                    pass

    def get_current_sprite(self):
        return self.moving_animation.get_current_sprite() if self.moving else self.idle_animation.get_current_sprite()

    def draw(self, screen):
        current_sprite = self.get_current_sprite()
        try:
            screen.blit(current_sprite, (self.pixel_x, self.pixel_y))
        except:
            color = 'blue' if 'hero' in current_sprite else 'red'
            screen.draw.filled_rect(Rect(self.pixel_x + 2, self.pixel_y + 2, GRID_SIZE - 4, GRID_SIZE - 4), color)

class Hero(Character):
    def __init__(self, x, y):
        idle_frames = ['hero_idle1', 'hero_idle2', 'hero_idle3', 'hero_idle2']
        moving_frames = ['hero_walk1', 'hero_walk2', 'hero_walk3', 'hero_walk4']
        super().__init__(x, y, idle_frames, moving_frames)
        self.health = 3
        self.score = 0

class Enemy(Character):
    def __init__(self, x, y, patrol_points):
        idle_frames = ['enemy_idle1', 'enemy_idle2', 'enemy_idle3', 'enemy_idle2']
        moving_frames = ['enemy_walk1', 'enemy_walk2', 'enemy_walk3', 'enemy_walk4']
        super().__init__(x, y, idle_frames, moving_frames)
        self.patrol_points = patrol_points
        self.current_patrol_index = 0
        self.patrol_timer = 0
        self.patrol_delay = 1.5

    def update(self, dt, sound_enabled=True):
        super().update(dt)
        if not self.moving:
            self.patrol_timer += dt
            if self.patrol_timer >= self.patrol_delay:
                self.patrol_timer = 0
                next_point = self.patrol_points[self.current_patrol_index]
                self.move_to(*next_point, sound_enabled)
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)

class Treasure:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.collected = False
        self.animation = SpriteAnimation(['treasure1', 'treasure2', 'treasure3', 'treasure2'], 0.5)

    def update(self, dt):
        if not self.collected:
            self.animation.update(dt)

    def draw(self, screen):
        if not self.collected:
            current_sprite = self.animation.get_current_sprite()
            try:
                screen.blit(current_sprite, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE))
            except:
                size = GRID_SIZE // 2 + int(math.sin(self.animation.frame_timer * 8) * 2)
                offset = (GRID_SIZE - size) // 2
                screen.draw.filled_rect(Rect(self.grid_x * GRID_SIZE + offset, self.grid_y * GRID_SIZE + offset, size, size), 'yellow')

class Game:
    def __init__(self):
        self.state = MENU
        self.sound_enabled = True
        self.music_enabled = True
        self.menu_buttons = [
            {'text': 'Start Game', 'rect': Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50), 'action': 'start'},
            {'text': f'Sound: {"ON" if self.sound_enabled else "OFF"}', 'rect': Rect(SCREEN_WIDTH // 2 - 100, 270, 200, 50), 'action': 'sound'},
            {'text': 'Exit', 'rect': Rect(SCREEN_WIDTH // 2 - 100, 340, 200, 50), 'action': 'exit'}
        ]
        self.init_game()

    def generate_internal_walls(self):
        """Generate internal walls/barriers to make the game more challenging"""
        internal_walls = set()

        # Create some vertical barriers
        for i in range(3):
            start_x = random.randint(3, GAME_WIDTH - 4)
            start_y = random.randint(2, GAME_HEIGHT - 6)
            length = random.randint(3, 5)
            for j in range(length):
                if start_y + j < GAME_HEIGHT - 1:
                    internal_walls.add((start_x, start_y + j))

        # Create some horizontal barriers
        for i in range(3):
            start_x = random.randint(2, GAME_WIDTH - 6)
            start_y = random.randint(3, GAME_HEIGHT - 4)
            length = random.randint(3, 5)
            for j in range(length):
                if start_x + j < GAME_WIDTH - 1:
                    internal_walls.add((start_x + j, start_y))

        # Create some L-shaped barriers
        for i in range(2):
            corner_x = random.randint(4, GAME_WIDTH - 5)
            corner_y = random.randint(4, GAME_HEIGHT - 5)
            # Horizontal part
            for j in range(3):
                internal_walls.add((corner_x + j, corner_y))
            # Vertical part
            for j in range(3):
                internal_walls.add((corner_x, corner_y + j))

        # Remove walls that would block the hero's starting position
        internal_walls.discard((1, 1))
        internal_walls.discard((1, 2))
        internal_walls.discard((2, 1))

        return internal_walls

    def init_game(self):
        self.hero = Hero(1, 1)

        # Generate border walls
        self.walls = set()
        for x in range(GAME_WIDTH):
            self.walls.add((x, 0))
            self.walls.add((x, GAME_HEIGHT - 1))
        for y in range(GAME_HEIGHT):
            self.walls.add((0, y))
            self.walls.add((GAME_WIDTH - 1, y))

        # Add internal walls/barriers
        internal_walls = self.generate_internal_walls()
        self.walls.update(internal_walls)

        # Enemies with patrol routes that avoid walls
        self.enemies = []
        for _ in range(3):
            attempts = 0
            while attempts < 20:  # Prevent infinite loop
                start = (random.randint(5, GAME_WIDTH - 2), random.randint(3, GAME_HEIGHT - 2))
                if start not in self.walls and start != (1, 1):
                    patrol = [start]
                    for _ in range(3):
                        for attempt in range(10):
                            pos = (random.randint(3, GAME_WIDTH - 2), random.randint(3, GAME_HEIGHT - 2))
                            if pos not in self.walls:
                                patrol.append(pos)
                                break
                    if len(patrol) > 1:
                        self.enemies.append(Enemy(*start, patrol))
                        break
                attempts += 1

        # Treasures in random positions avoiding walls
        self.treasures = []
        positions = set()
        attempts = 0
        while len(positions) < 5 and attempts < 50:
            pos = (random.randint(2, GAME_WIDTH - 3), random.randint(2, GAME_HEIGHT - 3))
            if pos not in positions and pos != (1, 1) and pos not in self.walls:
                positions.add(pos)
            attempts += 1
        self.treasures = [Treasure(x, y) for x, y in positions]

        self.game_over_timer = 0
        if self.music_enabled and self.sound_enabled:
            try:
                music.play('background')
                music.set_volume(0.3)
            except:
                pass

    def is_valid_position(self, x, y):
        return 0 <= x < GAME_WIDTH and 0 <= y < GAME_HEIGHT and (x, y) not in self.walls

    def handle_click(self, pos):
        if self.state == MENU:
            for button in self.menu_buttons:
                if button['rect'].collidepoint(pos):
                    if button['action'] == 'start':
                        self.state = PLAYING
                        self.init_game()
                    elif button['action'] == 'sound':
                        self.sound_enabled = not self.sound_enabled
                        button['text'] = f'Sound: {"ON" if self.sound_enabled else "OFF"}'
                        # Stop all sounds when disabled
                        if not self.sound_enabled:
                            try:
                                sounds.step.stop()
                                music.stop()
                            except:
                                pass
                        # Start music when enabled
                        elif self.music_enabled and self.state == PLAYING:
                            try:
                                music.play('background')
                                music.set_volume(0.3)
                            except:
                                pass
                    elif button['action'] == 'exit':
                        exit()

    def handle_key(self, key):
        if self.state == PLAYING and not self.hero.moving:
            dx, dy = 0, 0
            if key == keys.UP: dy = -1
            elif key == keys.DOWN: dy = 1
            elif key == keys.LEFT: dx = -1
            elif key == keys.RIGHT: dx = 1
            new_x = self.hero.grid_x + dx
            new_y = self.hero.grid_y + dy
            if self.is_valid_position(new_x, new_y):
                self.hero.move_to(new_x, new_y, self.sound_enabled)
        elif self.state in [GAME_OVER, VICTORY] and key == keys.SPACE:
            self.state = MENU
            try:
                music.stop()
            except:
                pass

    def update(self, dt):
        if self.state == PLAYING:
            self.hero.update(dt)

            for enemy in self.enemies:
                enemy.update(dt, self.sound_enabled)
                if enemy.grid_x == self.hero.grid_x and enemy.grid_y == self.hero.grid_y and self.hero.health > 0:
                    self.hero.health = 0
                    self.state = GAME_OVER
                    self.game_over_timer = 2
                    try:
                        sounds.step.stop()
                        if self.sound_enabled:
                            sounds.hit.play()
                        music.stop()
                    except:
                        pass

            for treasure in self.treasures:
                treasure.update(dt)
                if not treasure.collected and treasure.grid_x == self.hero.grid_x and treasure.grid_y == self.hero.grid_y:
                    treasure.collected = True
                    self.hero.score += 10
                    try:
                        if self.sound_enabled:
                            sounds.collect.play()
                    except:
                        pass

            if all(t.collected for t in self.treasures):
                self.state = VICTORY
                try:
                    sounds.step.stop()
                    music.stop()
                except:
                    pass

    def draw(self):
        screen.clear()
        if self.state == MENU:
            screen.draw.text("Mini Dungeon Game", center=(SCREEN_WIDTH // 2, 100), fontsize=60, color="white")
            screen.draw.text("Navigate through the maze!", center=(SCREEN_WIDTH // 2, 150), fontsize=24, color="gray")
            for button in self.menu_buttons:
                screen.draw.filled_rect(button['rect'], "darkblue")
                screen.draw.text(button['text'], center=button['rect'].center, fontsize=32, color="white")
        elif self.state in [PLAYING, GAME_OVER, VICTORY]:
            # Draw floor tiles
            for x in range(GAME_WIDTH):
                for y in range(GAME_HEIGHT):
                    screen.draw.rect(Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), "gray")

            # Draw walls (both border and internal)
            for wall in self.walls:
                screen.draw.filled_rect(Rect(wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), "darkgray")

            # Draw treasures
            for treasure in self.treasures:
                treasure.draw(screen)

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(screen)

            # Draw hero
            self.hero.draw(screen)

            # Draw UI
            screen.draw.text(f"Score: {self.hero.score}", (10, 10), fontsize=32, color="white")
            screen.draw.text(f"Health: {self.hero.health}", (10, 40), fontsize=32, color="white")
            collected = sum(1 for t in self.treasures if t.collected)
            screen.draw.text(f"Treasures: {collected}/{len(self.treasures)}", (10, 70), fontsize=32, color="white")

            if self.state == GAME_OVER:
                screen.draw.text("GAME OVER", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), fontsize=80, color="red")
                screen.draw.text("Press SPACE to return", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), fontsize=30, color="white")

            if self.state == VICTORY:
                screen.draw.text("YOU WIN!", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), fontsize=80, color="lime")
                screen.draw.text(f"Final Score: {self.hero.score}", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), fontsize=40, color="white")
                screen.draw.text("Press SPACE to return", center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90), fontsize=30, color="white")

# Global game instance
game = Game()

def update(dt):
    game.update(dt)

def draw():
    game.draw()

def on_key_down(key):
    game.handle_key(key)

def on_mouse_down(pos):
    game.handle_click(pos)