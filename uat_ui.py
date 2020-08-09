import pygame
from uat.uat_mechanics import Car
from uat.machine_spec import MachineSpec
from math import copysign
import os


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Safety Steering Strategy")
        width: int = 1280
        height: int = 960
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "uat.png")
        car_image = pygame.image.load(image_path)
        car = Car()
        machine_spec = MachineSpec()
        ppu: int = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = machine_spec.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -machine_spec.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * machine_spec.brake_deceleration:
                    car.acceleration = -copysign(machine_spec.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * machine_spec.free_deceleration:
                    car.acceleration = -copysign(machine_spec.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(min(car.acceleration, machine_spec.max_acceleration), -machine_spec.max_acceleration)

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-machine_spec.max_steering_angle, min(car.steering, machine_spec.max_steering_angle))

            # Logic
            car.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            x_pos = car.position.x * ppu - rect.width / 2
            y_pos = car.position.y * ppu - rect.height / 2
            self.screen.blit(rotated, (x_pos, y_pos))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()
