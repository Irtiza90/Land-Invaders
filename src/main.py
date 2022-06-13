import time
import random
from functools import partial
from turtle import Screen

from entities import Enemy, Player, Bullet, Entity, Score
from effects import Effects
from variables import (
    tank_assets, effect_assets,
    ASSET_FOLDER, SCREEN_WIDTH, SCREEN_HEIGHT,
)

# Creating Custom Type
Tank = Enemy | Player


class SpaceInvaders:
    def __init__(self):
        """ Main Game Class """
        self.enemies: list[Enemy] = []
        self.bullets: list[Bullet] = []
        self.player: Player | None = None
        self.running: bool = True

        # Setting it all up
        self.screen = Screen()
        self.effects = Effects(screen=self.screen)
        self.score_manager = Score()

        self.setup_game()

    def load_sprites(self) -> None:
        """ Loads all the Sprites """
        for sprite in (tank_assets + effect_assets):
            self.screen.register_shape(ASSET_FOLDER + sprite)

    def setup_game(self) -> None:
        """ Sets up the screen, sprites, player and key binds """
        # Setting up the screen
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.bgpic(f"{ASSET_FOLDER}/Effects/bg-desert.png")
        self.screen.tracer(0)

        # Loading all Sprites
        self.load_sprites()

        # Setting up the Player
        self.player = Player(starting_pos=(0, -260))

        # Spawning Random Tire Tracks
        tracks = ('/Effects/Tire_Track_1.gif', '/Effects/Tire_Track_2.gif')

        for _ in range(10):
            ycor = random.randrange(SCREEN_HEIGHT // 2 * -1, (SCREEN_HEIGHT // 2))
            xcor = random.randrange(SCREEN_WIDTH // 2 * -1, (SCREEN_WIDTH // 2))

            Entity(shape=ASSET_FOLDER + random.choice(tracks), starting_pos=(xcor, ycor))

        # Setting up the screen binds
        self.screen.onkeypress(fun=self.player.move_right, key="Right")
        self.screen.onkeypress(fun=self.player.move_left, key="Left")
        self.screen.onkey(
            fun=lambda: (partial(self.shoot, entity=self.player)(), self._start_player_shoot_cooldown()),
            key="space"
        )
        self.screen.listen()

    def shoot(self, *, entity: Tank) -> None:
        """
        :param entity: entity that will shoot, Must be a Player or Enemy Instance
        :raises TypeError: If entity is not an instance of Player or Enemy
        """
        facing_directions = {
            Player: "N", Enemy: "S"
        }

        bullet_facing_direction = facing_directions.get(type(entity))

        if bullet_facing_direction is None:
            raise TypeError('parameter "entity" must be of type Player or Enemy')

        # From Player
        if bullet_facing_direction == "N":
            if self.player.can_shoot is False:
                return
            else:
                # Resets it
                self.player.can_shoot = False

        bullet = Bullet(facing=bullet_facing_direction, from_pos=entity.pos())
        self.bullets.append(bullet)

    def move_bullets(self) -> None:
        """
        Moves all the Bullets on the screen one by one\n
        Checks if the bullet can move if it can then just move it, \n
        otherwise destroy the bullet, Also Detects Collision and deletes the enemy/player
        """
        for bullet in self.bullets[:]:  # loops in a copy of the list
            bullet_ycor = bullet.ycor()

            # The Bullet is out of the screen
            if bullet_ycor > 250 or bullet_ycor < -300:
                self.bullets.remove(bullet)
                bullet.destroy()

            # Means this bullet is from Player
            if bullet.facing == "N":
                if bullet_ycor < 60:
                    # just moves the bullet because enemy starts appearing  at ycor > 60
                    bullet.move()
                    continue

                for enemy in self.enemies[:]:
                    if bullet.collided_with_entity(enemy):
                        bullet.destroy()
                        enemy.destroy()
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score_manager.increase_score()
                        break

                # Moves the bullet if it had not been collided
                else:
                    bullet.move()

            # Bullet is From enemy
            else:
                # just moves the bullet because player's y-cor is after ycor -200
                if bullet_ycor > -200:
                    pass

                elif bullet.collided_with_entity(self.player):
                    bullet.destroy()
                    self.bullets.remove(bullet)
                    # Game will End
                    self.running = False

                bullet.move()

    @property
    def can_spawn_enemies(self) -> bool:
        # if self.enemies is empty returns True, otherwise return False
        return True if not self.enemies else False

    def spawn_enemies(self) -> None:
        screen_pos_width = int(SCREEN_WIDTH / 2)  # 400
        screen_neg_width = screen_pos_width * -1  # -400

        row_height = 300

        for _ in range(2):
            row_height -= 100
            for i in range(screen_pos_width-50, screen_neg_width, -50):
                en = Enemy(starting_pos=(i, row_height))
                self.enemies.append(en)

    def _start_player_shoot_cooldown(self):
        self.player.can_shoot = False
        self.screen.ontimer(
            t=1000, fun=partial(self.player.toggle_can_shoot, can_shoot=True)
        )

    def run(self) -> None:
        self.effects.startup_effect()

        while self.running:
            if self.can_spawn_enemies:
                if self.score_manager.score:
                    self.score_manager.increase_score(10)

                self.spawn_enemies()
                self.screen.update()
                time.sleep(0.8)
                continue

            self.move_bullets()

            for enemy in self.enemies:
                if random.randint(0, 40) == 0:
                    self.shoot(entity=enemy)

            self.screen.update()
            time.sleep(0.05)

        else:
            # Player is Dead
            self.end_game()

    def restart_game(self):
        self.running = True
        self.score_manager.set_score(0)
        self.player.reset()

        for enemy in self.enemies:
            enemy.destroy()

        self.enemies.clear()
        self.bullets.clear()
        self.run()

    def end_game(self) -> None:
        self.effects.explosion(self.player.pos())
        self.player.destroy()

        for bullet in self.bullets:
            bullet.destroy()
            time.sleep(0.02)
            self.screen.update()

        self.restart_game()


def main() -> None:
    game = SpaceInvaders()
    game.run()


if __name__ == "__main__":
    main()
