import numpy as np
from dataclasses import dataclass
from manim import *


@dataclass
class ChargeSource:
    charge: float
    position: np.array

def make_a_bunch_of_wires(which):
      listy_objs=[]
      if which in ['sense', 'Sense', 's', 'S', 'SENSE']:
            for i in range(-5,5):
                  if (i % 2) == 0: # this is even
                        sense_wire = Circle(radius=0.1).shift(2* LEFT, i*UP)
                  else: # this is odd
                        sense_wire = Circle(radius=0.1).shift(2.5* LEFT, i*UP)
                  sense_wire.set_fill(BLACK, opacity=1.0)
                  listy_objs.append(sense_wire)
      elif which in ['cathode', 'Cathode', 'c', 'C', 'CATHODE']:
            for i in range(-5,5):
                  cathode_wire = Circle(radius=0.1).shift(2 * RIGHT, i * UP)
                  cathode_wire.set_fill(BLUE, opacity=0.5)
                  listy_objs.append(cathode_wire)
      return listy_objs

class ElectricField:
    def __init__(self):
        self.charges = [
                ChargeSource(-2, np.array([2,0])),
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
    def __init__(self, label="", mass=1, color=RED, radius=0.2):
        super(Particle, self).__init__(radius=radius)
        self.set_fill(color, opacity=1)
        self.text = Text(label, font_size=24)
        self.add(self.text)
        self.v = np.zeros(2)
        self.mass = mass
        self.jitter_size = 0.2

    def add_field(self, field: ElectricField):
        self.field = field
        self.add_updater(self.update_position)

    def update_position(self, mobj, dt):
        # replace with if near wire...
        #if(mobj.get_x() < -10 or mobj.get_x() > 10 
                #or mobj.near_wire()):
            #mobj.v = np.zeros(2)
            #mobj.remove_updater(mobj.update_position) # this stops the updating if its near a wire...
        #else:
            jitter_probability = 0*dt
            if (np.random.uniform() < jitter_probability):
                jitter = self.jitter_size/self.mass*np.append(np.random.uniform(low=-1,size=2))
            else:
                jitter = np.zeros(2)

            a = 1/self.mass * self.field.field_at(self.get_center())
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


class EventParticle(Particle):
    def __init__(self):
        super(EventParticle, self).__init__(label="Be", color=BLUE)
        self.v = 5*DOWN
        self.shift(4*UP)


    def start(self):
        self.add_updater(self.update_position)

    def update_position(self, mobj, dt):
        # replace with if near wire...
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
      SenseWires=make_a_bunch_of_wires('Sense')
      CathodeWires=make_a_bunch_of_wires('Cathode')
      for wire in SenseWires: self.add(wire)
      for wire in CathodeWires: self.add(wire)
      self.wait()
      # run particle event
      be10 = EventParticle().set_z_index(3)
      self.electrons = []
      self.ions = []
      be10.add_updater(self.update_be)
      self.add(be10)
      self.wait(12)

    def update_be(self, mobj, dt):
      if(mobj.get_y() < -10):
            mobj.v = np.zeros(3)
            mobj.remove_updater(mobj.update_position)
      else:
            a = np.zeros(3)
            mobj.v = mobj.v + a*dt 
            mobj.shift(mobj.v * dt)
            p_particle = 5
            prob = p_particle * dt
            if (np.random.uniform() < prob):
                electron = Particle(label="-", color=RED, mass=-2, radius=0.1)
                electron.shift(mobj.get_center())
                electron.set_z_index(2)
                electron.add_field(self.e_field)
                self.electrons.append(electron)

                ion = Particle(label="+", color=PURPLE, mass=10)
                ion.shift(mobj.get_center())
                ion.set_z_index(1)
                ion.add_field(self.e_field)
                self.ions.append(ion)

                self.add(electron)
                self.add(ion)

