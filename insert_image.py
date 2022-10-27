from manim import *


def MakeWaveform():
      corona = ImageMobject("include/waveform.png")
      corona.scale(1)
      corona.shift(3.5*RIGHT, 2*UP)
      circle1 = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      circle1.shift(1*RIGHT, 0.6*UP)
      circle2 = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      circle2.shift(1*RIGHT, 3.3*UP)
      #line = Line(circle1.get_center(), circle2.get_center(), fill_opacity=0) # some red line
      #line.set_color(BLUE)
      return [corona,circle1,circle2]

class MovingWindow(Line):
      def __init__(self,circle1,circle2):
            super(MovingWindow, self).__init__(circle1.get_center(), circle2.get_center(),color=BLUE)
            self.v = 1*RIGHT
      def start(self):
            self.add_updater(self.update_position)
      def update_position(self, mobj, dt):
            # replace with near_wire
            if(mobj.get_x() > 5):
                  mobj.v = np.zeros(3)
                  mobj.remove_updater(mobj.update_position)
            else:
                  a = np.zeros(3)
                  mobj.v = mobj.v + a*dt 
                  mobj.shift(mobj.v * dt)

class Vid(Scene):
      def construct(self):
            self.camera.background_color = "#000000"
            waveform=MakeWaveform()
            for obj in waveform: self.add(obj)
            window = MovingWindow(waveform[1],waveform[2])
            window.add_updater(self.update_window)
            self.add(window)
            self.dts_propped=0
            TIME=12
            self.wait(TIME)
      def update_window(self, mobj, dt):
            self.dts_propped+=1
            if(mobj.get_x() > 6):
                  mobj.v = np.zeros(3)
                  mobj.remove_updater(mobj.update_position)
            elif(self.dts_propped>100):
                  a = np.zeros(3)
                  #print(a)
                  mobj.v = mobj.v + a*dt 
                  mobj.shift(mobj.v * dt)

