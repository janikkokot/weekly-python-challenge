import argparse

BASE = 'base/solution.py'


def get_examples(file):
    with open(file) as f:
        examples = []
        for line in f:
            if line.startswith('>>>'):
                examples.append('    ' + line)
                examples.append('    ' + next(f))
                examples.append('\n')
    return examples


def replace(flag, examples):
    with open(BASE) as f:
        lines = []
        for line in f:
            if flag in line:
                break
            lines.append(line)

        lines.extend(examples)
        for line in f:
            lines.append(line)
    return lines


def main(filename):
    a = get_examples(filename)
    lines = replace('_EXAMPLE_', a)
    return lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()
    print(''.join(main(args.filename)))
