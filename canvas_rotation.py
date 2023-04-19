import pygame, expyriment, math
from expyriment import stimuli, design, control, misc
from pygame.transform import rotozoom

# PARAMETERS

n_disks = 8
circle_radius = 120
disk_radius = 15
rotation_angle = 3
number_of_circle_positions = int(360/rotation_angle)
cut_angle = math.pi

presentation_time = 55
delay1_start = 2000
delay1_end = delay1_start+presentation_time
delay2_start = delay1_start+presentation_time
delay2_end = delay1_start+2*presentation_time

white = (240,240,240)
black = (0,0,0)
purple = (138, 23, 226)

# FUNCTIONS

def mask_right_half_disk(half_canvas):
    square_stim = expyriment.stimuli.Rectangle(size=(disk_radius*2, disk_radius),
                                                    position=(x, y-(disk_radius/2)),
                                                    colour=white)
    square_stim.plot(half_canvas)

def mask_left_half_disk(half_canvas):
    square_stim = expyriment.stimuli.Rectangle(size=(disk_radius*2, disk_radius),
                                                    position=(x, y+(disk_radius/2)),
                                                    colour=white)
    square_stim.plot(half_canvas)

def setting_canvas_list(canvas, canvas_list):
    for i in range (number_of_circle_positions):
        surf_stim = canvas.get_surface_copy()
        surf_stim = rotozoom(surf_stim, i*rotation_angle, 1.0)
        new_canvas = stimuli.Canvas(size=(300,300),
                                    colour= white)
        new_canvas.set_surface(surf_stim)
        canvas_list.append(new_canvas)

def create_canvas_with_circle():
    canvas = stimuli.Canvas(size=(300,300),
                                colour= white)
    circle_stim = stimuli.Circle(radius=circle_radius,
                                line_width=2,
                                colour= purple)
    circle_stim.plot(canvas)
    return canvas

# STARTING THE EXPERIMENT
exp = design.Experiment(name="Rotating circle with disks", background_colour=white)
expyriment.control.initialize(exp)

# CREATING THE CANVAS
full_canvas = create_canvas_with_circle()
halfL_canvas = create_canvas_with_circle()
halfR_canvas = create_canvas_with_circle()

# PLOTTING THE DISKS
for i in range(n_disks):
    angle = i * 2 * math.pi / n_disks
    x = circle_radius * math.cos(angle)
    y = circle_radius * math.sin(angle)
    disk_stim = expyriment.stimuli.Circle(radius=disk_radius,
                                           position=(x, y),
                                           colour=purple)
    disk_stim.plot(halfL_canvas)
    disk_stim.plot(halfR_canvas)
    disk_stim.plot(full_canvas)
    if i == 0:
        mask_left_half_disk(halfL_canvas)
        mask_right_half_disk(halfR_canvas)
    
# CREATE THREE LISTS OF CANVAS
full_canvas_list = []
halfL_canvas_list = []
halfR_canvas_list = []
setting_canvas_list(full_canvas, full_canvas_list)
setting_canvas_list(halfL_canvas, halfL_canvas_list)
setting_canvas_list(halfR_canvas, halfR_canvas_list)

# PRESENTING THE FULL DISK - STATIC
blankscreen = stimuli.BlankScreen()
blankscreen.present()
full_canvas.present()

# ROTATING THE FULL DISK
clock = expyriment.misc.Clock()
time_list = []
while clock.time < 5000:
    for i in range (number_of_circle_positions):
        t1 = clock.time
        if t1 >delay1_start and t1 <delay1_end:
            halfL_canvas_list[i].present()
        elif t1 >delay2_start and t1 <delay2_end:
            halfR_canvas_list[i].present()
        else:
            full_canvas_list[i].present()
        t = clock.time - t1
        time_list.append(t)

print(time_list)

# END
expyriment.control.end()