import numpy as np
from dataclasses import dataclass
from manim import *


@dataclass
class ChargeSource:
      charge: float
      position: np.array

def MakeWaveform():
      wave = ImageMobject("include/waveform.png")
      wave.scale(1)
      wave.shift(3.5*RIGHT, 2*UP)
      circle1 = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      circle1.shift(1*RIGHT, 0.5*UP)
      circle2 = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      circle2.shift(1*RIGHT, 3.4*UP)
      #line = Line(circle1.get_center(), circle2.get_center(), fill_opacity=0) # some red line
      #line.set_color(BLUE)
      return [wave,circle1,circle2]
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
def MakeFieldDrawing():
      arrow = Arrow([-4,3,0], [-2, 3, 0], buff=0)
      drift_text = Text('Electric/Drift Field',font_size=20).next_to(arrow, DOWN)
      circ = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      circ.shift(5*LEFT,0*UP,0)
      circ2 = Circle(color="#87c2a5", fill_opacity=0.1, radius=0.1)
      circ2.shift(5*LEFT,-3*UP,0)
      line = Line(circ.get_center(), circ2.get_center()).set_color(WHITE)
      b1 = Brace(line,direction=line.copy().rotate(-PI/2).get_unit_vector()).set_color(WHITE)
      b1text = b1.get_text("0 V")
      sense_text = Text('Sense wires',font_size=16).next_to(circ, LEFT)
      circ.shift(10*RIGHT,0*UP,0)
      circ2.shift(10*RIGHT,0*UP,0)
      line2 = Line(circ.get_center(), circ2.get_center()).set_color(WHITE)
      b2 = Brace(line2,direction=line2.copy().rotate(PI/2).get_unit_vector()).set_color(WHITE)
      b2text = b2.get_text("-10 kV")
      cathode_text = Text('Cathode wires',font_size=16).next_to(circ, RIGHT)
      return [arrow,drift_text,sense_text,cathode_text,b1,b2,b1text,b2text]
def make_a_bunch_of_wires(which):
      listy_objs=[]
      if which in ['sense', 'Sense', 's', 'S', 'SENSE']:
            for i in range(-3,1):
                  if (i % 2) == 0: # this is even
                        sense_wire = Circle(radius=0.1).shift(4* LEFT, i*UP)
                  else: # this is odd
                        sense_wire = Circle(radius=0.1).shift(4.5* LEFT, i*UP)
                  sense_wire.set_fill(BLACK, opacity=1.0)
                  listy_objs.append(sense_wire)
      elif which in ['cathode', 'Cathode', 'c', 'C', 'CATHODE']:
            for i in range(-5,3):
                  cathode_wire = Circle(radius=0.1).shift(4 * RIGHT, i * UP)
                  cathode_wire.set_fill(BLUE, opacity=0.5)
                  listy_objs.append(cathode_wire)
      return listy_objs

# need the electric field to change to a drift field, constant velocity essentially, because of the gas
# looking at Sauli CERN 1977, drift velocity of electrons! is on the order of 12cm/usec -> Sauli figure 29 shows mixture
# Argon - CO2. I extrapolate from the 0.6 x axis data point to the HELIX drift field (10000V/(3inches*2.54cm/in)) and divide by 760 mmHG to get to 1.73
# which is 2.88 times 0.6 x axis point, so assume linear extrap and get 4*2.88 which is 11.5cm/us 
# for ions its more about mobility: u^{+}=w^{+}/E, for CO2 roughly u^{+}= 1.09 cm^2/(Volt sec)
# so w^{+}=u^{+} * E where E=10000/(3*2.54)=1312 V/cm as above
# w^{+}=1430 cm/sec = 1.43cm/millisecond. 
# 
class ElectricField:
      def __init__(self):
            self.charges = [
                  ChargeSource(-2, np.array([2,0])), # this is charge, then x y position. So its at the x axis +2 and -2
                  ChargeSource(+2, np.array([-2,0]))]
                  #ChargeSource(-1, np.array([2,2,0])),
                  #ChargeSource(+1, np.array([-2,2,0])),
                  #ChargeSource(-1, np.array([2,-2,0])),
                  #ChargeSource(+1, np.array([-2,-2,0]))
                  #]
      def field_at(self, vector):
            # takes a 3 dimensional np array
            field = np.zeros(2)
            for charge in self.charges:
                  distance = np.linalg.norm(charge.position - vector[:2])
                  # 1/r^1 because these are wires, not points
                  field += charge.charge/distance**2 * (vector[:2] - charge.position)
            return field 


