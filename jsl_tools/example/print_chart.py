import argparse

def print_chart(numbers):
    for n in numbers:
        if n > 0:
            print("📈")
        elif n < 0:
            print("📉")
        else:
            print("📊")





if __name__ == "__main__":
    # Consider adding your own arg-passer to make script standalone
    parser = argparse.ArgumentParser(description='Select chart')
    parser.add_argument('numbers', nargs='+', type=int)

    args = parser.parse_args()
    print_chart(args.numbers)
