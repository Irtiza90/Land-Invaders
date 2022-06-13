import random
from turtle import Turtle

from variables import ASSET_FOLDER, tank_assets

coordinate = tuple[float, float]


class Entity(Turtle):
    def __init__(
            self, shape: str = None, starting_pos: coordinate = (0, 0),
            visible: bool = True, facing_angle: float = 90
    ):
        """
        Base Class For All Entities(Player, Enemy, Bullet)

        :param shape: the shape of the entity must be a valid turtle shape or a .gif file
        :param starting_pos: Tuple with (x, y) coordinates which entity will spawn at
        :param visible: if the entity is visible or not
        :param facing_angle: The direction in which entity will face after spawning(default = 90 NORTH)
        """
        super(Entity, self).__init__(shape="classic" if shape is None else shape, visible=visible)
        self.penup()
        self.speed(0)
        self.setpos(starting_pos)
        self.seth(facing_angle)

    def destroy(self) -> None:
        self.reset()
        self.hideturtle()


class Enemy(Entity):
    def __init__(self, starting_pos: coordinate = (0, 0)):
        """
        Create an Enemy Instance\n
        :param starting_pos: tuple with (x, y) coordinates which enemy will spawn at.
        """
        super(Enemy, self).__init__(
            shape=ASSET_FOLDER + random.choice(tank_assets[:-1]),
            starting_pos=starting_pos
        )


class Player(Entity):
    def __init__(self, starting_pos: coordinate, visible=True):
        """
        Create a Player Instance\n
        :param starting_pos: tuple with (x, y) coordinates which enemy will spawn at.
        :param visible: if the entity is visible or not
        """
        self._starting_pos = starting_pos
        self.can_shoot: bool = True
        super(Player, self).__init__(
            shape=ASSET_FOLDER + tank_assets[-1], visible=visible, starting_pos=starting_pos
        )

    def move_right(self):
        if (crr_xcor := self.xcor()) < 370:
            self.setx(crr_xcor + 20)

    def move_left(self):
        if (crr_xcor := self.xcor()) > -370:
            self.setx(crr_xcor - 20)

    def toggle_can_shoot(self, can_shoot: bool) -> None:
        """ Toggles the self.can_shoot instance variable """
        self.can_shoot = can_shoot

    def reset(self):
        """ Return The Player Back To its original Place. """
        self.setpos(self._starting_pos)
        self.showturtle()


class Bullet(Entity):
    def __init__(self, *, facing: str, from_pos: coordinate):
        """
        Spawns a Bullet on the Screen

        :param facing: The Direction to face, must be either "N" or "S"
        :param from_pos: (x, y) position to start from
        :raises ValueError: if facing != "N" or "S"
        """
        # ------------ Calculation Of Directions ----- #
        directions = {
            "N": {"sprite": "Exhaust_Fire_up.gif", "facing_angle": 90},
            "S": {"sprite": "Exhaust_Fire_down.gif", "facing_angle": 270}
        }

        val = directions.get(facing)
        if val is None:
            raise ValueError('"facing" Must be only "N" or "S".')

        # ---------------------------------------------------------- #
        self.facing = facing

        super(Bullet, self).__init__(
            shape=f"{ASSET_FOLDER}/Effects/{val['sprite']}", starting_pos=from_pos, facing_angle=val['facing_angle']
        )
        self.forward(20)

    @property
    def can_move(self) -> bool:
        # If bullet's x is between 480 and -480, and it's y is between 320 and -320, then it can move
        ycor = self.ycor()
        return -480 < ycor < 480 and -320 < ycor < 320

    def move(self) -> None:
        """ Moves the Bullet up/down depending on its direction. """
        self.forward(30)

    def collided_with_entity(self, entity: Entity) -> bool:
        """
        :param entity: Object to check collision with
        :returns: True if Collision Happened, else False
        """
        return entity.distance(self.pos()) <= 40


class Score:
    def __init__(self):
        self.score = 0
        self._turtle = Entity(starting_pos=(320, -250), visible=False)
        self._update_score()

    def _update_score(self):
        self._turtle.clear()
        self._turtle.write(self.score, font=("Terminal", 40, "normal"))

    def increase_score(self, amount: int = 1):
        self.score += amount
        self._update_score()

    def set_score(self, amount: int):
        self.score = amount
        self._update_score()
