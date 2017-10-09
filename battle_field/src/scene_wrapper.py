from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import (QTimer, QTime, qrand, QPointF, QRectF)

from personage import Personage
from obstacle import Obstacle


class SceneWrapper(QGraphicsScene):

    pers_count_maximum = 1
    obstackles_count_maximum = 50
    safety_objects_distance = 100

    def __init__(self, *xxx, **kwargs):
        QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        # create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / 30.0
        self.timer.start(self.dt * 1000)
        self.time = QTime()
        self.time.start()
        # self.addRect(QRectF(0, 0, 10, 10))

        # create obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + qrand() % 2000
            pos_y = -1000 + qrand() % 2000
            pos = QPointF(pos_x, pos_y)
            angle = 0
            self.addItem(Obstacle(self, pos, 0))

        # create personages objects (do not collide with obstackles!)
        # for i in range(self.pers_count_maximum):
            # pos_x = qrand() % 1000
            # pos_y = qrand() % 1000
            # pos = QPointF(pos_x, pos_y)
            # angle = qrand() % 360
            # self.addItem(Personage(self, pos, angle))

        # generate obstacles at battle_field
        pers_count_current = 0
        while (pers_count_current < self.pers_count_maximum):
            # generate random point
            pos_x = -1000 + qrand() % 2000
            pos_y = -1000 + qrand() % 2000
            pos = QPointF(pos_x, pos_y)
            angle = 0  # qrand() % 360
            # check that we don't collide with other tanks positions
            # and obstackles positions
            left_up_corner = QPointF(
                pos_x - self.safety_objects_distance,
                pos_y - self.safety_objects_distance)
            right_down_corner = QPointF(
                pos_x + self.safety_objects_distance,
                pos_y + self.safety_objects_distance)
            safety_rect = QRectF(left_up_corner, right_down_corner)
            permission_flag = True
            for item in self.items(safety_rect):
                if isinstance(item, Personage) or isinstance(item, Obstacle):
                    permission_flag = False
                    break
            if (permission_flag is True):
                self.addItem(Personage(self, pos, angle))
                pers_count_current += 1


    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        for item in self.items():
            item.update()
        if len(self.items()) < self.pers_count_maximum:
            pos_x = -1000 + qrand() % 2000
            pos_y = -1000 + qrand() % 2000
            pos = QPointF(pos_x, pos_y)
            angle = qrand() % 360
            self.addItem(Personage(self, pos, angle))
