import random
from abc import ABC, abstractmethod
import warnings
from fpdf import FPDF, XPos, YPos

answer_choices = 5
questions = 25
question_generators = []


def generator(cls):
    question_generators.append(cls())
    return cls

def generate_random_number_excluding(num_to, num_from, exclude):
    num = random.randint(num_to, num_from)
    while num in exclude:
        num = random.randint(num_to, num_from)
    return num

class Question:
    def __init__(self, question, answer_choice_list, correct_index):
        self.question = question
        self.answer_choice_list = answer_choice_list
        self.correct_index = correct_index


class QuestionGenerator(ABC):

    @abstractmethod
    def generate_value(self):
        pass

    @abstractmethod
    def generate_text(self, values):
        pass

    @abstractmethod
    def generate_answer(self, values):
        pass

    def generate_range(self, correct_answer, correct_index):
        answers = []
        try:
            correct_answer = int(correct_answer)
            for i in range(5):
                answers.append(generate_random_number_excluding(correct_answer- 10, correct_answer + 10, answers))
            answers[correct_index] = correct_answer
        except ValueError:
            answers = [self.generate_answer(self.generate_value()) for _ in range(5)]
            answers[correct_index] = correct_answer
            warnings.warn(f'Question generator, {type(self).__name__}, does not have an explicit generate_range method.')
        return answers



    def generate_question(self):
        correct_index = random.randint(0, answer_choices - 1)
        correct_value = self.generate_value()
        correct_answer = self.generate_answer(correct_value)
        question = self.generate_text(correct_value)

        return Question(question, self.generate_range(correct_answer, correct_index), correct_index)


class Quiz:

    def __init__(self, font_family='times', font_size=10, name='quiz'):
        self.font_family = font_family
        self.font_size = font_size
        self.name = name
        self.questions = []
        self.question_number = 1
        self.pdf = FPDF()
        self.pdf.set_font(self.font_family, size=self.font_size)
        self.pdf.add_page()

    def add_question(self, number=1, gen=None):
        for i in range(0, number):
            if gen is None:
                self.questions.append(random.choice(question_generators).generate_question())
            else:
                self.questions.append(gen.generate_question())

    def generate_quiz(self):
        for question in self.questions:
            cell_width = 190
            answers = question.answer_choice_list

            # Add the first block of text and answer choices
            self.pdf.multi_cell(cell_width, 5, f'({self.question_number})          {question.question}',
                                new_x=XPos.LMARGIN,
                                new_y=YPos.NEXT)
            self.pdf.cell(cell_width, 10,
                          f'A) {answers[0]}     B) {answers[1]}     C) {answers[2]}     D) {answers[3]}     E) {answers[4]}',
                          align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(cell_width, 10, f'', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            self.question_number += 1
        self.generate_answer_key()
        self.pdf.output(f'{self.name}.pdf')

    def generate_answer_key(self, z=1, x=10, y=10):
        self.pdf.add_page()
        self.pdf.set_font(size=20)
        self.pdf.cell(200, 10, txt="Math UIL Answer Key", ln=True, align='C')
        self.pdf.set_font(size=10)
        answer_choice = ["A", "B", "C", "D", "E"]

        for questions in self.questions:
            self.pdf.cell(x, y, txt=f"{z}.   {answer_choice[questions.correct_index]}", ln=True)
            z+=1

