import random
from abc import ABC, abstractmethod
from fpdf import FPDF, XPos, YPos


answer_choices = 5
questions = 25
question_generators = []


def generator(cls):
    question_generators.append(cls())
    return cls


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

    def generate_question(self):
        answers = []
        correct_index = random.randint(0, answer_choices - 1)
        correct_value = self.generate_value()
        question = self.generate_text(correct_value)

        for i in range(0, answer_choices):
            if i == correct_index:
                answers.append(self.generate_answer(correct_value))
            else:
                answers.append(self.generate_answer(self.generate_value()))

        return Question(question, answers, correct_index)


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
            self.pdf.multi_cell(cell_width, 5, f'({self.question_number})          {question.question}', new_x=XPos.LMARGIN,
                           new_y=YPos.NEXT)
            self.pdf.cell(cell_width, 10,
                     f'A) {answers[0]}     B) {answers[1]}     C) {answers[2]}     D) {answers[3]}     E) {answers[4]}',
                     align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(cell_width, 10, f'', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            print(question.correct_index)
            self.question_number += 1
        self.pdf.output(f'{self.name}.pdf')
