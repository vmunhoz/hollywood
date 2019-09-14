# Hollywood

Hollywood is a python library that generates video files with common situations used in the QA process of video analysis software.

## Usage

Example code:

``` python
from hollywood import Hollywood

h = Hollywood()

h.show_person(3) # shows a person for 3 seconds
h.wait(1) # 1 second of blank video
h.show_person(10, num_persons=5) # shows 5 persons for 10 seconds

h.close_video() # saves the video file as video.avi

```

### More examples

You can find more examples of usage in the `sample.py` file

## Converting to mp4

You can convert the output using ffmpeg:

``` bash
ffmpeg -y -i video.avi video.mp4
```