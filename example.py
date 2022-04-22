from manim import *


class ElectricField:
    def __init__(self):
        self.field = 1
        pass
    def field_at(self, vector):
        # takes a 3 dimensional np array
        return self.field

class Particle(Circle):
    def __init__(self, label="", rig=1, color=RED):
        super(Particle, self).__init__(radius=0.2)
        self.set_fill(color, opacity=1)
        self.text = Text(label, font_size=24)
        self.add(self.text)
        self.v = 0
        self.rig = rig

    def add_field(self, field: ElectricField):
        self.field = field
        self.add_updater(self.update_position)

    def update_position(self, mobj, dt):
        # replace with if near wire...
        if(mobj.get_x() < -2 or mobj.get_x() > 2):
            a = 0
            mobj.v = 0
            mobj.remove_updater(mobj.update_position)
        else:
            a = self.rig * self.field.field_at(self.get_center())
            mobj.v = mobj.v + a*dt
            mobj.shift(RIGHT * mobj.v * dt)


class CreateCircle(Scene):
    def construct(self):
        e_field = ElectricField()
        # constuct detector
        sense_wire = Circle(radius=0.1).shift(2* LEFT)  # create a circle
        sense_wire.set_fill(BLACK, opacity=1.0)
        cathode_wire = Circle(radius=0.1).shift(2 * RIGHT)
        cathode_wire.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        self.add(sense_wire)
        self.add(cathode_wire)

        electron = Particle(label="-", color=RED, rig=-0.5)
        ion = Particle(label="+", color=PURPLE, rig=0.1)

        self.wait()

        electron.add_field(e_field)
        ion.add_field(e_field)
        self.add(electron)
        self.add(ion)

        self.wait(2)
        e_field.field = 10
        self.wait(10)
