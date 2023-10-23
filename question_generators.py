import datetime
import random

from util import QuestionGenerator
from fractions import Fraction


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


# generate (i1, i2), m1 = a/b, m2 = c/d -> Line1: m = m1, b = -m1i1+i2, Line2: m = m2, b = -m2i1 + i2
class IntersectingLinesGen(QuestionGenerator):
    def generate_value(self):
        return [random.randint(-50, 50), random.randint(-50, 50), random.randint(-10, 10) / random.randint(1, 10), random.randint(-10, 10) / random.randint(1, 10)]

    def generate_text(self, values):
        i1, i2, m1, m2 = values
        b1 = Fraction(-m1 * i1 + i2).limit_denominator()
        b2 = Fraction(-m2 * i1 + i2).limit_denominator()

        return f'What is the intersection of the lines y = {Fraction(m1).limit_denominator()}x {"+" if b1 >= 0 else "-"} {abs(b1)} and y = {Fraction(m2).limit_denominator()}x {"+" if b2 >= 0 else "-"} {abs(b2)}?'

    def generate_answer(self, values):
        return f'({values[0]}, {values[1]})'

class SimpleAdditionSubtractionThreeTerms(QuestionGenerator):
    def generate_text(self, values):
        return f'What is {values[0]} + {values[1]} - {values[2]}?'

    def generate_answer(self, values):
        return values[0] + values[1] - values[2]

    def generate_value(self):
        return [random.randint(1, 1000000), random.randint(1, 1000000), random.randint(1, 1000000)]


# a1:coefficient, a2: distance - > a1(a2(a2+1)/2) for sum of first a2 terms
class RepeatingSummation(QuestionGenerator):
    def generate_value(self):
        return [random.randint(1, 8), random.randint(1, 90)]

    def generate_text(self, values):
        return f'What is the sum of the first {values[1]} terms of the sequence {values[0]} + {values[0] * 2} + {values[0] * 3} + ...?'

    def generate_answer(self, values):
        return int(values[0] * (values[1] * (values[1] + 1) / 2))