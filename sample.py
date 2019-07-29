from hollywood import Hollywood

h = Hollywood()


h.wait(1)  # espera 10 segundos


# h.show_person(3, num_persons=3, rows=1, cols=3)
# h.show_person(10, num_persons=10)

h.slide_person(3, slide_direction="down", rows=1, cols=1)
h.slide_person(3, slide_direction="up", rows=1, cols=1)
h.slide_person(5, slide_direction="right", rows=1, cols=1)
h.slide_person(5, slide_direction="left", rows=1, cols=1)


h.wait(1)  # espera 10 segundos


h.close_video()  # finaliza o video
