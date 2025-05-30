from manim import *

config.background_color = "#1f1f1f"

class SphereVolume(ThreeDScene):
    def construct(self):
        title = Tex("Calculating the Volume of a Sphere").scale(1.2).set_color(YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        formula = MathTex(r"V = \frac{4}{3} \pi r^3").set_color(GREEN)
        formula.scale(1.5)
        formula.next_to(title, DOWN, buff=1)
        self.play(Write(formula))
        self.wait(2)

        explanation = VGroup(
            Tex("Where:"),
            Tex(r"$V$ is the volume of the sphere,"),
            Tex(r"$r$ is the radius of the sphere,"),
            Tex(r"$\pi$ is a constant approximately equal to 3.14159.")
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation.next_to(formula, DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(3)
        self.play(FadeOut(explanation))

        radius_text = Tex("Let us use a specific radius, for example $r=2$.").set_color(BLUE)
        radius_text.next_to(formula, DOWN, buff=1)
        self.play(Write(radius_text))
        self.wait(2)
        self.play(FadeOut(radius_text))

        substitution = MathTex(r"V = \frac{4}{3} \pi (2)^3").set_color(BLUE)
        substitution.scale(1.2)
        substitution.next_to(formula, DOWN, buff=1)
        self.play(Write(substitution))
        self.wait(2)

        calculation1 = MathTex(r"V = \frac{4}{3} \pi \times 8").set_color(BLUE)
        calculation1.scale(1.2)
        calculation1.next_to(formula, DOWN, buff=1)
        self.play(TransformMatchingTex(substitution, calculation1))
        self.wait(2)

        calculation2 = MathTex(r"V = \frac{32}{3} \pi").set_color(BLUE)
        calculation2.scale(1.2)
        calculation2.next_to(formula, DOWN, buff=1)
        self.play(TransformMatchingTex(calculation1, calculation2))
        self.wait(2)

        result = MathTex(r"V \approx \frac{32}{3} \times 3.14159 \approx 33.51").set_color(GREEN)
        result.scale(1.2)
        result.next_to(formula, DOWN, buff=1)
        self.play(TransformMatchingTex(calculation2, result))
        self.wait(2)

        units = Tex(" cubic units").set_color(WHITE)
        units.next_to(result, RIGHT)
        self.play(Write(units))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(formula), FadeOut(result), FadeOut(units))
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        sphere = Sphere(radius=2, resolution=(50, 50)).set_color(BLUE)
        sphere_label = MathTex(r"r=2").set_color(WHITE)
        sphere_label.next_to(sphere, UP)
        self.play(Create(sphere), Write(sphere_label))
        self.wait(5)
        self.play(FadeOut(sphere), FadeOut(sphere_label))

        conclusion = Tex("Thus, the volume of a sphere with radius $r=2$ is approximately $33.51$ cubic units.").set_color(YELLOW)
        conclusion.scale(1.2)
        conclusion.to_edge(UP)
        self.play(Write(conclusion))
        self.wait(3)

        self.play(FadeOut(conclusion))