import glob
from typing import Union, Tuple

from manimlib.imports import *

ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets/")


class VerticalScene(Scene):
    CONFIG = {
        "camera_config": {
            "frame_height": 6.0 * 21 / 9,
            "frame_width": 6.0,
        }
    }


class Galaxy(ImageMobject):
    list = glob.glob(os.path.join(ASSETS_FOLDER, "./galaxies/*"))

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


class DeRhamAndPaoli(VerticalScene):
    def construct(self):
        de_rham_photo = ImageMobject(os.path.join(ASSETS_FOLDER, "./de_rham.jpg"))
        de_rham_photo.move_to(UP * 1.4 + LEFT * 0.8)
        de_rham_text = TextMobject("De Rham Claudia")
        de_rham_text.move_to(UP * 3 + LEFT * 0.8)

        paoli_photo = ImageMobject(os.path.join(ASSETS_FOLDER, "./paoli.jpg"))
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


class SadEinstein(VerticalScene):
    def construct(self):
        image = ImageMobject(os.path.join(ASSETS_FOLDER, "./sad_einstein.jpg"))

        self.play(FadeIn(image))

        self.wait(2)

        self.play(FadeOut(image))

        self.wait()
