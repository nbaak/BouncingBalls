from colors import generate_random_color
import config


class Ball:

    def __init__(self, pos, speed, radius):
        self.pos = pos
        self.speed = speed
        self.radius = radius
        self.color = generate_random_color()
        self.weight = radius ** 2
        self.friction = config.FRICTION

    def move(self, gravity_enabled=True):
        if gravity_enabled:
            self.speed[1] += 0.1  # Apply gravity

        if gravity_enabled:
            self.speed[0] *= (1 - self.friction)  # Apply horizontal friction
            self.speed[1] *= (1 - self.friction)  # Apply vertical friction

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def check_collision(self, other_ball) -> bool:
        distance = ((self.pos[0] - other_ball.pos[0]) ** 2 +
                    (self.pos[1] - other_ball.pos[1]) ** 2) ** 0.5
        if distance <= self.radius + other_ball.radius:
            self.resolve_collision(other_ball)
            return True
        
        return False

    def resolve_collision(self, other_ball):
        direction = [other_ball.pos[0] - self.pos[0], other_ball.pos[1] - self.pos[1]]
        distance = ((direction[0]) ** 2 + (direction[1]) ** 2) ** 0.5
        if distance == 0:
            return

        normal = [direction[0] / distance, direction[1] / distance]
        tangent = [-normal[1], normal[0]]

        self_speed_normal = self.speed[0] * normal[0] + self.speed[1] * normal[1]
        self_speed_tangent = self.speed[0] * tangent[0] + self.speed[1] * tangent[1]
        other_speed_normal = other_ball.speed[0] * normal[0] + other_ball.speed[1] * normal[1]
        other_speed_tangent = other_ball.speed[0] * tangent[0] + other_ball.speed[1] * tangent[1]

        self_speed_normal, other_speed_normal = other_speed_normal, self_speed_normal

        self_speed = [self_speed_normal * normal[0] + self_speed_tangent * tangent[0],
                      self_speed_normal * normal[1] + self_speed_tangent * tangent[1]]
        other_speed = [other_speed_normal * normal[0] + other_speed_tangent * tangent[0],
                       other_speed_normal * normal[1] + other_speed_tangent * tangent[1]]

        self.speed = self_speed
        other_ball.speed = other_speed

        overlap = self.radius + other_ball.radius - distance
        separation = overlap / 2
        self.pos[0] -= separation * direction[0] / distance
        self.pos[1] -= separation * direction[1] / distance
        other_ball.pos[0] += separation * direction[0] / distance
        other_ball.pos[1] += separation * direction[1] / distance

    def handle_boundary_collision(self, window_width, window_height) -> bool:
        collision = False
        
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.speed[0] = abs(self.speed[0])
            collision = True
            
        elif self.pos[0] + self.radius > window_width:
            self.pos[0] = window_width - self.radius
            self.speed[0] = -abs(self.speed[0])
            collision = True

        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.speed[1] = abs(self.speed[1])
            collision = True
            
        elif self.pos[1] + self.radius > window_height:
            self.pos[1] = window_height - self.radius
            self.speed[1] = -abs(self.speed[1])
            collision = True
            
        return collision
