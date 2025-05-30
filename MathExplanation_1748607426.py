from manim import *

config.background_color = "#1f1f1f"

class SineCosineComparison(Scene):
    def construct(self):
        title = Tex("Sine vs. Cosine").scale(1.5).set_color(YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        sin_text = MathTex(r"\sin(x)").set_color(BLUE)
        cos_text = MathTex(r"\cos(x)").set_color(GREEN)

        sin_text.next_to(title, DOWN, buff=1)
        cos_text.next_to(sin_text, RIGHT, buff=2)

        self.play(Write(sin_text), Write(cos_text))
        self.wait(2)

        self.play(FadeOut(title, sin_text, cos_text))
        self.wait(1)

        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            axis_config={"color": WHITE},
            tips=False,
        )
        circle = Circle(radius=1, color=WHITE).set_stroke(width=2)
        unit_circle_group = VGroup(axes, circle)
        unit_circle_group.scale(2).to_edge(LEFT, buff=1)

        self.play(Create(axes), Create(circle))
        self.wait(1)

        angle = 30 * DEGREES
        line = Line(ORIGIN, np.array([np.cos(angle), np.sin(angle), 0])).set_color(YELLOW)
        dot = Dot(np.array([np.cos(angle), np.sin(angle), 0])).set_color(RED)
        angle_arc = Arc(radius=0.3, start_angle=0, angle=angle).set_color(ORANGE)
        angle_label = MathTex(r"\theta").next_to(angle_arc, RIGHT, buff=0.1).set_color(ORANGE)

        self.play(Create(line), Create(dot), Create(angle_arc), Write(angle_label))
        self.wait(1)

        sin_line = DashedLine([np.cos(angle), np.sin(angle), 0], [np.cos(angle), 0, 0], color=BLUE)
        cos_line = DashedLine([np.cos(angle), np.sin(angle), 0], [0, np.sin(angle), 0], color=GREEN)
        sin_label = MathTex(r"\sin(\theta)").set_color(BLUE).next_to(sin_line, RIGHT)
        cos_label = MathTex(r"\cos(\theta)").set_color(GREEN).next_to(cos_line, UP)

        self.play(Create(sin_line), Create(cos_line), Write(sin_label), Write(cos_label))
        self.wait(2)

        for new_angle in [60 * DEGREES, 90 * DEGREES, 120 * DEGREES, 150 * DEGREES]:
            new_line = Line(ORIGIN, np.array([np.cos(new_angle), np.sin(new_angle), 0])).set_color(YELLOW)
            new_dot = Dot(np.array([np.cos(new_angle), np.sin(new_angle), 0])).set_color(RED)
            new_angle_arc = Arc(radius=0.3, start_angle=0, angle=new_angle).set_color(ORANGE)
            new_angle_label = MathTex(r"\theta").next_to(new_angle_arc, RIGHT, buff=0.1).set_color(ORANGE)

            new_sin_line = DashedLine([np.cos(new_angle), np.sin(new_angle), 0], [np.cos(new_angle), 0, 0], color=BLUE)
            new_cos_line = DashedLine([np.cos(new_angle), np.sin(new_angle), 0], [0, np.sin(new_angle), 0], color=GREEN)
            new_sin_label = MathTex(r"\sin(\theta)").set_color(BLUE).next_to(new_sin_line, RIGHT)
            new_cos_label = MathTex(r"\cos(\theta)").set_color(GREEN).next_to(new_cos_line, UP)

            self.play(
                Transform(line, new_line),
                Transform(dot, new_dot),
                Transform(angle_arc, new_angle_arc),
                Transform(angle_label, new_angle_label),
                Transform(sin_line, new_sin_line),
                Transform(cos_line, new_cos_line),
                Transform(sin_label, new_sin_label),
                Transform(cos_label, new_cos_label),
                run_time=2
            )
            self.wait(1)

        self.play(FadeOut(line, dot, angle_arc, angle_label, sin_line, cos_line, sin_label, cos_label, unit_circle_group))
        self.wait(1)

        axes = Axes(
            x_range=[-PI, 3 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": WHITE},
            tips=False,
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        axes.to_edge(LEFT, buff=1)

        sine_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cosine_graph = axes.plot(lambda x: np.cos(x), color=GREEN)

        sine_label = MathTex(r"y = \sin(x)").set_color(BLUE).next_to(sine_graph, UP)
        cosine_label = MathTex(r"y = \cos(x)").set_color(GREEN).next_to(cosine_graph, UP)

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(sine_graph), Write(sine_label))
        self.wait(1)
        self.play(Create(cosine_graph), Write(cosine_label))
        self.wait(2)

        shifted_cosine = axes.plot(lambda x: np.cos(x - PI / 2), color=ORANGE)
        shifted_cos_label = MathTex(r"y = \cos\left(x - \frac{\pi}{2}\right)").set_color(ORANGE).next_to(shifted_cosine, UP)

        self.play(Transform(cosine_graph, shifted_cosine), Transform(cosine_label, shifted_cos_label))
        self.wait(1)

        phase_shift_text = Tex("Cosine is a shifted Sine").set_color(YELLOW).scale(0.8)
        phase_shift_text.to_edge(DOWN)
        self.play(Write(phase_shift_text))
        self.wait(2)

        sin_equals_shifted_cos = MathTex(r"\sin(x) = \cos\left(x - \frac{\pi}{2}\right)").set_color(YELLOW).to_edge(DOWN)
        self.play(Transform(phase_shift_text, sin_equals_shifted_cos))
        self.wait(3)

        self.wait(3)