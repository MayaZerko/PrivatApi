import sys

from utils import get_days, get_few_dates, get_currencies


def main():
    days = get_days(sys.argv)
    few_days = get_few_dates(days)
    currencies = get_currencies(sys.argv)


if __name__ == "__main__":
    exit(main())
