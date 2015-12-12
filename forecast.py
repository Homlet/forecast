"""A simple python program which predicts the next time a
   location will be photographed by NASA satellites.
"""
import sys

from nasa import earth


START_DATE = "2010-01-01"


class BadInputError(Exception):
    def __init__(self, argv):
        super(BadInputError, self).__init__()
        self.arg_str = " ".join(argv)

    def __str__(self):
        return "Bad input given: " + self.arg_str


def forecast(coords):
    """Predict a date as the next time the given coords will be photographed."""
    assets = earth.assets(coords[0], coords[1], START_DATE)
    for asset in assets:
        print(asset)
    return "Never."


def process_input(argv):
    """Process the arguments and return a geographical coordinate.
    :param argv: User arguments.
    """
    if not 2 <= argv.length <= 3:
        raise BadInputError(argv)
    return 0.0, 0.0


if __name__ == "__main__":
    try:
        coords = process_input(sys.argv)
        print(forecast(coords))
    except BadInputError as e:
        print(e)
        print("Usage: python forecast.py "
              "[--address [textual address] | --coord LAT LONG]")
