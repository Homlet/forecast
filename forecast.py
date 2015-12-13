"""A simple python program which predicts the next time a
   location will be photographed by NASA satellites.
"""
import sys
from datetime import datetime, timedelta

from geopy.geocoders import Nominatim
from nasa import earth
from requests import HTTPError

REQ_FORMAT = "%Y-%m-%d"
IN_FORMAT = "%Y-%m-%dT%H:%M:%S"
OUT_FORMAT = "%Y-%m-%d %H:%M:%S"
START_DATE = datetime.strftime(datetime.now() - timedelta(days=365),
                               REQ_FORMAT)


class BadInputError(Exception):
    def __init__(self, argv):
        super(BadInputError, self).__init__()
        self.arg_str = " ".join(argv)

    def __str__(self):
        return "Bad input given: " + self.arg_str


def td_average(deltas):
    """Find the average from a list of timedeltas."""
    add = lambda a, b: a + b
    return timedelta(seconds=
                     reduce(add, deltas).total_seconds() / len(deltas))


def forecast(coord):
    """Predict a date as the next time the given coord will be pictured."""
    over_quota = True
    while over_quota:
        try:
            # This will probably fail, due to NASA's poor, overworked servers.
            assets = earth.assets(coord[0], coord[1], START_DATE)
        except HTTPError:
            continue
        over_quota = False

    # Get a list of date-times for the photographs.
    dates = [datetime.strptime(asset.date, IN_FORMAT) for asset in assets]

    # Find the average wavelength between dates.
    deltas = []
    for i in range(1, len(dates)):
        deltas.append(dates[i] - dates[i-1])
    wavelength = td_average(deltas)

    # Find the average phase, relative to the first date.
    phases = []
    for i in range(1, len(dates)):
        phase = dates[i] - dates[0]
        while phase > wavelength:
            phase -= wavelength
        phases.append(phase)
    phase = td_average(phases)

    # Find the prediction by repeatedly adding the wavelength.
    prediction = dates[0] + phase + wavelength
    while prediction < datetime.now():
        prediction += wavelength

    return prediction


def process_input(argv):
    """Process the arguments and return a geographical coordinate.
    :param argv: User arguments.
    """
    # If the first argument is not an option, raise an error.
    if len(argv) == 0 or not argv[0][:2] == "--":
        raise BadInputError(argv)
    option = argv[0][2:]
    if option == "address":
        try:
            address = " ".join(argv[1:])
            location = Nominatim().geocode(address)
            return location.latitude, location.longitude
        except IndexError:
            # Not enough values were given.
            raise BadInputError(argv)
    elif option == "coord":
        # Try to interpret the arguments as a coordinate.
        try:
            lat = float(argv[1])
            lon = float(argv[2])
            return lat, lon
        except ValueError or IndexError:
            # Invalid values were given, or not enough values.
            raise BadInputError(argv)
    else:
        # The option is invalid; raise an error.
        raise BadInputError(argv)


if __name__ == "__main__":
    try:
        argv = sys.argv
        # The first argument supplied might be a path to the script.
        if argv[0][-11:] == "forecast.py":
            # If so, discard it.
            argv = argv[1:]
        # Get a coordinate from the input, then forecast for it.
        coord = process_input(argv)
        prediction = forecast(coord)
        print datetime.strftime(prediction, OUT_FORMAT)
    except BadInputError as e:
        print e
        print("Usage: python forecast.py "
              "[--address [textual address] | --coord LAT LON]")
