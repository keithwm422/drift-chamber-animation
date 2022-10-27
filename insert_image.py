from manim import *

class Waveform(Scene):
      def construct(self):
            self.camera.background_color = "#000000"
            corona= ImageMobject("include/waveform.png")
            corona.scale(1.2)
            corona.to_edge(RIGHT, buff=1)
            self.add(corona)


