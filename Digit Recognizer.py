import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

BOUND = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PTH = "bestmodel.h5"
IMGSAVE = False
model = load_model(PTH)
LABELS = {0: "Zero",
          1: "One",
          2: "Two",
          3: "Three",
          4: "Four",
          5: "Five",
          6: "Six",
          7: "Seven",
          8: "Eight",
          9: "Nine"}
pygame.init()
FONT = pygame.font.Font(None, 18)
DS = pygame.display.set_mode((640, 480))
#WHILE_INT = DISPLAYSURF.mp_rgb(WHITE)
pygame.display.set_caption("Digit Board")

iswriting = False
num_xc = []
num_yc = []
imgcnt = 1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and iswriting:
            xc, yc = event.pos
            pygame.draw.circle(DS, WHITE, (xc, yc), 4, 0)
            num_xc.append(xc)
            num_yc.append(yc)
        if event.type == MOUSEBUTTONDOWN:
            iswriting = True
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            xc = sorted(num_xc)
            yc = sorted(num_yc)
            
            rect_min_x, rect_max_x = max(num_xc[0]-BOUND, 0), min(640, num_xc[-1]+BOUND)
            rect_min_y, rect_max_y = max(num_yc[0] - BOUND, 0), min(num_yc[-1] + BOUND, 480)

            num_xc = []
            num_yc = []
            img_arr = np.array(pygame.PixelArray(DS))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            if IMGSAVE:
                cv2.imwrite("image.png")
                imgcnt += 1
            if img_arr.size > 0:
                image = cv2.resize(img_arr, (28, 28))
                image = np.pad(image, (10, 10), 'constant', constant_values=0)
                image = cv2.resize(image, (28,28))/255
                label = str(LABELS[np.argmax(model.predict(image.reshape(1, 28, 28, 1)))])
                tS = FONT.render(label, True, RED, WHITE)
                tRO = tS.get_rect()
                tRO.left, tRO.bottom = rect_min_x, rect_max_y
                DS.blit(tS, tRO)
            if event.type == KEYDOWN and event.unicode == "n":
                DS.fill(BLACK)
                    
    pygame.display.update()