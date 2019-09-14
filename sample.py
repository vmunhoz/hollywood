""" Sample file. """
from hollywood import Hollywood

h = Hollywood()


h.wait(1)  # wait 1 second

h.show_car(2, num_cars=1, rows=1, cols=1)
h.show_car(2, num_cars=5)

h.wait(1)

h.show_person(2, num_persons=1, rows=1, cols=1)
h.show_person(2, num_persons=3, rows=1, cols=3)
h.show_person(2, num_persons=5)

h.wait(1)

h.slide_car(3, slide_direction="down", rows=1, cols=1)
h.slide_car(3, slide_direction="up", rows=1, cols=1, index=1)
h.slide_car(3, slide_direction="right", rows=1, cols=1, index=2)
h.slide_car(3, slide_direction="left", rows=1, cols=1, index=3)

h.wait(1)

h.slide_person(3, slide_direction="down", rows=1, cols=1)
h.slide_person(3, slide_direction="up", rows=1, cols=1, index=1)
h.slide_person(3, slide_direction="right", rows=1, cols=1, index=2)
h.slide_person(3, slide_direction="left", rows=1, cols=1, index=3)


h.wait(1)

h.slide_person(3, slide_direction="right", rows=1, cols=1, index=13)
h.slide_person(3, slide_direction="right", rows=1, cols=3, index=13)
h.slide_person(3, slide_direction="right", rows=1, cols=5, index=13)


h.close_video()  # finaliza o video
