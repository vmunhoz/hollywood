import os
import cv2
import numpy as np
import random
import math


class Hollywood():
    def __init__(self, width=1920, height=1080, output='video.avi', fps=30.0):
        self._video = None
        self.width = width
        self.height = height
        self.fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.fps = fps
        self.output = output
        self._get_all_images()
        self.video = cv2.VideoWriter(
            self.output, self.fourcc, self.fps, (self.width, self.height))

    def _get_all_images(self):
        self.persons_paths = []
        for dirpath, dirnames, filenames in os.walk('persons'):
            for f in filenames:
                if f.endswith('.png') or f.endswith('.jpg'):
                    self.persons_paths.append(dirpath + '/' + f)
        self.persons_paths.sort()

    def _get_person_path(self, i=0):
        # return random.choice(self.persons_paths)
        while i > len(self.persons_paths) - 1:
            i -= len(self.persons_paths)
        return self.persons_paths[i]

    def _fit_in_the_middle(self, frame, image):
        frame_y, frame_x, _ = frame.shape
        image_y, image_x, _ = image.shape

        padding_x = math.floor((frame_x - image_x) / 2)
        padding_y = math.floor((frame_y - image_y) / 2)

        frame[padding_y:padding_y+image_y, padding_x:padding_x+image_x] = image
        return frame


    def _resize_to_fit_frame(self, frame, image, rows, cols):
        frame_y, frame_x, _ = frame.shape
        image_y, image_x, _ = image.shape

        height = math.floor(frame_y / rows)
        max_width = math.floor(frame_x / cols)

        # adjust height first
        ratio = height / float(image_y)
        width = int(image_x * ratio)

        if width > max_width:
            # adjust width
            ratio = max_width / float(width)
            height = int(height * ratio)
            width = max_width
        
        return cv2.resize(image, (width, height))


    def _build_square(self, frame, rows, cols):
        height = math.floor(frame.shape[0] / rows)
        width = math.floor(frame.shape[1] / cols)
        return np.zeros((height, width, 3), dtype='uint8') + 255

    def add_frame(self, frame):
        self.video.write(frame)

    def wait(self, seconds):
        white_frame = np.zeros((self.height, self.width, 3), dtype='uint8') + 255
        for _ in range(seconds * int(self.fps)):
            self.add_frame(white_frame)

    def show_person(self, seconds, num_persons=1, rows=2, cols=5):
        print('show_person: {} segundos, {} pessoas, em uma grid [{},{}]'.format(seconds, num_persons, rows, cols))
        new_frame = np.zeros((self.height, self.width, 3), dtype='uint8') + 255
        frame_y, frame_x, _ = new_frame.shape
        last_offset_x = 0
        next_offset_x = 0
        last_offset_y = 0

        height = math.floor(frame_y / rows)
        width = math.floor(frame_x / cols)

        for i in range(num_persons):
            square = self._build_square(new_frame, rows, cols)
            person_img = cv2.imread(self._get_person_path(i))
            person_img = self._resize_to_fit_frame(new_frame, person_img, rows, cols)
            square = self._fit_in_the_middle(square, person_img)

            person_y, person_x, _ = person_img.shape
            offset_x = next_offset_x
            offset_y = last_offset_y
            while (width + offset_x) > frame_x:
                offset_x = 0
                offset_y = last_offset_y + height
            
            last_offset_x = offset_x
            # next_offset_x = last_offset_x + person_x
            next_offset_x = last_offset_x + width
            last_offset_y = offset_y


            # print('{} --- person x {}:{}, y {}:{}'.format(i, 0, person_x, 0, person_y))
            # print('{} --- recorte x {}:{}, y {}:{}\n'.format(i, offset_x, person_x + offset_x, offset_y, person_y + offset_y))

            new_frame[offset_y:height + offset_y,
                      offset_x:width + offset_x] = square

        # new_frame = cv2.add(new_frame, person_img)
        for _ in range(seconds * int(self.fps)):
            self.add_frame(new_frame)

    def _walk_one(self, current_position, step):
        return (current_position[0] + step[0], current_position[1] + step[1])

    def slide_person(self, move_seconds, hold_seconds=0, slide_direction='down', rows=2, cols=5):
        """ possible border_from = up, right, down, left """
        frame = np.zeros((self.height, self.width, 3), dtype='uint8') + 255
        frame_y, frame_x, _ = frame.shape

        square = self._build_square(frame, rows, cols)
        person_img = cv2.imread(self._get_person_path())
        person_img = self._resize_to_fit_frame(frame, person_img, rows, cols)
        square = self._fit_in_the_middle(square, person_img)

        square_y, square_x, _ = square.shape
        total_frames = move_seconds * int(self.fps)

        pos = (0, 0)
        final_position = (frame_y, 0)
    
        if slide_direction == 'down':
            pos = (square_y*-1, 0)
            final_position = (frame_y, 0)

        if slide_direction == 'up':
            pos = (frame_y, 0)
            final_position = (square_y*-1, 0)
        
        if slide_direction == 'right':
            pos = (0, square_x*-1)
            final_position = (0, frame_x)
        
        if slide_direction == 'left':
            pos = (0, frame_x)
            final_position = (0, square_x*-1)

        step = (math.ceil((final_position[0] - pos[0]) / total_frames), 
                math.ceil((final_position[1] - pos[1]) / total_frames))


        for i in range(total_frames):
            frame = np.zeros((self.height, self.width, 3), dtype='uint8') + 255
            # print('--------------------------')
            # print(pos[0], pos[0] + square_y, (pos[0] + square_y) - pos[0] )
            # print(frame[pos[0]:square_y + pos[0], pos[1]:square_x + pos[1]].shape)
            # print(square.shape)

            overflow_y = max(0, (square_y + pos[0]) - frame_y)
            overflow_x = max(0, (square_x + pos[1]) - frame_x)

            # print(overflow_y, overflow_x)
            # print(square_y - overflow_y, square_x - overflow_x)
            # print('--------------------------')

            if square_y - overflow_y < 0 or square_x - overflow_x < 0:
                print(pos)
                print('D=')
                continue


            init_frame_y = pos[0]
            init_square_y = 0

            init_frame_x = pos[1]
            init_square_x = 0

            if pos[0] < 0:
                init_frame_y = 0
                init_square_y = pos[0]

            if pos[1] < 0:
                init_frame_x = 0
                init_square_x = pos[1]

            frame[init_frame_y:square_y + pos[0] - overflow_y, 
                    init_frame_x:square_x + pos[1] - overflow_x] = square[0 - init_square_y:square_y - overflow_y, 0 - init_square_x:square_x - overflow_x]

            self.add_frame(frame)
            pos = self._walk_one(pos, step)
        print(final_position)


    def close_video(self):
        self.video.release()
        print(self.video)



# img1 = cv2.imread('1.jpg')
# height, width, layers = img1.shape

# video.write(img1)
# video.write(img2)
# video.write(img3)

# cv2.destroyAllWindows()
# video.release()


