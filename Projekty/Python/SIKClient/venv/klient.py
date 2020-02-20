#!/usr/bin/python

import time
import socket  # Import socket module
import pygame
import pygame_textinput

'''Game screens:
1 = title screen
2 = create server
3 = join server
4 = choose ship placement
5 = game screen
6 = endgame screen
'''
port = 2137



class placement(pygame.sprite.Sprite):
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('tile.png')
        self.rect = self.image.get_rect(topleft=(x,y))
        self.chosen = False


class mainFunctions:
    def __init__(self):
        #Global assets
        pygame.init()
        self.clock = pygame.time.Clock()
        self.mainloop = 1
        self.windowHeight = 768
        self.windowWidth = 1024
        self.gameScreen = 1
        self.background = pygame.image.load('background.jpg')
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.events = pygame.event.get()
        self.playerTurn = 'False'
        self.explosion = pygame.image.load('explosion.png')
        #Fonts

        self.titleFont = pygame.font.Font(None, 115)
        self.lowerTitleFont = pygame.font.Font(None, 70)
        self.counterFont = pygame.font.Font(None, 50)

        #Game data

        self.shipCount = 10
        self.enemyShips = 10
        self.ipAddress = 'null'
        self.fleetString = ''
        self.currentShot = ''

        #Enemy hit values
        self.enemyHit = False
        self.hitX = 1024
        self.hitY = 768
        self.hitX2 = 1024
        self.hitY2 = 768

        #Player hit values
        self.playerHit = False
        self.explosionCounter = 60
        self.explosionCounter2 = 60
        #Screen 1 assets

        self.titleText = self.titleFont.render("WarGames", True, (0, 0, 0))
        self.joinTitleText = self.lowerTitleFont.render("Join Game", True, (0, 0, 0))
        self.startTitleText = self.lowerTitleFont.render("Start Server", True, (0, 0, 0))

        #Screen 2 assets

        self.enterIPText = self.lowerTitleFont.render("Enter an IP Address", True, (0, 0, 0))
        self.textinput = pygame_textinput.TextInput()
        self.textinput.font_size = 70

        #Screen 3 assets

        self.troopPlacementText = self.lowerTitleFont.render("Place your units", True, (0, 0, 0))
        self.readyText = pygame.image.load('ready.png')
        self.a1=placement(130,30,'a1')
        self.a2=placement(203,30,'a2')
        self.a3=placement(276,30,'a3')
        self.a4=placement(349,30,'a4')
        self.a5=placement(422,30,'a5')
        self.a6=placement(495,30,'a6')
        self.a7=placement(568,30,'a7')
        self.a8=placement(641,30,'a8')
        self.a9=placement(714,30,'a9')
        self.a10=placement(787,30,'a0')
        self.b1=placement(130,103,'b1')
        self.b2=placement(203,103,'b2')
        self.b3=placement(276,103,'b3')
        self.b4=placement(349,103,'b4')
        self.b5=placement(422,103,'b5')
        self.b6=placement(495,103,'b6')
        self.b7=placement(568,103,'b7')
        self.b8=placement(641,103,'b8')
        self.b9=placement(714,103,'b9')
        self.b10=placement(787,103,'b0')
        self.c1=placement(130,176,'c1')
        self.c2=placement(203,176,'c2')
        self.c3=placement(276,176,'c3')
        self.c4=placement(349,176,'c4')
        self.c5=placement(422,176,'c5')
        self.c6=placement(495,176,'c6')
        self.c7=placement(568,176,'c7')
        self.c8=placement(641,176,'c8')
        self.c9=placement(714,176,'c9')
        self.c10=placement(787,176,'c0')
        self.d1=placement(130,249,'d1')
        self.d2=placement(203,249,'d2')
        self.d3=placement(276,249,'d3')
        self.d4=placement(349,249,'d4')
        self.d5=placement(422,249,'d5')
        self.d6=placement(495,249,'d6')
        self.d7=placement(568,249,'d7')
        self.d8=placement(641,249,'d8')
        self.d9=placement(714,249,'d9')
        self.d10=placement(787,249,'d0')
        self.e1=placement(130,322,'e1')
        self.e2=placement(203,322,'e2')
        self.e3=placement(276,322,'e3')
        self.e4=placement(349,322,'e4')
        self.e5=placement(422,322,'e5')
        self.e6=placement(495,322,'e6')
        self.e7=placement(568,322,'e7')
        self.e8=placement(641,322,'e8')
        self.e9=placement(714,322,'e9')
        self.e10=placement(787,322,'e0')
        self.f1=placement(130,395,'f1')
        self.f2=placement(203,395,'f2')
        self.f3=placement(276,395,'f3')
        self.f4=placement(349,395,'f4')
        self.f5=placement(422,395,'f5')
        self.f6=placement(495,395,'f6')
        self.f7=placement(568,395,'f7')
        self.f8=placement(641,395,'f8')
        self.f9=placement(714,395,'f9')
        self.f10=placement(787,395,'f0')
        self.g1=placement(130,468,'g1')
        self.g2=placement(203,468,'g2')
        self.g3=placement(276,468,'g3')
        self.g4=placement(349,468,'g4')
        self.g5=placement(422,468,'g5')
        self.g6=placement(495,468,'g6')
        self.g7=placement(568,468,'g7')
        self.g8=placement(641,468,'g8')
        self.g9=placement(714,468,'g9')
        self.g10=placement(787,468,'g0')
        self.h1=placement(130,541,'h1')
        self.h2=placement(203,541,'h2')
        self.h3=placement(276,541,'h3')
        self.h4=placement(349,541,'h4')
        self.h5=placement(422,541,'h5')
        self.h6=placement(495,541,'h6')
        self.h7=placement(568,541,'h7')
        self.h8=placement(641,541,'h8')
        self.h9=placement(714,541,'h9')
        self.h10=placement(787,541,'h0')
        self.i1=placement(130,614,'i1')
        self.i2=placement(203,614,'i2')
        self.i3=placement(276,614,'i3')
        self.i4=placement(349,614,'i4')
        self.i5=placement(422,614,'i5')
        self.i6=placement(495,614,'i6')
        self.i7=placement(568,614,'i7')
        self.i8=placement(641,614,'i8')
        self.i9=placement(714,614,'i9')
        self.i10=placement(787,614,'i0')
        self.j1=placement(130,687,'j1')
        self.j2=placement(203,687,'j2')
        self.j3=placement(276,687,'j3')
        self.j4=placement(349,687,'j4')
        self.j5=placement(422,687,'j5')
        self.j6=placement(495,687,'j6')
        self.j7=placement(568,687,'j7')
        self.j8=placement(641,687,'j8')
        self.j9=placement(714,687,'j9')
        self.j10 = placement(787,687,'j0')
        self.list = []
        self.list.append(self.a1)
        self.list.append(self.a2)
        self.list.append(self.a3)
        self.list.append(self.a4)
        self.list.append(self.a5)
        self.list.append(self.a6)
        self.list.append(self.a7)
        self.list.append(self.a8)
        self.list.append(self.a9)
        self.list.append(self.a10)
        self.list.append(self.b1)
        self.list.append(self.b2)
        self.list.append(self.b3)
        self.list.append(self.b4)
        self.list.append(self.b5)
        self.list.append(self.b6)
        self.list.append(self.b7)
        self.list.append(self.b8)
        self.list.append(self.b9)
        self.list.append(self.b10)
        self.list.append(self.c1)
        self.list.append(self.c2)
        self.list.append(self.c3)
        self.list.append(self.c4)
        self.list.append(self.c5)
        self.list.append(self.c6)
        self.list.append(self.c7)
        self.list.append(self.c8)
        self.list.append(self.c9)
        self.list.append(self.c10)
        self.list.append(self.d1)
        self.list.append(self.d2)
        self.list.append(self.d3)
        self.list.append(self.d4)
        self.list.append(self.d5)
        self.list.append(self.d6)
        self.list.append(self.d7)
        self.list.append(self.d8)
        self.list.append(self.d9)
        self.list.append(self.d10)
        self.list.append(self.e1)
        self.list.append(self.e2)
        self.list.append(self.e3)
        self.list.append(self.e4)
        self.list.append(self.e5)
        self.list.append(self.e6)
        self.list.append(self.e7)
        self.list.append(self.e8)
        self.list.append(self.e9)
        self.list.append(self.e10)
        self.list.append(self.f1)
        self.list.append(self.f2)
        self.list.append(self.f3)
        self.list.append(self.f4)
        self.list.append(self.f5)
        self.list.append(self.f6)
        self.list.append(self.f7)
        self.list.append(self.f8)
        self.list.append(self.f9)
        self.list.append(self.f10)
        self.list.append(self.g1)
        self.list.append(self.g2)
        self.list.append(self.g3)
        self.list.append(self.g4)
        self.list.append(self.g5)
        self.list.append(self.g6)
        self.list.append(self.g7)
        self.list.append(self.g8)
        self.list.append(self.g9)
        self.list.append(self.g10)
        self.list.append(self.h1)
        self.list.append(self.h2)
        self.list.append(self.h3)
        self.list.append(self.h4)
        self.list.append(self.h5)
        self.list.append(self.h6)
        self.list.append(self.h7)
        self.list.append(self.h8)
        self.list.append(self.h9)
        self.list.append(self.h10)
        self.list.append(self.i1)
        self.list.append(self.i2)
        self.list.append(self.i3)
        self.list.append(self.i4)
        self.list.append(self.i5)
        self.list.append(self.i6)
        self.list.append(self.i7)
        self.list.append(self.i8)
        self.list.append(self.i9)
        self.list.append(self.i10)
        self.list.append(self.j1)
        self.list.append(self.j2)
        self.list.append(self.j3)
        self.list.append(self.j4)
        self.list.append(self.j5)
        self.list.append(self.j6)
        self.list.append(self.j7)
        self.list.append(self.j8)
        self.list.append(self.j9)
        self.list.append(self.j10)

        self.a=self.counterFont.render("a",True,(0,0,0))
        self.b=self.counterFont.render("b",True,(0,0,0))
        self.c=self.counterFont.render("c",True,(0,0,0))
        self.d=self.counterFont.render("d",True,(0,0,0))
        self.e=self.counterFont.render("e",True,(0,0,0))
        self.f=self.counterFont.render("f",True,(0,0,0))
        self.g=self.counterFont.render("g",True,(0,0,0))
        self.h=self.counterFont.render("h",True,(0,0,0))
        self.i=self.counterFont.render("i",True,(0,0,0))
        self.j=self.counterFont.render("j",True,(0,0,0))
        self.one=self.counterFont.render("1",True,(0,0,0))
        self.two=self.counterFont.render("2",True,(0,0,0))
        self.three=self.counterFont.render("3",True,(0,0,0))
        self.four=self.counterFont.render("4",True,(0,0,0))
        self.five=self.counterFont.render("5",True,(0,0,0))
        self.six=self.counterFont.render("6",True,(0,0,0))
        self.seven=self.counterFont.render("7",True,(0,0,0))
        self.eight=self.counterFont.render("8",True,(0,0,0))
        self.nine=self.counterFont.render("9",True,(0,0,0))
        self.ten=self.counterFont.render("10",True,(0,0,0))

        #Screen 4 assets

        self.yourTurnText = self.lowerTitleFont.render("Your Turn", True, (0, 0, 0))
        self.enemyTurnText = self.lowerTitleFont.render("Enemy Turn", True, (0, 0, 0))
        self.enemyScoreText = self.counterFont.render("Enemy Turn", True, (0, 0, 0))
        self.enemyLabelText = self.counterFont.render("Enemy", True, (0, 0, 0))
        self.playerLabelText = self.counterFont.render("Player", True, (0, 0, 0))

    def ScreenRefresh(self):
        if self.gameScreen == 1:
            self.screen.fill((255,255,255))
            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.titleText,(310,150))
            self.screen.blit(self.joinTitleText, (390, 400))
            self.screen.blit(self.startTitleText, (375, 500))
            pygame.display.flip()
        elif self.gameScreen == 2:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.enterIPText,(310,150))
            self.screen.blit(self.textinput.get_surface(), (480,280))
            pygame.display.flip()
        elif self.gameScreen == 3:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.troopPlacementText, (290, 350))
            self.screen.blit(self.readyText,(903,200))
            for l in self.list:
                self.screen.blit(l.image,(l.x,l.y))
            self.screen.blit(self.a,(868,50))
            self.screen.blit(self.b, (868, 125))
            self.screen.blit(self.c, (868, 190))
            self.screen.blit(self.d, (868, 265))
            self.screen.blit(self.e, (868, 340))
            self.screen.blit(self.f, (868, 415))
            self.screen.blit(self.g, (868, 480))
            self.screen.blit(self.h, (868, 555))
            self.screen.blit(self.i, (868, 630))
            self.screen.blit(self.j, (868, 700))
            self.screen.blit(self.one, (150, -2))
            self.screen.blit(self.two, (225, -2))
            self.screen.blit(self.three, (300, -2))
            self.screen.blit(self.four, (370, -2))
            self.screen.blit(self.five, (445, -2))
            self.screen.blit(self.six, (525, -2))
            self.screen.blit(self.seven, (595, -2))
            self.screen.blit(self.eight, (670, -2))
            self.screen.blit(self.nine, (745, -2))
            self.screen.blit(self.ten, (800, -2))

            pygame.display.flip()
        elif self.gameScreen == 4:
            enemyShipText = self.counterFont.render(str(self.enemyShips), True, (0, 0, 0))
            playerShipText = self.counterFont.render(str(self.shipCount), True, (0, 0, 0))
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(enemyShipText,(940,150))
            self.screen.blit(playerShipText, (40, 150))
            self.screen.blit(self.playerLabelText,(10,100))
            self.screen.blit(self.enemyLabelText, (900, 100))
            self.screen.blit(self.a, (868, 50))
            self.screen.blit(self.b, (868, 125))
            self.screen.blit(self.c, (868, 190))
            self.screen.blit(self.d, (868, 265))
            self.screen.blit(self.e, (868, 340))
            self.screen.blit(self.f, (868, 415))
            self.screen.blit(self.g, (868, 480))
            self.screen.blit(self.h, (868, 555))
            self.screen.blit(self.i, (868, 630))
            self.screen.blit(self.j, (868, 700))
            self.screen.blit(self.one, (150, -2))
            self.screen.blit(self.two, (225, -2))
            self.screen.blit(self.three, (300, -2))
            self.screen.blit(self.four, (370, -2))
            self.screen.blit(self.five, (445, -2))
            self.screen.blit(self.six, (525, -2))
            self.screen.blit(self.seven, (595, -2))
            self.screen.blit(self.eight, (670, -2))
            self.screen.blit(self.nine, (745, -2))
            self.screen.blit(self.ten, (800, -2))
            for l in self.list:
                self.screen.blit(l.image, (l.x, l.y))
            if self.enemyHit:
                if(self.explosionCounter>0):
                    self.screen.blit(self.explosion, (self.hitX+10,self.hitY+10))
                elif self.explosionCounter == 0:
                    self.enemyHit = False
                    self.explosionCounter = 60
            if self.playerHit:
                if(self.explosionCounter2>0):
                    self.screen.blit(self.explosion, (self.hitX+10,self.hitY+10))
                elif self.explosionCounter2 == 0:
                    self.playerHit = False
                    self.explosionCounter2 = 60
            pygame.display.flip()
        else:
            pygame.display.flip()

    def EventHandler(self):
        self.events = pygame.event.get()
        if self.gameScreen == 1:
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.Shutdown()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 373 <= pygame.mouse.get_pos()[0] <= 653 and 376 <= pygame.mouse.get_pos()[1] <= 460:
                        self.gameScreen = 2
        elif self.gameScreen == 2:
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.Shutdown()
            if self.textinput.update(self.events):
                network.address = self.textinput.get_text()
                if network.Connect():
                    network.FirstPackage()
                    self.gameScreen = 3
                else:
                    self.Shutdown()

        elif self.gameScreen == 3:
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.Shutdown()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 910<= pos[0] <=983 and 209<= pos[1] <=292:
                        counter = 0
                        for l in self.list:
                            if l.chosen and counter <10:
                                self.fleetString = l.name
                                network.FleetSend(self.fleetString)
                                counter +=1
                                l.image = pygame.image.load('tile.png')
                        self.gameScreen = 4
                    for l in self.list:
                        if l.rect.collidepoint(pos):
                            if not l.chosen:
                                l.chosen = True
                                l.image = pygame.image.load('usedtile.png')
                            else:
                                l.chosen = False
                                l.image = pygame.image.load('tile.png')

        elif self.gameScreen == 4:
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.Shutdown()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for l in self.list:
                        if l.rect.collidepoint(pos):
                            network.MakeMove(l.name)
                            if self.enemyHit:
                                self.hitX = l.x
                                self.hitY = l.y
                            l.image = pygame.image.load('usedtile.png')





    def Shutdown(self):
        self.mainloop = 0

