import datetime
import random
from math import floor

from util import QuestionGenerator, generator
from fractions import Fraction


@generator
class TimeDifferenceGen(QuestionGenerator):
    @staticmethod
    def datetime_formatter(d):
        return f'{d.hour if d.hour <= 12 else d.hour - 12}:{d.minute:02}{"AM" if d.hour < 12 else "PM"}'

    def generate_value(self):
        d1 = datetime.datetime(2003, 1, 1, random.randint(1, 23), random.randint(0, 59))
        d2 = datetime.datetime(2003, 1, 1, random.randint(1, 23), random.randint(0, 59))
        return [d1, d2] if d1 > d2 else [d2, d1]

    def generate_text(self, values):
        d1 = values[0]
        d2 = values[1]
        return f'How many minutes are between {self.datetime_formatter(d2)} and {self.datetime_formatter(d1)}?'

    def generate_answer(self, values):
        time_difference = values[0] - values[1]
        minutes_difference = int(time_difference.total_seconds() / 60)
        return minutes_difference


@generator
# generate factored form (ax + b)(cx+d) -> x intercepts are -b/a and -d/c; A = ac, B = ad + bc, C = bd
class QuadraticZerosGen(QuestionGenerator):
    def generate_value(self):
        return [random.randint(-3, 6), random.randint(0, 6), random.randint(-3, 6), random.randint(1, 8)]

    def generate_text(self, values):
        a, b, c, d = values
        return f'What is one of the x-intercepts of {a * c}x² {"+" if a * d + b * c >= 0 else "-"} {abs(a * d + b * c)}x {"+" if b * d >= 0 else "-"} {b * d}'

    def generate_answer(self, values):
        a, b, c, d = values
        try:
            return Fraction(-b, a)
        except ZeroDivisionError:
            try:
                return Fraction(-d, c)
            except ZeroDivisionError:
                return "No Solutions"


@generator
# generate (i1, i2), m1 = a/b, m2 = c/d -> Line1: m = m1, b = -m1i1+i2, Line2: m = m2, b = -m2i1 + i2
class IntersectingLinesGen(QuestionGenerator):
    def generate_value(self):
        return [random.randint(-50, 50), random.randint(-50, 50), random.randint(-10, 10) / random.randint(1, 10),
                random.randint(-10, 10) / random.randint(1, 10)]

    def generate_text(self, values):
        i1, i2, m1, m2 = values
        b1 = Fraction(-m1 * i1 + i2).limit_denominator()
        b2 = Fraction(-m2 * i1 + i2).limit_denominator()

        return f'What is the intersection of the lines y = {Fraction(m1).limit_denominator()}x {"+" if b1 >= 0 else "-"} {abs(b1)} and y = {Fraction(m2).limit_denominator()}x {"+" if b2 >= 0 else "-"} {abs(b2)}?'

    def generate_answer(self, values):
        return f'({values[0]}, {values[1]})'


@generator
class SimpleAdditionSubtractionThreeTerms(QuestionGenerator):
    def generate_text(self, values):
        return f'What is {values[0]} + {values[1]} - {values[2]}?'

    def generate_answer(self, values):
        return values[0] + values[1] - values[2]

    def generate_value(self):
        return [random.randint(1, 1000000), random.randint(1, 1000000), random.randint(1, 1000000)]


@generator
# a1:coefficient, a2: distance - > a1(a2(a2+1)/2) for sum of first a2 terms
class RepeatingSummation(QuestionGenerator):
    def generate_value(self):
        return [random.randint(1, 8), random.randint(1, 90)]

    def generate_text(self, values):
        return f'What is the sum of the first {values[1]} terms of the sequence {values[0]} + {values[0] * 2} + {values[0] * 3} + ...?'

    def generate_answer(self, values):
        return int(values[0] * (values[1] * (values[1] + 1) / 2))

@generator
class BaseAddition(QuestionGenerator):
    def generate_value(self):
        base1 = random.randint(2, 10)
        x = [str(random.randint(0, base1 - 1)) for _ in range(2)]
        y = [str(random.randint(0, base1 - 1)) for _ in range(2)]

        return [base1, ''.join(x),  ''.join(y)]

    def generate_text(self, values):
        return f'What is {values[1]}(base {values[0]}) + {values[2]}(base {values[0]}) in base {values[0]}?'

    def generate_answer(self, values):
        carry = 0
        answer = []
        for i in range(len(values[1]) - 1, -1, -1):
            if int(values[1][i]) + int(values[2][i]) + carry >= values[0]:
                carry = floor((int(values[1][i]) + int(values[2][i]) + carry) / values[0])
                answer.append(str(int(values[1][i]) + int(values[2][i]) - carry*int(values[0])))
            else:
                carry = 0
                answer.append(str(int(values[1][i]) + int(values[2][i]) - carry*int(values[0])))
        answer.append(str(carry))
        answer.reverse()
        return ''.join(answer)

@generator
class Percentage(QuestionGenerator):
    def generate_value(self):
        return [random.randint(10, 20) * 5, random.randint(1, 70) * 5, random.randint(1, 10) * 5]

    def generate_text(self, values):
        return f'{values[0]}% of {values[1]} is {values[2]}% of ____'

    def generate_answer(self, values):
        return int((values[0] * values[1]) / values[2])


@generator
class CubeOfSquare(QuestionGenerator):
    def generate_value(self):
        return [random.randint(5, 10)]

    def generate_text(self, values):
        return f'If the edge of the cube is {values[0]} units, what is the volume of the cube?'

    def generate_answer(self, values):
        return int(values[0] ** 3)


@generator
class PercentOff(QuestionGenerator):

    def generate_value(self):
        return [random.randint(1, 25) * 4, random.randint(20, 80) * 5]

    def generate_text(self, values):
        return (f'Long bought a phone that was on sale for {values[0]}% off the original price. If the original price '
                f'of the phone was ${values[1]}.00, how much did he save?')

    def generate_answer(self, values):
        return "{:.2f}".format(float((values[0] * values[1]) / 100))


@generator
class PointSlopeForm(QuestionGenerator):
    def generate_value(self):
        return [random.randint(-10, 10), random.randint(-10, 10), random.randint(-5, 5)]

    def generate_text(self, values):
        return (f'Which is an equation for the line passing through the point ({values[0]}, {values[1]}) and having a '
                f'slope of {values[2]}?')

    def generate_answer(self, values):
        answer = (values[0] * -1) * values[2] + values[1] * -1
        answer = str(answer)
        if answer == 0:
            answer = ""
        if "-" not in answer:
            answer = "+ " + answer
        return f'y = {values[2]}x {answer}'