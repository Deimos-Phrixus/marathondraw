import pygame
import pickle
from network import Network

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        if game.all_ready():
                pygame.time.delay(500)
                try:
                    game = n.send("reset")
                except:
                    run = False
                    print("Couldn't get game")
                    break
        command = input()
        try:
            game = n.send(command)
        except:
            run = False
            print("Couldn't get game")
            break

if __name__ == "__main__":
    main()
