import glob
from typing import Union, Tuple

from manimlib.imports import *

ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets/")


class TimelineScene(Scene):
    _timeline_dt = None

    def get_next_dt(self):
        if self._timeline_dt is None:
            if hasattr(self, "timeline"):
                tl = [0, *self.timeline]
                self._timeline_dt = (t for t in map(lambda t: t[1] - t[0], zip(tl[:-1], tl[1:])))
        return next(self._timeline_dt)


class VerticalScene(TimelineScene):
    CONFIG = {
        "camera_config": {
            "frame_height": 6.0 * 21 / 9,
            "frame_width": 6.0,
        }
    }


class DebugScene(Scene):
    CONFIG = {
        "camera_config": {
            "frame_height": 4 * 6.0 * 21 / 9,
            "frame_width": 4 * 6.0,
        }
    }

    def construct(self):
        self.add(Rectangle(height=6.0 * 21 / 9, width=6.0))


class Galaxy(ImageMobject):
    list = glob.glob(os.path.join(ASSETS_FOLDER, "./images/galaxies/*"))

    def __init__(self,
                 scale: Union[float, Tuple[float, float]] = (0.01, 0.6),
                 rotation: Union[float, Tuple[float, float]] = (0, 360.0),
                 position: Union[np.array, Tuple[Tuple[float, float], Tuple[float, float]]] = ((-4, 4), (-8, 8))
                 ) -> None:
        super(Galaxy, self).__init__(os.path.join(ASSETS_FOLDER, random.choice(Galaxy.list)))

        self.scale(random.uniform(scale[0], scale[1]) if isinstance(scale, tuple) else scale)
        self.rotate(random.uniform(rotation[0], rotation[1]) if isinstance(rotation, tuple) else rotation)
        self.move_to([
                         random.uniform(position[0][0], position[0][1]),
                         random.uniform(position[1][0], position[1][1]),
                         0] if isinstance(rotation, tuple) else position)

    def go_away(self, dist: float, respect_from: np.array = np.array([0, 0, 0])) -> None:
        self.shift(normalize(self.get_center() - respect_from) * dist)


class DarkEnergy(VerticalScene):
    def construct(self):
        text = TextMobject("Energia oscura")

        galaxies = Group(*[Galaxy() for _ in range(100)])

        self.play(FadeIn(galaxies))
        self.wait(1)

        self.play(
            Write(text),
            *[v(g) for g in galaxies for v in (lambda g: g.go_away, lambda g: random.uniform(8, 40))],
            run_time=3, rate_func=lambda t: pow(t, 2)
        )

        self.play(Transform(text, TextMobject("Deus Ex Machina")))
        self.wait(1)

        red_cross = Cross(text)

        self.play(ShowCreation(red_cross))
        self.wait(1)

        self.play(FadeOut(text), FadeOut(red_cross))
        self.wait()


class Expansion(VerticalScene):
    CONFIG = {
        "timeline": [1.0, 3.0, 6.0]
    }

    def construct(self):
        galaxies = Group(*[Galaxy() for _ in range(100)])

        self.play(
            FadeIn(galaxies),
            run_time=self.get_next_dt()
        )

        self.wait(self.get_next_dt())

        self.play(
            *[v(g) for g in galaxies for v in (lambda g: g.go_away, lambda g: random.uniform(8, 40))],
            run_time=self.get_next_dt(), rate_func=lambda t: pow(t, 2)
        )


class DeRhamAndPaoli(VerticalScene):
    def construct(self):
        de_rham_photo = ImageMobject(os.path.join(ASSETS_FOLDER, "./images/de_rham.jpg"))
        de_rham_photo.move_to(UP * 1.4 + LEFT * 0.8)
        de_rham_text = TextMobject("De Rham Claudia")
        de_rham_text.move_to(UP * 3 + LEFT * 0.8)

        paoli_photo = ImageMobject(os.path.join(ASSETS_FOLDER, "./images/paoli.jpg"))
        paoli_photo.move_to(DOWN * 1.4 + RIGHT * 0.8)
        paoli_text = TextMobject("Wolfgang Paoli")
        paoli_text.move_to(DOWN * 3 + RIGHT * 0.8)

        self.play(
            FadeIn(de_rham_photo),
            Write(de_rham_text)
        )

        self.wait(2)

        self.play(
            FadeIn(paoli_photo),
            Write(paoli_text)
        )

        self.wait(1)

        self.play(
            FadeOut(de_rham_photo),
            FadeOut(de_rham_text),
            FadeOut(paoli_photo),
            FadeOut(paoli_text)
        )

        self.wait()


class DeRham(VerticalScene):
    def construct(self):
        de_rham_photo = ImageMobject(os.path.join(ASSETS_FOLDER, "./images/de_rham.jpg"))
        de_rham_text = TextMobject("De Rham Claudia").move_to(DOWN * 1.5)

        self.play(
            FadeIn(de_rham_photo),
            Write(de_rham_text),
            run_time=0.5
        )

        self.wait(2)

        self.play(
            FadeOut(de_rham_photo),
            FadeOut(de_rham_text),
            run_time=0.5
        )


class SadEinstein(VerticalScene):
    def construct(self):
        image = ImageMobject(os.path.join(ASSETS_FOLDER, "./images/sad_einstein.jpg"))

        self.play(FadeIn(image))

        self.wait(2)

        self.play(FadeOut(image))

        self.wait()


class BigCrunch(VerticalScene):
    def construct(self):
        galaxies = Group(*[Galaxy() for _ in range(100)])

        for g in galaxies:
            g.go_away(random.uniform(6, 16))

        self.add(galaxies)

        self.play(
            *[v(g) for g in galaxies for v in (lambda g: g.move_to,
                                               lambda g: np.array([0, 0, 0]),
                                               lambda g: g.scale,
                                               lambda g: 0.1)],
            run_time=3, rate_func=lambda t: pow(t, 2)
        )
        self.wait()


