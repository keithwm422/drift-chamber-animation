import numpy as np
from dataclasses import dataclass
from manim import *


@dataclass
class ChargeSource:
    charge: float
    position: np.array

class ElectricField:
    def __init__(self):
        self.charges = [
                ChargeSource(-1, np.array([2,0,0])),
                ChargeSource(+1, np.array([-2,0,0]))
                ]
                # ChargeSource(-1, np.array([2,2,0])),
                # ChargeSource(+1, np.array([-2,2,0])),
                # ChargeSource(-1, np.array([2,-2,0])),
                # ChargeSource(+1, np.array([-2,-2,0])),

    def field_at(self, vector):
        # takes a 3 dimensional np array
        field = np.zeros(3)
        for charge in self.charges:
            distance = np.linalg.norm(charge.position - vector)
            field += charge.charge/distance**2 * (vector - charge.position)
        return field 


class Particle(Circle):
    def __init__(self, label="", mass=1, color=RED, radius=0.2):
        super(Particle, self).__init__(radius=radius)
        self.set_fill(color, opacity=1)
        self.text = Text(label, font_size=24)
        self.add(self.text)
        self.v = np.zeros(3)
        self.mass = mass
        self.jitter_size = 0.2

    def add_field(self, field: ElectricField):
        self.field = field
        self.add_updater(self.update_position)

    def update_position(self, mobj, dt):
        # replace with if near wire...
        if(mobj.get_x() < -10 or mobj.get_x() > 10):
            mobj.v = 0
            mobj.remove_updater(mobj.update_position)
        else:
            jitter_probability = 10*dt
            if (np.random.uniform() < jitter_probability):
                jitter = self.jitter_size/self.mass*np.append(np.random.uniform(low=-1,size=2), 0)
            else:
                jitter = np.zeros(3)

            a = 1/self.mass * self.field.field_at(self.get_center())
            mobj.v = mobj.v + a*dt + jitter
            mobj.shift(mobj.v * dt)


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
            mobj.v = 0
            mobj.remove_updater(mobj.update_position)
        else:
            a = np.zeros(3)
            mobj.v = mobj.v + a*dt 
            mobj.shift(mobj.v * dt)


class CreateCircle(Scene):
    def construct(self):
        e_field = ElectricField()
        # constuct detector
        sense_wire = Circle(radius=0.1).shift(2* LEFT)
        sense_wire.set_fill(BLACK, opacity=1.0)
        cathode_wire = Circle(radius=0.1).shift(2 * RIGHT)
        cathode_wire.set_fill(BLUE, opacity=0.5) 

        self.add(sense_wire)
        self.add(cathode_wire)

        num_electrons = 9
        electrons = []
        for i in range(num_electrons):
            electron = Particle(label="-", color=RED, mass=-2, radius=0.1)
            electron.shift((i-5)/3.0*UP)
            electron.add_field(e_field)
            electrons.append(electron)

        num_ions = 6
        ions = []
        for i in range(num_ions):
            ion = Particle(label="+", color=PURPLE, mass=10)
            ion.shift((i-3)/2.0*UP)
            ion.add_field(e_field)
            ions.append(ion)

        be10 = EventParticle()
        self.wait()

        be10.start()
        self.add(be10)
        self.wait(1)
        for electron in electrons:
            self.add(electron)
        for ion in ions:
            self.add(ion)

        self.wait(10)

