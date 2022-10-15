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
    parser.add_argument("dir", nargs='?', default='.',
        help='The directory to process. Defaults to ".".')
    parser.add_argument("--file", '-f', nargs='?', help='If provided, '
        'processes a single file instead of the specified directory.')
    parser.add_argument("--verbose", '-v', action='store_true')
    args = parser.parse_args()

    if args.file:
        files = [args.file]
    else:
        # List all files in the dir
        files = os.listdir(args.dir)

        # Filter to only those that match the pattern
        files = list(filter(p.match, files))

    for file in files:
        if args.verbose:
            print(file)

        track = int(p.match(file).group(1))

        if not track > 0:
            if args.verbose:
                print(f'Skipping invalid track number: {track}')
            continue

        # Append full path for files (since listdir only returns the filename)
        if not args.file:
            file = os.path.join(args.dir, file)

        audio = EasyID3(file)
        audio['tracknumber'] = str(track)
        audio.save()

    if args.verbose:
        print('Done')


if __name__ == "__main__":
    main()

