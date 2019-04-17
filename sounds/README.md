# How to create MP3 sound bites

Copy the following contents to a local file called `youtube-audio.py`:

```python
#!/usr/bin/env python

# OS dependencies:
#  - youtube-dl
#  - ffmpeg
#  - mpg123

from subprocess import call
import os.path
import re
import sys

# Check if all parameters are provided
if len(sys.argv) != 5:
    print("Usage: youtube-audio.py MOVIE_ID FROM_TIME LENGTH SOUND_NAME")
    sys.exit(1)

movie_id = sys.argv[1]
from_time = sys.argv[2]
length = sys.argv[3]
sound_name = re.sub(r'[ \t]+', '-', sys.argv[4])

entire_mp3_file = "%s-%s.mp3" % (movie_id, sound_name)
part_mp3_file = "%s.mp3" % sound_name

# If the mp3 file is already downloaded, don't do it again
if os.path.isfile(entire_mp3_file):
    print("%s already exists, skip downloading" % entire_mp3_file)
else:
    call("youtube-dl --extract-audio --audio-format mp3 --output %s https://www.youtube.com/watch?v=%s" % (
        entire_mp3_file, movie_id), shell=True)

# Extract the mp3 part from the entire mp3
call('ffmpeg -ss %s -t %s -i %s "%s"' % (from_time, length, entire_mp3_file, part_mp3_file), shell=True)

# Play the mp3 part
call("mpg123 %s" % part_mp3_file, shell=True)
```

Be sure to install all dependencies. For Debian based systems, do:

```
sudo apt-get install youtube-dl
sudo apt-get install ffmpeg
sudo apt-get install mpg123
```

And on Mac OSX, with [Brew](http://brew.sh), do:

```
brew install youtube-dl
brew install ffmpeg
brew install mpg123
```

Downloading sounds from Youtube can now be done like this:

```
youtube-audio.py YOUTUBE-ID START-TIME LENGTH "NAME-AUDIO-FILE"
```

For example, if you'd like to download 2.5 seconds starting at 1:35 and 750 milliseconds 
from the movie https://www.youtube.com/watch?v=VM4KBOv-O-g, run the following command:

```
youtube-audio.py VM4KBOv-O-g 1:35.750 2.500 "superman no here"
```

Then, make a pull request where you add the file `sounds/family.guy/consuela/superman-no-here.mp3`

