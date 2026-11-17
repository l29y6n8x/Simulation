import pygame


class Camera:
    def __init__(self, dt):
        self.dt = dt
        self.orientation = [0, 0]
        self.camera_distance = 300
        
        self.mouse_zoom_step = 10.0
        self.mouse_rotation_sensitivity = 0.35
        self.rotating_with_mouse = False



    def move_camera(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self.rotating_with_mouse = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            self.rotating_with_mouse = False
        elif event.type == pygame.MOUSEWHEEL:
            self.camera_distance = max(
                10,
                self.camera_distance - event.y * self.mouse_zoom_step,
            )
        elif event.type == pygame.MOUSEMOTION and self.rotating_with_mouse:
            horizontal, vertical = event.rel
            sensitivity = self.mouse_rotation_sensitivity
            self.orientation[0] -= vertical * sensitivity
            self.orientation[1] += horizontal * sensitivity

        return self.camera_distance, self.orientation



    