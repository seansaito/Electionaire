import json, os

class Candidate(object):

    def __init__(self, answers, name):
        self.answers = answers
        self.name = name

    def get_json(self):
        dict_summary = {"answers": self.answers, "name": self.name}
        return json.jsonify(dict_summary)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CandidateMatcher():
    # CandidateMatcher should be a Singleton class for sake of efficiency
    __metaclass__ = Singleton

    def __init__(self, num_questions):
        self.candidates = {
            "dog": Candidate([(1, 4), (2, 3), (3, 0)], "dog"),
            "cat": Candidate([(1, 0), (2, 1), (3, 4)], "cat"),
            "human": Candidate([(1, 2), (2, 2), (2, 2)], "human")
        }
        self.num_questions = num_questions

    def get_answer(self, candidate, index):
        return self.candidates[candidate].answers[index][1]

    def get_match(self, request_form):
        deviation = {key: 0 for key in self.candidates.keys()}
        for i in range(1, self.num_questions + 1):
            answer_index = i - 1 # offset for array of answers
            result = request_form.getlist(str(i))

            # If the length of the result is not 2, or in other words,
            # the user did not answer the question, skp it.
            if len(result) != 2:
                continue

            # Unpack result
            importance, user_choice = result

            for candidate in self.candidates.keys():
                deviation[candidate] += int(importance) * abs(self.get_answer(candidate, answer_index) - int(user_choice))
        # End loop
        least_deviation = deviation.keys()[0]
        for candidate in deviation.keys():
            if deviation[candidate] < deviation[least_deviation]:
                least_deviation = candidate
        return least_deviation
