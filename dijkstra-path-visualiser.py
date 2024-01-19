from tkinter import messagebox, Tk
import pygame
import sys
import queue
from button import Button

pygame.init()

window_width = 600
window_height = 600

window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption ("Shortest path finder using Dijkstra's Algorithm")

BG = pygame.image.load ("assets/Background.png")

def get_font (size) :
    return pygame.font.Font ("assets/font.ttf" , size)

def start():
    START_MOUSE_POS = pygame.mouse.get_pos()

    columns = 40
    rows = 40

    box_width = window_width // columns
    box_height = window_height // rows

    grid = []
    q = queue.Queue()
    path = []


    class Box:
        def __init__(self, i, j):
            self.x = i
            self.y = j
            self.start = False
            self.wall = False
            self.target = False
            self.queued = False
            self.visited = False
            self.neighbours = []
            self.prior = None

        def draw(self, win, color):
            pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

        def set_neighbours(self):
            if self.x > 0:
                self.neighbours.append(grid[self.x - 1][self.y])
            if self.x < columns - 1:
                self.neighbours.append(grid[self.x + 1][self.y])
            if self.y > 0:
                self.neighbours.append(grid[self.x][self.y - 1])
            if self.y < rows - 1:
                self.neighbours.append(grid[self.x][self.y + 1])


    # Draw the Grid
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)

    # Set Neighbours
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours()

    start_box = grid[0][0]
    start_box.start = True
    start_box.visited = True
    q.put(start_box)
    begin_search = False
    target_box_set = False
    searching = True  # interrupt searching once end point is reached
    target_box = None  # store the box we want to reach

    while True:
        pygame.time.delay (5)

        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Draw Wall
                if event.buttons[0]:   # left mouse button to make walls
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True

                # Set Target
                if event.buttons[2] and not target_box_set:   # right mouse button to set target
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True # target box is set

            # Start showing the Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if not q.empty() and searching:
                current_box = q.get(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            q.put(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution found", "There is no solution here !")
                    searching = False

        window.fill((0, 0, 0))
        
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                # Drawing the boxes in different colors
                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))
                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))


        pygame.display.flip()

def instructions() :
    while True:
        INSTRUCTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("white")

        INSTRUCTIONS_TEXT_1 = get_font(10).render("Left click on the mouse to draw the walls in the grid.", True, "Black")
        INSTRUCTIONS_TEXT_2 = get_font(10).render("Right click to set the target.", True, "Black")
        INSTRUCTIONS_TEXT_3 = get_font(10).render("Then press Enter to start the visualiser.", True, "Black")

        INSTRUCTIONS_RECT_1 = INSTRUCTIONS_TEXT_1.get_rect(center=(300, 150))
        INSTRUCTIONS_RECT_2 = INSTRUCTIONS_TEXT_2.get_rect(center=(300, 180))
        INSTRUCTIONS_RECT_3 = INSTRUCTIONS_TEXT_3.get_rect(center=(300, 210))

        window.blit(INSTRUCTIONS_TEXT_1, INSTRUCTIONS_RECT_1)
        window.blit(INSTRUCTIONS_TEXT_2, INSTRUCTIONS_RECT_2)
        window.blit(INSTRUCTIONS_TEXT_3, INSTRUCTIONS_RECT_3)

        INSTRUCTIONS_BACK = Button(image=None, pos=(300, 450), text_input="BACK", font=get_font(35), base_color="Black", hovering_color="Green")

        INSTRUCTIONS_BACK.changeColor(INSTRUCTIONS_MOUSE_POS)
        INSTRUCTIONS_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkForInput(INSTRUCTIONS_MOUSE_POS):
                    main()

        pygame.display.update()


def main() :
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 60))

        START_BUTTON = Button(image=pygame.image.load("assets/Start Rect.png"), pos=(300, 180), 
                            text_input="START", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        INSTRUCTIONS_BUTTON = Button(image=pygame.image.load("assets/Instructions Rect.png"), pos=(300, 320), 
                            text_input="INSTRUCTIONS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(300, 460), 
                            text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [START_BUTTON, INSTRUCTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start()
                if INSTRUCTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instructions()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main()
