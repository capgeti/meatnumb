import time
from src import bgui as bgui
import bge

__author__ = 'capgeti'

class DefaultView(bgui.System):

    def __init__(self):
        bgui.System.__init__(self, "guiStyle")
        self.clear_time = time.time()

        self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if
                       val.endswith('KEY') or val.startswith('PAD')}

    def main(self):
        mouse = bge.logic.mouse

        pos = list(mouse.position)
        pos[0] *= bge.render.getWindowWidth()
        pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])

        mouse_state = bgui.BGUI_MOUSE_NONE
        mouse_events = mouse.events

        if mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED: mouse_state = bgui.BGUI_MOUSE_CLICK
        elif mouse_events[
             bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED: mouse_state = bgui.BGUI_MOUSE_RELEASE
        elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE: mouse_state = bgui.BGUI_MOUSE_ACTIVE

        self.update_mouse(pos, mouse_state)

        keyboard = bge.logic.keyboard

        key_events = keyboard.events
        is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or\
                     key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE

        for key, state in keyboard.events.items():
            if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
                self.update_keyboard(self.keymap[key], is_shifted)

        bge.logic.getCurrentScene().post_draw = [self.render]
