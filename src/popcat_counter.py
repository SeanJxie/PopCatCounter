import pygame
import sys
import os
import random
import winsound
from tkinter import Tk

"""

A "pop cat" themed counter program.
- Sean Xie (26/12/2020)

"""


# When the exe is launched, data is unpacked under the location sys._MEIPASS. If needed, access this location for data.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # May not exist
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Window args
ROOT = Tk()
SCALE = 2
win = (ROOT.winfo_screenwidth() // SCALE, ROOT.winfo_screenheight() // SCALE)
CAPTION = "PopCat Counter"
FPS_CAP = 120

# Initialize video and sound system
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Image
cat_dimensions = [win[0] // 3, win[1] // 2]

IM_1 = resource_path("assets/popcat1.jpg")  # Set default image
IM_2 = resource_path("assets/popcat2.jpg")
ICON = pygame.image.load(resource_path("assets/popcat_icon.ico"))

cat = pygame.image.load(IM_1)  # Load with default dimensions
cat = pygame.transform.scale(cat, cat_dimensions)  # Scale cat image

# GUI
font_size = win[1] // 2
font_name = resource_path("assets/FreeSansBold.ttf")
font = pygame.font.Font(font_name, font_size)

# pygame window
MAIN_SURFACE = pygame.display.set_mode(win)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)

# Clock
clock = pygame.time.Clock()

# Main loop
if __name__ == '__main__':
    curr_img = IM_1
    curr_bg_col = (255, 255, 255)  # Set default background color
    count = 0

    fs = False

    while 1:
        # Exit on exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

            # Change current image, background and play sound depending on keypress event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Enable full screen if not already
                    pygame.display.quit()  # Exit current display mode

                    # Reset caption and icon
                    pygame.display.set_caption(CAPTION)
                    pygame.display.set_icon(ICON)

                    if not fs:
                        win = (ROOT.winfo_screenwidth(), ROOT.winfo_screenheight())  # Change window dimensions to size of monitor
                        MAIN_SURFACE = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Change display mode to full screen

                        font_size *= SCALE  # Scale font size
                        cat_dimensions[0] *= SCALE
                        cat_dimensions[1] *= SCALE

                    else:  # Do the opposite of the block above
                        win = (ROOT.winfo_screenwidth() // SCALE, ROOT.winfo_screenheight() // SCALE)
                        MAIN_SURFACE = pygame.display.set_mode(win)
                        pygame.display.set_caption(CAPTION)
                        pygame.display.set_icon(ICON)

                        font_size //= SCALE
                        cat_dimensions[0] //= SCALE
                        cat_dimensions[1] //= SCALE

                    fs = not fs  # Toggle full screen

                if event.key == pygame.K_SPACE:  # On space press, change bg col and image, play sound, and iterate counter
                    curr_img = IM_2
                    winsound.PlaySound(resource_path("assets/Pop-sound-effect.wav"),
                                       winsound.SND_ASYNC)  # without SND_ASYNC, program is blocked
                    curr_bg_col = [random.randint(0, 255) for _ in range(3)]
                    count += 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    curr_img = IM_1

        # Update sizes and images, render to window
        font = pygame.font.Font(font_name, font_size)
        cat = pygame.image.load(curr_img)
        cat = pygame.transform.scale(cat, cat_dimensions)

        txt_surface = font.render(str(count), True, (255 - curr_bg_col[0], 255 - curr_bg_col[1], 255 - curr_bg_col[2]))

        MAIN_SURFACE.fill(curr_bg_col)
        MAIN_SURFACE.blit(cat, (win[0] // 2 - cat_dimensions[0] // 2, win[1] // 2 - win[1] // 17))  # Very specific
        MAIN_SURFACE.blit(txt_surface, (0, -font_size // 4))

        pygame.display.update()
        clock.tick(FPS_CAP)
