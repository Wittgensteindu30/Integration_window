import pygame, expyriment, math, random
from expyriment import stimuli, design, control, misc
from pygame.transform import rotozoom

# PARAMETERS

n_trials = 25
delay_before_rotation = 500
delay_presentation_list = [-70, -35, 0, 35, 70]
presentation_time_list = [15, 30, 45, 60]
delay_rotation_change = 800

n_disks = 8
circle_radius = 120
disk_radius = 15
rotation_angle = 3
number_of_circle_positions = int(360/rotation_angle)
cut_angle = math.pi

white = (240,240,240)
black = (0,0,0)
purple = (138, 23, 226)

yes_detection = 'f'
no_detection = 'j'
max_response_delay = 2000

# FUNCTIONS

def mask_half_disk(half_canvas, left_or_right):
    if left_or_right == 'right':
        square_stim = expyriment.stimuli.Rectangle(size=(disk_radius*2, disk_radius),
                                                    position=(x, y-(disk_radius/2)),
                                                    colour=white)
    else:
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

def setting_the_trials(n_trials):
    trials_list = []
    for x in range (n_trials):
        for y in range (len(presentation_time_list)):
            presentation_time = presentation_time_list[y]
            for w in range (len(delay_presentation_list)):
                delay_presentation = delay_presentation_list[w] 
                i_trial = (presentation_time, delay_presentation)
                trials_list.append(i_trial)
    random.shuffle(trials_list)
    return trials_list


def setting_the_delays(delay_presentation, delay_rotation_change):
    delay1_start = delay_presentation+delay_rotation_change
    delay1_end = delay1_start+presentation_time
    delay2_start = delay1_start+presentation_time
    delay2_end = delay1_start+2*presentation_time
    return delay1_start, delay1_end, delay2_start, delay2_end

# STARTING THE EXPERIMENT
exp = design.Experiment(name="Rotating circle with disks", background_colour=white)
expyriment.control.initialize(exp)
trials_list = setting_the_trials(n_trials)

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
        mask_half_disk(halfL_canvas, 'left')
        mask_half_disk(halfR_canvas, 'right')
    
# CREATE THREE LISTS OF CANVAS
full_canvas_list = []
halfL_canvas_list = []
halfR_canvas_list = []
setting_canvas_list(full_canvas, full_canvas_list)
setting_canvas_list(halfL_canvas, halfL_canvas_list)
setting_canvas_list(halfR_canvas, halfR_canvas_list)

# CREATING THE VARIABLES
exp.add_data_variable_names(['trial', 'delay_rotation_change', 'stimulus_delay', 'detection', 'reaction time'])

# PRESENTING THE INSTRUCTIONS
lankscreen = stimuli.BlankScreen()
instructions = stimuli.TextScreen("Instructions",
    f"""You will see one circle composed of eight disks rotate and change rotation.

    Your task is to report every time you see one odd disk. 
    When one disk appears to be different than the others, press {yes_detection}.
    If all disks look the same to you, press {no_detection}.

    Press the spacebar to start.""", text_colour=black)
instructions.present()
exp.keyboard.wait()
expyriment.control.start(exp)

# ROTATING THE FULL DISK
for i_trial in range (n_trials):
    blankscreen = stimuli.BlankScreen()
    blankscreen.present()
    full_canvas.present()
    pygame.time.wait(delay_before_rotation)
    presentation_time, stimulus_delay = trials_list[i_trial]
    delay1_start, delay1_end, delay2_start, delay2_end = setting_the_delays(stimulus_delay, delay_rotation_change)
    print(delay1_start, delay1_end, delay2_start, delay2_end)
    clock = expyriment.misc.Clock()
    time_list = []
    while clock.time < 1200:
        while clock.time < delay_rotation_change:
            for i in range (number_of_circle_positions):
                t1 = clock.time
                if t1 >delay1_start and t1 <delay1_end:
                    halfL_canvas_list[i].present()
                    print(t1)
                elif t1 >delay2_start and t1 <delay2_end:
                    halfR_canvas_list[i].present()
                else:
                    full_canvas_list[i].present()
                t = clock.time - t1
                time_list.append(t)
                landmark = i
                if clock.time > delay_rotation_change:
                    break
        for x in range (number_of_circle_positions):
            t1 = clock.time
            print(t1)
            if t1 >delay1_start and t1 <delay1_end:
                halfL_canvas_list[landmark-x].present()
            elif t1 >delay2_start and t1 <delay2_end:
                halfR_canvas_list[landmark-x].present()
            else:
               full_canvas_list[landmark-x].present()
            t = clock.time - t1
            time_list.append(t)
            if clock.time > 1200:
                break
    blankscreen.present()
    key, rt = exp.keyboard.wait_char([yes_detection, no_detection], duration=max_response_delay)
    exp.data.add([i_trial, delay_rotation_change, stimulus_delay, rt])
    print(i_trial)

#prompt
print(time_list)

# END
expyriment.control.end()