class LISA(VerticalScene):
    CONFIG = {
        "satellites_style": {
            "radius": 0.2,
            "fill_opacity": 1,
            "fill_color": "#000080",
            "color": "#003696"
        },
        "lasers_style": {
            "color": "#F00",
            "stroke_width": 15
        },
        "waves_style": {
            "color": "WHITE",
            "stroke_width": 30
        }
    }

    def construct(self):
        # creates the sun
        sun = ImageMobject(os.path.join(ASSETS_FOLDER, "./images/sun.png"), height=10)
        sun.move_to(DOWN * 8)

        # creates satellites
        sats = Group(*[Circle(**self.satellites_style) for _ in range(3)])
        # moves satellites to position
        for i in range(3):
            sats[i].move_to(2 * RIGHT)
            sats[i].rotate_about_origin(np.pi / 2 + i * 2 * np.pi / 3)

        # creates lasers between satellites
        lasers = Polygon(*[ORIGIN], **self.lasers_style)
        # binds lasers to satellites
        lasers.add_updater(lambda l: l.set_points_as_corners([s.get_center() for s in [*sats, sats[0]]]))

        # creates gravity waves
        waves = Group(*[Circle(radius=(i + 3) / 1.5, **self.waves_style) for i in range(5)])
        waves.move_to(10 * RIGHT + 5 * UP)

        # shows the sun
        self.play(GrowFromCenter(sun), run_time=1)

        # shows satellites
        self.play(*[GrowFromCenter(sats[i]) for i in range(3)], run_time=1)

        # starts rotation
        self.play(
            Rotate(sats, 1 * np.pi, about_point=ORIGIN),
            run_time=4, rate_func=linear
        )

        # shows lasers
        self.bring_to_back(lasers)
        self.play(
            Rotate(sats, 1 / 4 * np.pi, about_point=ORIGIN),
            ShowCreation(lasers),
            run_time=1, rate_func=linear
        )

        # waits waves
        self.play(
            Rotate(sats, 1 * np.pi, about_point=ORIGIN),
            run_time=4, rate_func=linear
        )

        # starts waves
        self.add(waves)
        self.play(
            Rotate(sats, 1 * np.pi, about_point=ORIGIN),
            *[v(w) for w in waves for v in (lambda w: w.scale, lambda w: 10)],
            run_time=4, rate_func=linear
        )

        # removes lasers
        self.play(
            Uncreate(lasers),
            run_time=0.5
        )

        # removes sun and satellites
        self.play(
            ScaleInPlace(sun, 0),
            ScaleInPlace(sats, 0),
            run_time=0.5
        )

        self.wait()


class MassiveGravityText(VerticalScene):
    def construct(self):
        text = TextMobject("Gravità massiva")

        self.wait()

        self.play(Write(text))

        self.wait()


class WaveRace(VerticalScene):
    def construct(self):
        light_text = TextMobject("Luce").move_to(DOWN * 4 + LEFT * 1.5)
        gravity_text = TextMobject("Gravità").move_to(DOWN * 4 + RIGHT * 1.5)

        light_wave = FunctionGraph(lambda x: np.sin(x * 3) / 3, x_min=0, x_max=9, color="yellow", stroke_width=5) \
            .rotate(90 * DEGREES) \
            .move_to(1 * UP + LEFT * 1.5)
        gravity_wave = FunctionGraph(lambda x: np.sin(x * 3) / 3, x_min=0, x_max=6, color="green", stroke_width=20) \
            .rotate(90 * DEGREES) \
            .move_to(0.5 * DOWN + RIGHT * 1.5)

        self.wait()

        self.play(
            Write(light_text),
            Write(gravity_text)
        )

        self.play(
            ShowCreation(light_wave),
            ShowCreation(gravity_wave),
            run_time=2, rate_func=linear
        )

        self.wait()


class Thinker(VerticalScene):
    def construct(self):
        thinker = ImageMobject(os.path.join(ASSETS_FOLDER, "./images/thinker.png"), height=8)

        self.wait()

        self.add(thinker)

        self.wait()

        self.play(ScaleInPlace(thinker, 0), run_time=0.5)

        self.wait()


class GravityPoints(VerticalScene):
    CONFIG = {
        "timeline": [1.0, 4.0, 5.0, 6.0],
        "point_small_style": {
            "radius": 0.2,
            "fill_opacity": 1,
            "stroke_width": 2,
            "fill_color": "#FF0000",
            "color": "#FF3696"
        },
        "point_big_style": {
            "radius": 0.7,
            "fill_opacity": 1,
            "stroke_width": 4,
            "fill_color": "#000080",
            "color": "#003696"
        }
    }

    def construct(self):
        point_small = Circle(**self.point_small_style).move_to(ma2v(6, 110 * DEGREES))
        point_big = Circle(**self.point_big_style).move_to(ma2v(-3, 110 * DEGREES))

        self.play(
            DrawBorderThenFill(point_small),
            DrawBorderThenFill(point_big),
            run_time=self.get_next_dt()
        )

        self.play(
            point_small.move_to, ma2v(0.2, 110 * DEGREES),
            point_big.move_to, ma2v(-0.7, 110 * DEGREES),
            rate_func=lambda t: pow(t, 2),
            run_time=self.get_next_dt()
        )

        self.wait(self.get_next_dt())

        self.play(
            ScaleInPlace(point_small, 0),
            ScaleInPlace(point_big, 0),
            run_time=self.get_next_dt()
        )


def ma2v(m: float, a: float):
    return m * (RIGHT * np.cos(a) + UP * np.sin(a))
