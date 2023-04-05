import pygame
import sys
import random

pygame.init()

# Screen dimensions
WIDTH = 1000
HEIGHT = 750

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
paddle_width = 40
paddle_height = 150
paddle_speed = 8  # Increased paddle movement speed

# Ball settings
ball_width = 20
ball_height = 20
ball_speed_x = 7
ball_speed_y = 7

max_ball_speed = 50

# Fonts
font = pygame.font.Font(None, 36)


def draw_objects(screen, left_paddle, right_paddle, ball, score):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, left_paddle)
    pygame.draw.rect(screen, BLACK, right_paddle)
    pygame.draw.ellipse(screen, BLACK, ball)
    pygame.draw.aaline(screen, BLACK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    # Display the score with "Score: " text
    score_surface = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_surface, (WIDTH // 2 + 10, 10))


def ai_move(paddle, ball):
    if ball.centery > paddle.centery:
        paddle.y += paddle_speed
    elif ball.centery < paddle.centery:
        paddle.y -= paddle_speed

    if paddle.top < 0:
        paddle.top = 0
    if paddle.bottom > HEIGHT:
        paddle.bottom = HEIGHT

    return paddle


def check_ball_collision(ball, ball_speed_x, ball_speed_y, left_paddle, right_paddle, collision_count, score):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        collision_count += 1

        if collision_count % 3 == 0:
            ball_speed_x += 2 if ball_speed_x > 0 else -1  # Increase ball speed by 1 every 5 paddle hits
            ball_speed_y += 2 if ball_speed_y > 0 else -1  # Increase ball speed by 1 every 5 paddle hits

        # Increment the score if the right paddle hits the ball
        if ball.colliderect(right_paddle):
            score += 1
    elif ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1

    # Limit the ball speed
    ball_speed_x = min(max_ball_speed, max(ball_speed_x, -max_ball_speed))
    ball_speed_y = min(max_ball_speed, max(ball_speed_y, -max_ball_speed))

    return ball_speed_x, ball_speed_y, collision_count, score





def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    clock = pygame.time.Clock()

    collision_count = 0
    score = 0

    left_paddle = pygame.Rect(0, HEIGHT / 2 - paddle_height / 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(WIDTH - paddle_width, HEIGHT / 2 - paddle_height / 2, paddle_width, paddle_height)

    ball = pygame.Rect(WIDTH / 2 - ball_width / 2, HEIGHT / 2 - ball_height / 2, ball_width, ball_height)

    ball_speed_x = 3 * (-1 if random.random() < 0.5 else 1)
    ball_speed_y = 3 * (-1 if random.random() < 0.5 else 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        #WS functionality
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            right_paddle.y += paddle_speed

        #arrow key functionality
        if keys[pygame.K_UP]:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN]:
            right_paddle.y += paddle_speed


        if right_paddle.top < 0:
            right_paddle.top = 0
        if right_paddle.bottom > HEIGHT:
            right_paddle.bottom = HEIGHT

        left_paddle = ai_move(left_paddle, ball)

        ball_speed_x, ball_speed_y, collision_count, score = check_ball_collision(ball, ball_speed_x, ball_speed_y, left_paddle, right_paddle, collision_count, score)

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        draw_objects(screen, left_paddle, right_paddle, ball, score)

        pygame.display.flip()
        clock.tick(60)

        if ball.left <= 0 or ball.right >= WIDTH:
            game_result(screen, "You Win!" if ball.left <= 0 else "You Lose!", score)
            break






def start_menu(score):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    clock = pygame.time.Clock()

    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)

    while True:
        screen.fill(WHITE)

        text_surface = font.render("START", True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - 60, HEIGHT // 2 - 25))
        pygame.draw.rect(screen, BLACK, start_button, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

            # Check for Enter key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        pygame.display.flip()
        clock.tick(60)





def game_result(screen, message, score):
    clock = pygame.time.Clock()
    result_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)

    score_surface = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_surface, (WIDTH // 2 - 50, HEIGHT // 2 - 150))


    while True:
        screen.fill(WHITE)
        text_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - 70, HEIGHT // 2 - 75))
        
        # Display the score
        score_surface = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_surface, (WIDTH // 2 - 50, HEIGHT // 2 - 150))
        
        text_surface = font.render("MENU", True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - 60, HEIGHT // 2 - 25))
        pygame.draw.rect(screen, BLACK, result_button, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if result_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(60)





if __name__ == "__main__":
    score = 0
    while True:
        start_menu(score)
        score = main()


