import pygame

def init():
    pygame.init()
    window = pygame.display.set_mode((400,400))

def getKey(key):
    pressed = False
    for event in pygame.event.get():
        pass
    KeyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(key))
    if KeyInput[myKey]:
        pressed = True
    pygame.display.update()

    return pressed

def main():
    if getKey("LEFT"):
        print("Left Key Pressed")
    if getKey("RIGHT"):
        print("Right key Pressed")

if __name__ == "__main__":
    init()
    while True:
        main()