class Particle(Circle):
      def __init__(self, label="", mass=1, color=RED, radius=0.2,charge=-1):
            super(Particle, self).__init__(radius=radius)
            self.set_fill(color, opacity=1)
            self.text = Text(label, font_size=24)
            self.add(self.text)
            self.v = np.zeros(2)
            self.mass = mass
            self.jitter_size = 0.2
            self.iter=0
            self.charge=charge
      def add_efield(self, efield: ElectricField):
            self.efield = efield
            self.add_updater(self.electric_update_position)
      def electric_update_position(self, mobj, dt):
            # replace with if near wire...
            #if(mobj.get_x() < -10 or mobj.get_x() > 10 
                #or mobj.near_wire()):
            #mobj.v = np.zeros(2)
            #mobj.remove_updater(mobj.update_position) # this stops the updating if its near a wire...
            #else:
            jitter_probability = 0*dt
            if (np.random.uniform() < jitter_probability):
                  jitter = self.charge*self.jitter_size/self.mass*np.append(np.random.uniform(low=-1,size=2))
                  self.iter = self.iter+1
            else:
                  jitter = np.zeros(2)
            a = 1/self.mass * self.efield.field_at(self.get_center()) * self.charge
            mobj.v = mobj.v + a*dt + jitter
            mobj.shift(np.append(mobj.v * dt,0))
      def near_wire(self):
            thresh = 0.2
            for x, y in [(-2,0), (2,0)]:
                  dx = np.abs(self.get_x() - x)
                  dy = np.abs(self.get_y() - y)
                  if (dx < thresh and dy < thresh):
                        return True
            return False
      def add_drift_velocity(self):
            self.add_updater(self.drift_update_position)
      def drift_update_position(self, mobj, dt):
            a = np.zeros(2)
            drift_ve=-2 # for electrons
            drift_vi=0.5 # for ions
            if(self.charge==-1):
                  mobj.v = np.array([drift_ve,0], np.float64) + a*dt
            elif(self.charge==+1):
                  mobj.v = np.array([drift_vi,0], np.float64) + a*dt 
            mobj.shift(np.append(mobj.v * dt,0))
class EventParticle(Particle):
      def __init__(self):
            super(EventParticle, self).__init__(label="Be", color=BLUE)
            self.v = 5*DOWN
            self.shift(4*UP)
      def start(self):
            self.add_updater(self.update_position)
      def update_position(self, mobj, dt):
            # replace with near_wire
            if(mobj.get_y() < -5):
                  mobj.v = np.zeros(3)
                  mobj.remove_updater(mobj.update_position)
            else:
                  a = np.zeros(3)
                  mobj.v = mobj.v + a*dt 
                  mobj.shift(mobj.v * dt)

class CreateVideo(Scene):
      def construct(self):
            self.e_field = ElectricField()
            # constuct detector
            arrows=MakeFieldDrawing()
            for obj in arrows: self.add(obj)
            SenseWires=make_a_bunch_of_wires('Sense')
            CathodeWires=make_a_bunch_of_wires('Cathode')
            for wire in SenseWires: self.add(wire)
            for wire in CathodeWires: self.add(wire)
            waveform=MakeWaveform()
            for obj in waveform: self.add(obj)
            window = MovingWindow(waveform[1],waveform[2])
            window.add_updater(self.update_window)
            self.dts_propped_window=0
            self.add(window)
            self.wait()
            # run cosmic ray particle event
            be10 = EventParticle().set_z_index(3)
            self.electrons = []
            self.ions = []
            self.dts_propped=0
            be10.add_updater(self.update_be)
            self.add(be10)
            TIME=12
            self.wait(TIME)
      def update_be(self, mobj, dt):
            # this code should execute at each dt, and since we give the Be-10 nucleus a velocity, no acceleration, and the same starting point
            # the waiting (self.wait(12)) determines the length to propagate time to, and hence decides the length of the video, abrubptly ending the video early it seems. 
            # so this dt is sort of always the same, and we should just decide, if total time is T and dt is always the same, then number of ions made is about a random sampling
            # in the region the Be-10 propagates. If we want 1/3 of the dt's to result in ion pair, then we do every 3 dts maybe?
            #print(mobj.get_center()[:2])
            if(mobj.get_y() < -4):
                  mobj.v = np.zeros(3)
                  mobj.remove_updater(mobj.update_position)
            #elif (mobj.get_y() <=4 and mobj.get_y()>=3):
            else:
                  self.dts_propped+=1
                  a = np.zeros(3)
                  #print(a)
                  mobj.v = mobj.v + a*dt 
                  mobj.shift(mobj.v * dt)
                  p_particle = 5
                  prob = p_particle * dt
                  # can we get a maximum 5 electrons or some shit?
                  sample=[]
                  #for i in range (0,1): 
                  #if(self.dts_propped % 4 == 0):
                  #if((mobj.get_y() <= 2.1 and mobj.get_y() >= 1.9) or mobj.get_y() == 1 or mobj.get_y() == 0 or mobj.get_y() == -1 or mobj.get_y() == -2 or mobj.get_y() == -3):
                  if((mobj.get_y() <= 0.1 and mobj.get_y() >= -0.1) or (mobj.get_y() <= -0.9 and mobj.get_y() >= -1.1) or (mobj.get_y() <= -1.9 and mobj.get_y() >= -2.1) or (mobj.get_y() <= -2.9 and mobj.get_y() >= -3.1)):
                        sample.append(self.dts_propped)
                        print(sample)
                  #if (sample < prob):
                  #if (iter % 2 == 0):
                        electron = Particle(label="-", color=RED, mass=2, radius=0.1,charge=-1)
                        electron.shift(mobj.get_center())
                        electron.set_z_index(2)
                        electron.add_drift_velocity()
                        #electron.add_efield(self.e_field)
                        self.electrons.append(electron)
                        ion = Particle(label="+", color=PURPLE, mass=10,charge=+1)
                        ion.shift(mobj.get_center())
                        ion.set_z_index(1)
                        #ion.add_efield(self.e_field)
                        ion.add_drift_velocity()
                        self.ions.append(ion)
                        self.add(electron)
                        self.add(ion)
      def update_window(self, mobj, dt):
            if(mobj.get_x() > 6):
                  mobj.v = np.zeros(3)
                  mobj.remove_updater(mobj.update_position)
            else:
                  self.dts_propped_window+=1
                  if(self.dts_propped_window>30):
                        a = np.zeros(3)
                        #print(a)
                        mobj.v = mobj.v + a*dt 
                        mobj.shift(mobj.v * dt)
