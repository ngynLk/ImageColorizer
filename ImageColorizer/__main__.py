import subprocess
from .ClassModule import ImageColorizer
import argparse


def output(command):
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='File to generate image from.')
    parser.add_argument('output', help='File to generate image to.')
    parser.add_argument(
        '-x', '--xresources', help='Get palette from Xresources.', action='store_true')
    parser.add_argument(
        '-c', '--colorer', help='Get palette from colorer.', metavar='COLORSCHEME')
    parser.add_argument(
        '-s', '--show', help='Show image using xdg-open when image is generated.', action='store_true')
    parser.add_argument(
        '--average', help='Use average algorithm (calculate the average color of each pixel with the pixels around) to generate the wallpaper, and set the size of the box to calculate the color from', type=int, metavar='BOX_SIZE')
    args = parser.parse_args()

    img_col = ImageColorizer()

    values = []
    if args.xresources:
        values = output('xrdb -query | cut -f 2').split('\n')
    elif args.colorer is not None:
        values = output(
            'colorer --get all {}'.format(args.colorer)).split('\n')
    img_col.load_palette(values)

    img_col.set_average(args.average is not None, args.average)

    img_col.generate(args.input, args.output, show=args.show)


if __name__ == '__main__':
    main()
