import sys
import random
import os

from PyQt6.QtCore import (
    Qt,
    QTimer,
    QPoint,
    QRect
)

from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QFont,
    QRadialGradient
)

from PyQt6.QtWidgets import (
    QApplication,
    QWidget
)


class JarvisHUD(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("JARVIS HUD")

        self.setGeometry(200, 100, 1400, 900)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setStyleSheet(
            "background: transparent;"
        )

        # -----------------------------------
        # DRAGGING
        # -----------------------------------

        self.old_pos = None

        # -----------------------------------
        # CLOSE BUTTON
        # -----------------------------------

        self.close_button_rect = QRect(
            self.width() - 70,
            20,
            40,
            40
        )

        # -----------------------------------
        # STATUS
        # -----------------------------------

        self.voice_status = "Idle"

        self.system_info = [
            "Memory Active",
            "Vision Online",
            "Web Access Enabled"
        ]

        # -----------------------------------
        # ANIMATION
        # -----------------------------------

        self.rotation = 0

        self.inner_rotation = 0

        self.pulse = 0

        self.pulse_direction = 1

        self.audio_level = 0

        self.current_subtitle = (
            "Jarvis initialized."
        )

        self.current_mode = "ONLINE"

        self.subtitle_offset = 0

        # -----------------------------------
        # PARTICLES
        # -----------------------------------

        self.particles = []

        for _ in range(160):

            self.particles.append({
                "x": random.randint(0, 1400),
                "y": random.randint(0, 900),
                "size": random.randint(1, 4),
                "speed": random.uniform(0.2, 1.2)
            })

        # -----------------------------------
        # TIMER
        # -----------------------------------

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)

    # -----------------------------------
    # WINDOW BUTTONS
    # -----------------------------------

    def draw_window_buttons(self, painter):

        painter.setBrush(
            QColor(255, 70, 70, 200)
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            self.close_button_rect
        )

        painter.setPen(
            QColor(255, 255, 255)
        )

        font = QFont(
            "Consolas",
            16
        )

        painter.setFont(font)

        painter.drawText(
            self.close_button_rect,
            Qt.AlignmentFlag.AlignCenter,
            "×"
        )

    # -----------------------------------
    # WINDOW DRAGGING
    # -----------------------------------

    def mousePressEvent(self, event):

        if self.close_button_rect.contains(
            event.position().toPoint()
        ):

            os._exit(0)

        self.old_pos = (
            event.globalPosition().toPoint()
        )

    def mouseMoveEvent(self, event):

        if self.old_pos:

            delta = (
                event.globalPosition().toPoint()
                - self.old_pos
            )

            self.move(
                self.x() + delta.x(),
                self.y() + delta.y()
            )

            self.old_pos = (
                event.globalPosition().toPoint()
            )

    def mouseReleaseEvent(self, event):

        self.old_pos = None

    # -----------------------------------
    # ANIMATION LOOP
    # -----------------------------------

    def animate(self):

        self.rotation += 1.4

        self.inner_rotation -= 2.1

        self.pulse += (
            self.pulse_direction * 1.2
        )

        if self.pulse > 20:

            self.pulse_direction = -1

        if self.pulse < 0:

            self.pulse_direction = 1

        for particle in self.particles:

            particle["y"] += particle["speed"]

            if particle["y"] > self.height():

                particle["y"] = 0

                particle["x"] = random.randint(
                    0,
                    self.width()
                )

        self.update()

    # -----------------------------------
    # HUD STATE
    # -----------------------------------

    def set_mode(self, mode):

        self.current_mode = mode

        self.update()

    def set_audio_level(self, level):

        self.audio_level = level

        self.update()

    def set_subtitle(self, text):

        self.current_subtitle = text

        self.update()

    # -----------------------------------
    # MAIN DRAW
    # -----------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        self.draw_background(painter)

        self.draw_particles(painter)

        self.draw_hud_lines(painter)

        self.draw_glass_panels(painter)

        self.draw_radar(painter)

        self.draw_orb(painter)

        self.draw_window_buttons(painter)

        self.draw_text(painter)

    # -----------------------------------
    # BACKGROUND
    # -----------------------------------

    def draw_background(self, painter):

        gradient = QRadialGradient(
            self.width() // 2,
            self.height() // 2,
            900
        )

        gradient.setColorAt(
            0,
            QColor(0, 15, 40, 180)
        )

        gradient.setColorAt(
            1,
            QColor(0, 0, 0, 235)
        )

        painter.fillRect(
            self.rect(),
            gradient
        )

    # -----------------------------------
    # PARTICLES
    # -----------------------------------

    def draw_particles(self, painter):

        for particle in self.particles:

            glow = QColor(
                0,
                255,
                255,
                random.randint(40, 120)
            )

            painter.setPen(glow)

            painter.drawEllipse(
                int(particle["x"]),
                int(particle["y"]),
                particle["size"],
                particle["size"]
            )

    # -----------------------------------
    # HUD LINES
    # -----------------------------------

    def draw_hud_lines(self, painter):

        pen = QPen(
            QColor(0, 255, 255, 70)
        )

        pen.setWidth(2)

        painter.setPen(pen)

        margin = 40

        painter.drawRect(
            margin,
            margin,
            self.width() - margin * 2,
            self.height() - margin * 2
        )

    # -----------------------------------
    # GLASS PANELS
    # -----------------------------------

    def draw_glass_panel(
        self,
        painter,
        x,
        y,
        w,
        h,
        title
    ):

        panel_color = QColor(
            0,
            20,
            40,
            100
        )

        border_color = QColor(
            0,
            255,
            255,
            120
        )

        painter.setBrush(panel_color)

        pen = QPen(border_color)

        pen.setWidth(2)

        painter.setPen(pen)

        painter.drawRoundedRect(
            x,
            y,
            w,
            h,
            20,
            20
        )

        painter.setPen(
            QColor(0, 255, 255)
        )

        font = QFont(
            "Consolas",
            14
        )

        painter.setFont(font)

        painter.drawText(
            x + 15,
            y + 30,
            title
        )

        if title == "VOICE STATUS":

            info_font = QFont(
                "Consolas",
                12
            )

            painter.setFont(info_font)

            painter.drawText(
                x + 15,
                y + 70,
                f"State: {self.voice_status}"
            )

            painter.drawText(
                x + 15,
                y + 105,
                f"Mode: {self.current_mode}"
            )

        if title == "SYSTEM STATUS":

            info_font = QFont(
                "Consolas",
                11
            )

            painter.setFont(info_font)

            y_offset = 70

            for item in self.system_info:

                painter.drawText(
                    x + 15,
                    y + y_offset,
                    f"• {item}"
                )

                y_offset += 30

    def draw_glass_panels(self, painter):

        self.draw_glass_panel(
            painter,
            60,
            180,
            260,
            180,
            "VOICE STATUS"
        )

        self.draw_glass_panel(
            painter,
            self.width() - 320,
            180,
            260,
            220,
            "SYSTEM STATUS"
        )

        self.draw_glass_panel(
            painter,
            self.width() - 320,
            450,
            260,
            220,
            "RADAR"
        )

    # -----------------------------------
    # RADAR
    # -----------------------------------

    def draw_radar(self, painter):

        x = self.width() - 190

        y = 560

        radius = 90

        painter.save()

        painter.translate(x, y)

        pen = QPen(
            QColor(0, 255, 255, 120)
        )

        pen.setWidth(2)

        painter.setPen(pen)

        for r in [20, 40, 60, 90]:

            painter.drawEllipse(
                -r,
                -r,
                r * 2,
                r * 2
            )

        painter.rotate(self.rotation * 2)

        scan_pen = QPen(
            QColor(0, 255, 255, 220)
        )

        scan_pen.setWidth(3)

        painter.setPen(scan_pen)

        painter.drawLine(
            0,
            0,
            radius,
            0
        )

        painter.restore()

    # -----------------------------------
    # ORB
    # -----------------------------------

    def draw_orb(self, painter):

        center_x = self.width() // 2

        center_y = self.height() // 2

        painter.save()

        painter.translate(
            center_x,
            center_y
        )

        painter.rotate(self.rotation)

        pen = QPen(
            QColor(0, 255, 255, 140)
        )

        pen.setWidth(3)

        painter.setPen(pen)

        for radius in [220, 180]:

            for angle in range(0, 360, 30):

                painter.drawArc(
                    -radius,
                    -radius,
                    radius * 2,
                    radius * 2,
                    int((angle + self.rotation) * 16),
                    int(18 * 16)
                )

        painter.restore()

        glow_size = (
            180
            + self.pulse
            + self.audio_level
        )

        gradient = QRadialGradient(
            center_x,
            center_y,
            glow_size
        )

        gradient.setColorAt(
            0,
            QColor(0, 255, 255, 255)
        )

        gradient.setColorAt(
            0.4,
            QColor(0, 180, 255, 180)
        )

        gradient.setColorAt(
            1,
            QColor(0, 255, 255, 0)
        )

        painter.setBrush(gradient)

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            int(center_x - glow_size),
            int(center_y - glow_size),
            int(glow_size * 2),
            int(glow_size * 2)
        )

        core_gradient = QRadialGradient(
            center_x,
            center_y,
            80
        )

        core_gradient.setColorAt(
            0,
            QColor(255, 255, 255)
        )

        core_gradient.setColorAt(
            1,
            QColor(0, 255, 255)
        )

        painter.setBrush(core_gradient)

        painter.drawEllipse(
            int(center_x - 70),
            int(center_y - 70),
            140,
            140
        )

    # -----------------------------------
    # TEXT
    # -----------------------------------

    def draw_text(self, painter):

        title_font = QFont(
            "Orbitron",
            42
        )

        painter.setFont(title_font)

        painter.setPen(
            QColor(0, 100, 255, 80)
        )

        painter.drawText(
            3,
            103,
            self.width(),
            60,
            Qt.AlignmentFlag.AlignCenter,
            "J.A.R.V.I.S"
        )

        painter.setPen(
            QColor(180, 255, 255)
        )

        painter.drawText(
            0,
            100,
            self.width(),
            60,
            Qt.AlignmentFlag.AlignCenter,
            "J.A.R.V.I.S"
        )

        status_font = QFont(
            "Consolas",
            18
        )

        painter.setFont(status_font)

        painter.drawText(
            0,
            self.height() - 240,
            self.width(),
            40,
            Qt.AlignmentFlag.AlignCenter,
            self.current_mode
        )

        subtitle_font = QFont(
            "Consolas",
            18
        )

        painter.setFont(subtitle_font)

        subtitle_rect_x = 140

        subtitle_rect_y = self.height() - 180

        subtitle_rect_width = self.width() - 280

        subtitle_rect_height = 100

        painter.setPen(
            QColor(0, 180, 255, 80)
        )

        painter.drawText(
            subtitle_rect_x + 2,
            subtitle_rect_y + 2,
            subtitle_rect_width,
            subtitle_rect_height,
            Qt.AlignmentFlag.AlignCenter
            | Qt.TextFlag.TextWordWrap,
            self.current_subtitle
        )

        painter.setPen(
            QColor(180, 255, 255)
        )

        painter.drawText(
            subtitle_rect_x,
            subtitle_rect_y,
            subtitle_rect_width,
            subtitle_rect_height,
            Qt.AlignmentFlag.AlignCenter
            | Qt.TextFlag.TextWordWrap,
            self.current_subtitle
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = JarvisHUD()

    window.show()

    sys.exit(app.exec())