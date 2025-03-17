from raylibpy import *
from enum import Enum, auto
from os.path import join
import json
from sys import exit
from math import *

class Game:
    def __init__(self):
        # Window Setting
        init_window(1920 / 1.2, 1080 / 1.2, "dialogue test")

        # Scene Mangement
        self.scene_manager = SceneMangager(self)
        self.current_scene = None
        self.scene_manager.start_scene("main_menu")

        # Game Management
        self.time_scale = 1
        self.delta_time = get_frame_time() * self.time_scale
        set_target_fps(144)

        self.camera = Camera2D(Vector2(get_screen_width() / 2, get_screen_height() / 2), Vector2(0, 0), 0, 1)
        self.camera_speed = 3
        
    def game_update(self):
        # Game Management
        self.delta_time = get_frame_time() * self.time_scale
        
    def run(self):
        while not window_should_close():
            self.game_update()
            self.currentScene.update()

            self.currentScene.draw()
        close_window()

class SceneMangager:
    def __init__(self, game : Game):
        self.scenes : dict[str, Scene] = {
            "main_menu" : MainMenu(game),
            "main_game" : GameScene(game),
        }

        self.game = game

    def start_scene(self, scene_name : str):
        if self.game.current_scene != None : self.game.current_scene.on_scene_disable()
        selectedScene = self.scenes[scene_name]
        selectedScene.on_scene_enable()
        self.game.currentScene = selectedScene

#이 씬 클래스에 뭔가를 넣으면 모든 씬에 적용된다
class Scene:
    def __init__(self, game : Game):
        self.game = game

    #씬이 활성화 될때 불림.
    def on_scene_enable(self):
        pass

    def on_scene_disable(self):
        pass

    #씬이 활성화되고 매프레임마다 불림.
    def update(self):
        pass

    #총 렌더.
    def draw(self):
        pass

class MainMenu(Scene):
    def __init__(self, game : Game):
        super().__init__(game)

    def update(self):
        super().update()
        if (is_key_pressed(KEY_SPACE)):
            self.game.scene_manager.start_scene("main_game")

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        draw_text("Main Menu", 100, 100, 80, WHITE)

        end_drawing()

class GameScene(Scene):
    def __init__(self, game : Game):
        super().__init__(game)

        self.assets = {
            "image_big" : load_texture("New Piskel.png")
        }
        
        self.x_margin = 50
        self.texts = ["this is text test.\nabcdefghijklmnopqrstuvxyz\ni am motbam.", "this is second motbam desune~~."]
        self.current_text = ""
        self.speed = 5
        self.len = 0
        self.is_end = False
        self.current_index = 0

    def on_scene_enable(self):
        super().on_scene_enable()
        self.game.camera.zoom = 1.5

    def on_scene_disable(self):
        super().on_scene_disable()
        self.game.camera.zoom = 1

    def update(self):
        super().update()

        if self.is_end == False and self.len < self.speed:
            self.len += 1
        if self.len == self.speed:
            self.len = 0
            self.current_text = self.texts[self.current_index][0:len(self.current_text) + 1]

        if len(self.current_text) == len(self.texts[self.current_index]):
            self.is_end = True

        if self.is_end and is_key_pressed(KEY_SPACE):
            self.is_end = False
            self.current_index += 1
            self.len = 0
            self.current_text = self.texts[self.current_index][0]

    def draw(self):
        begin_drawing()
        clear_background(BLANK)

        # UI DRAW ##################################
        draw_texture(self.assets["image_big"], 800, 50, WHITE)
        draw_rectangle_rec(Rectangle(self.x_margin, get_screen_height() - 350, get_screen_width() - self.x_margin * 2, 300), RED)
        draw_text(self.current_text, 100, get_screen_height() - 300, 50, WHITE)
        draw_fps(20, 20)
        # UI DRAW END ##############################

        end_drawing()

if __name__ == "__main__":
    game = Game()
    game.run()