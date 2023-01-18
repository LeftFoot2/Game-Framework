"""
Alien Game

Written in python using arcade and random library. 

"""

import random
import arcade

# Different variables for sizes or speeds so they can be adjusted easily.

bullet_size = .05
canon_size = .2
alien_size = .2
alien_speed = -1
player_speed = 5
bullet_speed = 5

# Determine screen size.
screen_width = 600
screen_height = 800
screen_title = "Alien Game"

class Start_Screen(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLUE)

    
    def on_draw(self):
        self.clear()
        arcade.draw_text('Alien Game', screen_width / 2, screen_height / 1.75, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text('Click to start', screen_width / 2, screen_height / 1.75 - 75, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press: 'A' to move left, 'D' to move right, Spacebar to shoot", screen_width / 2, screen_height / 1.75 - 135, arcade.color.WHITE, font_size=10, anchor_x="center")


    def on_mouse_press(self, x, y, button, modifiers):
        game_view = Alien_Game()
        game_view.setup()
        self.window.show_view(game_view)

class End_Screen(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('End_game_alien.png')

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(screen_width / 2, screen_height / 2, screen_width, screen_height)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        
        if symbol == arcade.key.ENTER:
            game_view = Alien_Game()
            game_view.setup()
            self.window.show_view(game_view)


class Alien_Game(arcade.View):#Window):


    # Used to initiate main variables.
    def __init__(self):

        super().__init__()#screen_width, screen_height, screen_title)

        self.texture = arcade.load_texture('alien_game_background.png')


        self.alien_list = None
        self.bullet_list = None
        self.canon_list = None
        self.person_list = None
        self.earth_list = None

        self.earth_health = 3

        self.player = None
        self.alien = None
        self.background = None


    # This is the set up to get the game started.
        
    def setup(self):


        # I couldn't figure out how to just set the background to my image so I made it into a sprite.


        # self.background = arcade.Sprite('alien_game_background.png', 1.15)
        # self.background.center_x = 325
        # self.background.center_y = 425



        # Make each list a sprite list append sprites to later.

        self.alien_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.canon_list = arcade.SpriteList()
        self.person_list = arcade.SpriteList()
        self.earth_list = arcade.SpriteList()


        # The earth need to be a sprite to the aliens could clyde with it.

        self.earth = arcade.Sprite('earth_alien_game.png', 1)
        self.earth.center_x = screen_width / 2
        self.earth.center_y = 219
        self.earth_list.append(self.earth)


        # The cannon is can now be seen on the earths surface and bullets will shoot from it later.

        self.player = arcade.Sprite('canon2.png', canon_size)
        self.player.center_x = screen_width / 2
        self.player.center_y = 100
        self.person_list.append(self.player)

        # These two lines were added to the setup so that they didn't lag the game later when trying to get them going.

        self.bullet = arcade.Sprite("alien_bullet.png", bullet_size)
        self.alien = arcade.Sprite("alien.png", alien_size)

        # Determines the speed at which aliens come.

        arcade.schedule(self.add_alien, 1)


    # Function adds alien to top of the screen at a random x coordinate.

    def add_alien(self, delta_time: float):
        self.alien = arcade.Sprite("alien.png", alien_size)

        self.alien.change_y = alien_speed

        self.alien.bottom = screen_height
        self.alien.left = random.randint(0, screen_width - 70)
        self.alien_list.append(self.alien)


    # Determines if user pressed down on a key.

    def on_key_press(self, symbol, modifiers):
        
        # Pressing D will move player to the right.

        if symbol == arcade.key.D:
            self.player.change_x += player_speed

        # Pressing A will move player to the left.

        if symbol == arcade.key.A:
            self.player.change_x -= player_speed

        # Pressing the spacebar will create and shoot a bullet out of cannon.

        if symbol == arcade.key.SPACE:

            self.bullet = arcade.Sprite("alien_bullet.png", bullet_size)

            self.bullet.change_y = bullet_speed

            self.bullet.center_x = self.player.center_x + 2
            self.bullet.bottom = self.player.top

            self.bullet_list.append(self.bullet)


    def on_key_release(self, symbol, modifiers):

        # Used to stop player from moving after key release.
        print(self.player.change_x)
    
        if symbol == arcade.key.D:

            self.player.change_x -= player_speed

        if symbol == arcade.key.A:
            self.player.change_x += player_speed

    # Function allows for the game to update frequently. Allowing for movement of sprits.

    def on_update(self, delta_time):

        # These are the three sprits that are moving or getting removed from the memory.

        self.alien_list.update()
        self.player.update()
        self.bullet_list.update()

        # Used to check if an alien has hit the earth and if so removes a health from the earth.

        for alien in self.alien_list:

            hit_earth = arcade.check_for_collision_with_list(alien, self.earth_list)

            if hit_earth:
                alien.remove_from_sprite_lists()
                self.earth_health -= 1

                # If the earth losses all its health it will close the window.

                if self.earth_health < 1:
                    game_over_view = End_Screen()
                    self.window.show_view(game_over_view)


        # Used to remove bullets if they hit an allen or go off the top of the screen.

        for bullet in self.bullet_list:

            hit_alien = arcade.check_for_collision_with_list(bullet, self.alien_list)

            if bullet.bottom > 800:
                bullet.remove_from_sprite_lists()

            if hit_alien:

                bullet.remove_from_sprite_lists()

                for alien in hit_alien:

                    alien.remove_from_sprite_lists()


        # Prevents player form going of the screen.

        if self.player.right > screen_width:
            self.player.right = screen_width

        if self.player.left < 0:
            self.player.left = 0

    # Draws all the sprites onto the window.

    def on_draw(self):

        self.clear()

        arcade.start_render()

        # self.background.draw()
        self.texture.draw_sized(screen_width/2, screen_height/2, screen_width, screen_height)
        self.earth_list.draw()
        self.person_list.draw()
        self.alien_list.draw()
        self.bullet_list.draw()
        
# Starts the game.

if __name__ == '__main__':
    window = arcade.Window(screen_width, screen_height, screen_title)
    # game = Alien_Game()
    start_view = Start_Screen()
    window.show_view(start_view)
    # game.setup()
    arcade.run()




