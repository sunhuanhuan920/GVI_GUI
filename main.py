from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pygame
import math


class LoadObjFile:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []

        file = open(filename)
        for line in file:
            if line[:2] == "v ":
                # Character start at position 0 add 1
                index1 = line.find(" ") + 1
                # substring searched after first index
                index2 = line.find(" ", index1 + 1)
                # substring searched after second index
                index3 = line.find(" ", index2 + 1)

                vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                self.vertices.append(vertex)
            elif line[0] == "f":
                string = line.replace("//", "/")
                i = string.find(" ") + 1
                face = []
                for item in range(string.count(" ")):
                    if string.find(" ", i) == -1:
                        face.append(string[i:-1])
                        break
                    face.append(string[i:string.find(" ", i)])
                    i = string.find(" ", i) + 1
                self.faces.append(tuple(face))
        file.close()

    def render_object(self):
        if len(self.faces) > 0:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for f in face:
                    vertexDraw = self.vertices[int(f) - 1]
                    glColor4f(0, 1, 0, 1)
                    glVertex3fv(vertexDraw)
            glEnd()


#a = LoadObjFile("castle.obj")
#print(a.vertices[0][0] * 2)

class Object:
    def __init__(self):
        self.angle = 0
        self.vertices = []
        self.faces = []
        self.coordinates = [0, 0, -65]
        self.shape = LoadObjFile("castle.obj")
        #self.shape = LoadObjFile("teapot.obj")
        self.position = [0, 0, -50]

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 0, math.sin(math.radians(self.angle)), 0, math.cos(math.radians(self.angle)) * -1, 0, 1, 0)
        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])


    def forward(self):
        self.coordinates[2] += 3 * math.cos(math.radians(self.angle))
        self.coordinates[0] -= 3 * math.sin(math.radians(self.angle))

    def back(self):
        self.coordinates[2] -= 3 * math.cos(math.radians(self.angle))
        self.coordinates[0] += 3 * math.sin(math.radians(self.angle))

    def up(self, n):
        self.coordinates[1] -= n

    def down(self, n):
        self.coordinates[1] += n

    def move_left(self, n):
        self.coordinates[0] += n * math.cos(math.radians(self.angle))
        self.coordinates[2] += n * math.sin(math.radians(self.angle))



def main():
    pygame.init()
    pygame.display.set_mode((1280, 1280), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("cube")
    clock = pygame.time.Clock()
    # Feature checker
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    #
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(800) / 600, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    objectcube = Object()

    done = False
    pressed_up = False
    pressed_down = False
    pressed_right = False
    pressed_left = False
    pressed_w = False
    pressed_s = False
    pressed_r = False
    angle = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:  # check for key presses
                if event.key == pygame.K_LEFT:  # left arrow turns left
                    pressed_left = True
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    pressed_right = True
                elif event.key == pygame.K_UP:  # up arrow goes up
                    pressed_up = True
                elif event.key == pygame.K_DOWN:  # down arrow goes down
                    pressed_down = True
                elif event.key == pygame.K_w:
                    pressed_w = True
                elif event.key == pygame.K_s:
                    pressed_s = True
                elif event.key == pygame.K_r:
                    pressed_r = True
            elif event.type == pygame.KEYUP:  # check for key releases
                if event.key == pygame.K_LEFT:  # left arrow turns left
                    pressed_left = False
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    pressed_right = False
                elif event.key == pygame.K_UP:  # up arrow goes up
                    pressed_up = False
                elif event.key == pygame.K_DOWN:  # down arrow goes down
                    pressed_down = False
                elif event.key == pygame.K_w:
                    pressed_w = False
                elif event.key == pygame.K_s:
                    pressed_s = False
                elif event.key == pygame.K_r:
                    pressed_r = False

        if pressed_up:
            objectcube.forward()
        if pressed_down:
            objectcube.back()
        if pressed_right:
            objectcube.angle += 10
        if pressed_left:
            objectcube.angle -= 10
        if pressed_w:
            objectcube.up(1)
        if pressed_s:
            objectcube.down(1)

        objectcube.render()
        objectcube.shape.render_object()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()