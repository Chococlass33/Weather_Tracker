import argparse

parser = argparse.ArgumentParser(description='Add some integers.')

parser.add_argument('api', metavar='api', type=int, nargs='+',
                    help='api key')

parser.add_argument('--sum', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

print(args.sum(args.integers))
