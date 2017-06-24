"""
Name: huntsim-legacy.py 
Authors: Oliver Giles & Max Potter
Date: June 2017
Description:
    - Contains code that could be used to patch together a version of huntsim with a controllable tiger
    - Does not contain stuff like map generation
    - To be functional, would need to replace current definition of creature class and the main game loop
"""


tiger1, tigersprites = c.spawn_creature("tiger", pos=[150,100])

#Detect collisions between each tiger and all the deer on the map. If there is a collision, kill the deer.
    for tiger in c.tigerList:
        collision_list = pygame.sprite.spritecollide(tiger, c.deerList, True)
        for col in collision_list:
            tiger.eat(tigerEatEnergy)

    #Gather all living sprites into one list
    cList = c.tigerList.sprites() + c.deerList.sprites()

    #Update creature vision
    for creature in cList:
        i, j = mf.find_tile(creature, tileSize, height, width)
        creature.vision = mf.get_vision(i, j, tilemap, height, width)
        creature.vision[2][2] = tilemapMaster[i][j] #stop the tiger seeing itself in the centre square
        # if creature.ctype == "tiger":
        #     print '\n'
        #     print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in creature.vision]))
     
    #Handle input events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        tiger1.speed = tiger1.topSpeed
    else:
        tiger1.speed = tiger1.baseSpeed
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_w:
                tiger1.dy -= 1
            if event.key == K_a:
                tiger1.dx -= 1
            if event.key == K_s:
                tiger1.dy += 1
            if event.key == K_d:
                tiger1.dx += 1
        elif event.type == KEYUP:
            if event.key == K_w or event.key == K_s:
                tiger1.dy = 0
            if event.key == K_a or event.key == K_d:
                tiger1.dx = 0

    #Update display
    #Blit all living sprites on top of the background
    for creature in cList:
        creature.rect.clamp_ip(displayRect)
    #update background to cover up dead (unupdated) sprites
    display.blit(bgSurface,(0,0))
    for creature in cList:
        display.blit(bgSurface, creature.rect, creature.rect)  
    c.deerList.update()
    c.tigerList.update()
    # - draw all living sprites to the screen
    c.deerList.draw(display)
    c.tigerList.draw(display)
    pygame.display.update()

    #Update tilemap with positions of all creatures
    tigerPoints = []
    deerPoints = []
    for creature in cList:
        #what tile is the creature on?
        i, j = mf.find_tile(creature, tileSize, height, width)

        #Update tilemap to reflect what creatures are on each tiles - tigers trump deer
        if creature.ctype == "tiger" and tilemapMaster != wood: #tigers are invisible in the forest
            tigerPoints.append([i,j])
            tilemap[i][j] = 4
        elif creature.ctype == "deer" and tilemap[i][j] != tiger: 
            tilemap[i][j] = 3
            deerPoints.append([i,j])
            if tilemapMaster[i][j] == grass: #don't forget to feed the deer!
                creature.eat(deerEatEnergy)

    #Gather list of empty tiles by comparing old and new lists, then replace the tiles with their original types.
    emptyTiles = [point for point in oldTigerPoints if point not in tigerPoints]
    emptyTiles.extend([point for point in oldDeerPoints if point not in deerPoints])
    for tile in emptyTiles:
        tilemap[tile[0]][tile[1]] = tilemapMaster[tile[0]][tile[1]]

    oldDeerPoints = deerPoints
    oldTigerPoints = tigerPoints


class Creature(pygame.sprite.Sprite):
    """
    Generic creature class.
    Tigers hunt deer, deer eat grass. 
    All creatures lose energy over time and die it if hits zero.
    Handles sprite initialisation and movement.
    """

    def __init__(self, position, ctype, DNA = ''):
        pygame.sprite.Sprite.__init__(self)
        self.ctype = ctype
        self.name = self.get_name()

        #Handle creature type senstive parameters
        if ctype == 'tiger':
            self.image, self.rect = load_png('tiger.png')
            self.add(tigerList)
            self.baseSpeed = 2
            self.topSpeed = 10
            self.energy = 1500
            self.drainRate = 1
        elif ctype == 'deer':
            self.image, self.rect = load_png('deer.png')
            self.add(deerList)
            self.baseSpeed = 2
            self.topSpeed = 3
            self.energy = 1000
            self.drainRate = 2

        #Set up display information
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()  
        self.rect = self.image.get_rect(topleft=(position[0], position[1]))
        
        #Movement
        self.speed = self.baseSpeed
        self.dx = 0
        self.dy = 0

        #Set up default vision (5x5 grid, all seeing 'off map')
        self.vision = [[-1 for column in range(5)] for row in range(5)]

    def update(self):
        #Deplete energy and check if still alive!
        self.energy -= self.drainRate
        if self.energy <= 0:
            if self.ctype == 'tiger':
                tigerList.remove(self)
            if self.ctype == 'deer':
                deerList.remove(self)

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        pygame.event.pump()

    def get_name(self):
        return choice(list(open('names.txt')))

    def eat(self, eatEnergy):
        self.energy += eatEnergy
