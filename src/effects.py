from time import sleep

from variables import ASSET_FOLDER, SCREEN_WIDTH
from entities import Entity, coordinate


class Effects:
    def __init__(self, screen):
        self.screen = screen

    def explosion(self, starting_pos: coordinate, delay: float = 0.08, ticks: int = 4) -> None:
        turtles = []
        main_t = Entity(starting_pos=starting_pos, visible=False)

        for i in range(1, ticks + 1):
            tur = main_t.clone()
            tur.shape(f"{ASSET_FOLDER}/Effects/Explosion{i}.gif")
            turtles.append(tur)

        for tur in turtles:
            tur.showturtle()
            self.screen.update()
            sleep(delay)
            tur.destroy()

    def multi_explosion(self, coordinates: list[coordinate], delay: float = 0.08) -> None:
        """
        Spawns and Updates Multiple Explosions at the same time\n
        :param coordinates: a list of tuples containing (x, y) coordinates which explosion will spawn at
        :param delay: the time to wait until all the turtles update
        """
        # This list will contain a list of Entities with the Explosion Effect gifs
        turtles: list[list[Entity]] = []

        for coord in coordinates:
            turtles.append([
                Entity(visible=False, shape=f"{ASSET_FOLDER}/Effects/Explosion{sprite_num}.gif", starting_pos=coord)
                for sprite_num in range(1, 5)
            ])

        turtle_queue: list[tuple[Entity]] = list(zip(*turtles))

        for turtle_li in turtle_queue:
            for tur in turtle_li:
                tur.showturtle()
            sleep(delay)
            self.screen.update()

        for idx, turtle_li in enumerate(turtle_queue[::-1]):
            for tur in turtle_li:
                tur.destroy()

        sleep(delay)
        self.screen.update()

    def startup_effect(self) -> None:
        """ Launches a 3, 2, 1. GO Effect """
        counter = Entity(starting_pos=(-30, -20), visible=False)
        self.screen.update()

        for i in range(3, 0, -1):
            counter.write(i, font=("Consolas", 100, "bold"))
            sleep(0.6)
            self.screen.update()
            counter.clear()

        coordinates = [xcor for xcor in range(SCREEN_WIDTH // 2 * -1, SCREEN_WIDTH // 2, 100)] + [400]
        sorted_coordinates = [0]

        for i in range(4, 0, -1):
            sorted_coordinates.extend([
                coordinates[i - 1], coordinates[i * -1],
            ])

        self.multi_explosion([(xcor, 0) for xcor in sorted_coordinates])
