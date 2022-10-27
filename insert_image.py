from manim import *


def MakeWaveform():
      corona = ImageMobject("include/waveform.png")
      corona.scale(1.2)
      corona.shift(2*RIGHT, 2*UP)
      circle = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      return [corona,circle]

class Vid(Scene):
      def construct(self):
            self.camera.background_color = "#000000"
            waveform=MakeWaveform()
            for obj in waveform: self.add(obj)

