PyJay is a python package made by Connor Layson. It is made to make game development easier in Pygame.

PyJay is a collection of tools that I have found that I need in my game development journey. Simple things like buttons, animations, save files, maps, hitboxes, etc. You are still doing
all the heavy lifting, but with PyJay, it is much easier. I remember constantly looking up the same things over and over again, so I stopped looking them up and made the PyJay engine!

Making maps and colliders is long, tedious, and annoying to make yourself, so PyJay will make it for you with just a few files. Interactable tiles? No problem!

Stop trying to reinvent the wheel every time you make a game and ```pip install pyJay``` today!

View the documentation at ```connorlayson.github.io/pyJay```

PyJay & Pygame template:
```
import pygame
import pyJay

pygame.init()
screen = pygame.display.set_mode((700,700))
clock = pygame.time.Clock()

exit_button = pyJay.button(350,350,'Exit Game')

while True:
	screen.fill((0,0,0))
	
	exit_button.display(screen)
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if exit_button.get_click(pygame.mouse.get_pos()):
				pygame.quit()
				sys.exit()
	
	pygame.display.flip()
	clock.tick(60)
```
This will add a simple "Exit Game" button to the screen.
