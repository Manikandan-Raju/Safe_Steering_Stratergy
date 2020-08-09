from pygame.math import Vector2
from math import sin, radians, degrees
from uat.machine_spec import MachineSpec
machine_spec = MachineSpec()


class Car:
    def __init__(self):
        self.position = Vector2()
        self.velocity = Vector2()
        self.angle = 0.0
        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(min(self.velocity.x, machine_spec.top_speed), -machine_spec.top_speed)

        if self.steering:
            turning_radius = machine_spec.total_length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
