MANIM_COMMAND=manim
MANIM_ARGUMENTS=-r2520,1080 --high_quality
MANIM_ARGUMENTS_PREVIEW=-r630,270 -pl

MANIM_SOURCE=scenes/scenes.py

ifdef PREVIEW
	MANIM_ARGUMENTS=$(MANIM_ARGUMENTS_DEBUG)
endif

.PHONY: all clean all_scenes

all: all_scenes

clean:
	rm ./media -r

all_scenes: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) $(MANIM_ARGUMENTS) -a

# single scenes
scene_dark_energy: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) DarkEnergy $(MANIM_ARGUMENTS)

scene_de_rham_pauli: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) DeRhamAndPaoli $(MANIM_ARGUMENTS)

scene_sad_einstein: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) SadEinstein $(MANIM_ARGUMENTS)

scene_big_crunch: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) BigCrunch $(MANIM_ARGUMENTS)

scene_lisa: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) LISA $(MANIM_ARGUMENTS)

scene_massive_gravity_text: $(MANIM_SOURCE)
	$(MANIM_COMMAND) $(MANIM_SOURCE) MassiveGravityText $(MANIM_ARGUMENTS)