class Network:
    def __init__(self):
        self.response = 'st'
        self.address = 'null'
        self.port = port
        self.socket = socket.socket()
        self.player = 'null'
        self.turn = 0
        self.blockConnect = False
        self.response = ''
        self.answer = ''
    def Connect(self):
        if self.socket.connect_ex((self.address, self.port)) == 0:
            return True
        else:
            return False
    def FirstPackage(self):
        response = self.socket.recv(2)
        if response.decode() == "p1":
            self.player = 'p1'
            main.playerTurn = True
        else:
            self.player = 'p2'


    def FleetSend(self,string):
        package = string.encode()
        self.socket.sendall(package)
    def MakeMove(self,string):
        if self.player == 'p1' and self.turn == 0:
            temp = string.encode()
            self.socket.sendall(temp)
            # receive info on answer success
            self.response = self.socket.recv(2)
            self.response = self.response.decode()
            if (self.response == 'ok'):
                main.playerHit = True
                main.enemyShips -= 1
            elif (self.response == 'no'):
                print("Miss")
            #self.response = ''
            main.playerTurn = False
            self.turn += 1
        elif self.player == 'p2' and self.turn == 0:
            self.response = self.socket.recv(2)
            self.response = self.response.decode()
            if (self.response == 'ok'):
                main.shipCount -= 1
                main.enemyHit = True
            elif (self.response == 'no'):
                print("Miss")
            # input answer

            self.answer = string.encode()
            self.socket.sendall(self.answer)
            #
            # receive info on answer success
            self.response = self.socket.recv(2)
            self.response = self.response.decode()
            if (self.response == 'ok'):
                main.playerHit = True
                main.enemyShips -= 1
            elif (self.response == 'no'):
                print('Miss')
            self.response = ''
            self.turn += 1
            main.playerTurn = True
        else:
            main.playerTurn = False
            self.response = self.socket.recv(2)
            self.response = self.response.decode()
            if (self.response == 'ok'):
                main.shipCount -= 1
                main.enemyHit = True
            elif (self.response == 'no'):
                print("Miss")
            elif (self.response == 'w1'):
                if(self.player == 'p1'):
                    f = open('Winner.pdf', 'wb')
                    size = int.from_bytes(self.socket.recv(4), byteorder="big")
                    remaining_bytes = socket.ntohl(size)
                    print("Wielkość pliku =", remaining_bytes)

                    l = self.socket.recv(512)
                    while (l):
                        print("Receiving...")
                        f.write(l)
                        l = self.socket.recv(512)
                    exit(0)
                elif self.player == 'p2':
                    print("Lost")
                    exit(0)
            elif (self.response == 'w2'):
                if(self.player == 'p1'):
                    print("Lost")
                    exit(0)
                elif self.player == 'p2':
                    f = open('Winner.pdf', 'wb')
                    size = int.from_bytes(self.socket.recv(4), byteorder="big")
                    remaining_bytes = socket.ntohl(size)
                    print("Wielkość pliku =", remaining_bytes)

                    l = self.socket.recv(512)
                    while (l):
                        print("Receiving...")
                        f.write(l)
                        l = self.socket.recv(512)
                    exit(0)
            main.playerTurn = True
            # input answer
            self.answer = string.encode()
            self.socket.sendall(self.answer)
            #
            # receive info on answer success
            #
            self.response = self.socket.recv(2)
            self.response = self.response.decode()
            if (self.response == 'ok'):
                self.playerHit = True
                main.enemyShips -= 1
            elif (self.response == 'no'):
                print("Miss")
            elif (self.response == 'w1'):
                if (self.player == 'p1'):
                    f = open('Winner.pdf', 'wb')
                    size = int.from_bytes(self.socket.recv(4), byteorder="big")
                    remaining_bytes = socket.ntohl(size)
                    print("Wielkość pliku =", remaining_bytes)
                    l = self.socket.recv(512)
                    while (l):
                        print("Receiving...")
                        f.write(l)
                        l = self.socket.recv(512)
                    exit(0)
                elif self.player == 'p2':
                    print("Lost")
                    exit(0)
            elif (self.response == 'w2'):
                if (self.player == 'p1'):
                    print("Lost")
                    exit(0)
                elif self.player == 'p2':
                    f = open('Winner.pdf', 'wb')
                    size = int.from_bytes(self.socket.recv(4), byteorder="big")
                    remaining_bytes = socket.ntohl(size)
                    print("Wielkość pliku =", remaining_bytes)
                    l = self.socket.recv(512)
                    while (l):
                        print("Receiving...")
                        f.write(l)
                        l = self.socket.recv(512)
                    exit(0)




main = mainFunctions()
network = Network()

while(main.mainloop):
    main.EventHandler()
    main.ScreenRefresh()
    main.clock.tick(60)
