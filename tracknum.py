#!/usr/bin/env python3

# Written by Gem Newman. This work is licensed under the MIT License.


from argparse import ArgumentParser
from mutagen.easyid3 import EasyID3
import re, os


PATTERN = r'^(\d+).*\.mp3'
p = re.compile(PATTERN)


def main():
    parser = ArgumentParser(
        description='Adds (or overwrites) the ID3 track number in any MP3 file'
        'with a file name beginning with a number.')
    parser.add_argument("dir", nargs='?',
        help='The directory to process. Defaults to ".".', default='.')
    args = parser.parse_args()

    # List all files in the dir
    files = os.listdir(args.dir)

    # Filter to only those that match the pattern
    files = list(filter(p.match, files))

    for file in files:
        track = int(p.match(file).group(1))
        print(file)
        audio = EasyID3(file)
        audio['tracknumber'] = str(track)
        audio.save()

    print('Done')


if __name__ == "__main__":
    main()

