import json, os
from collections import OrderedDict

class Candidate(object):

    def __init__(self, answers, name, short):
        self.answers = answers
        self.name = name
        self.short = short

    def get_summary(self):
        summary =  {"answers": self.answers, "name": self.name, "short": self.short}
        return summary

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
            "PAP": Candidate([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 1), (8, 0), (9, 0), (10, 0), (11, 2), (12, 1), (13, 0), (14, 0), (15, 0)], "PAP (People's Action Party)", "PAP"),
            "SG1ST": Candidate([(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 3), (7, 2), (8, 4), (9, 3), (10, 3), (11, 3), (12, 2), (13, 3), (14, ""), (15, 3)], "SG1ST (Singaporeans First)", "SG1ST"),
            "SDA": Candidate([(1, 3), (2, 4), (3, 4), (4, 4), (5, ""), (6, 0), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, ""), (13, 3), (14, ""), (15, "")], "SDA (Singapore Democratic Alliance)", "SDA"),
            "WP": Candidate([(1, 4), (2, 3), (3, 3), (4, 3), (5, 2), (6, 3), (7, 4), (8, 3), (9, 4), (10, 4), (11, 3), (12, 2), (13, 2), (14, 3), (15, 4)], "WP (Worker's Party)", "WP"),
            "SDP": Candidate([(1, 3), (2, 2), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4)], "SDP (Singapore Democratic Party)", "SDP"),
            "DPP": Candidate([(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 2), (9, 2), (10, 3), (11, 4), (12, 2), (13, 3), (14, ""), (15, 3)], "DPP (Democratic Progressive Party)", "DPP"),
            "NSP": Candidate([(1, 4), (2, 4), (3, 3), (4, 4), (5, 2), (6, 4), (7, 1), (8, 3), (9, 3), (10, 4), (11, 3), (12, 3), (13, 3), (14, ""), (15, 3)], "NSP (National Solidarity Party)", "NSP"),
            "RP": Candidate([(1, 2), (2, 4), (3, 2), (4, 3), (5, 4), (6, 4), (7, 3), (8, 4), (9, 4), (10, 3), (11, 4), (12, 3), (13, 4), (14, ""), (15, 4)], "RP (Reform Party)", "RP"),
            "SPP": Candidate([(1, 4), (2, 2), (3, 3), (4, 2), (5, ""), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 2), (12, 4), (13, 4), (14, ""), (15, 3)], "SPP (Singapore People's Party)", "SPP"),
            "PPP": Candidate([(1, 2), (2, 4), (3, 2), (4, 3), (5, ""), (6, 3), (7, ""), (8, ""), (9, ""), (10, 4), (11, 2), (12, ""), (13, 3), (14, ""), (15, 2)], "PPP (People's Power Party)", "PPP")
        }
        self.num_questions = num_questions

    def get_answer(self, candidate, index):
        return self.candidates[candidate].answers[index][1]

    def get_match(self, request_form):
        deviation = {key: 0 for key in self.candidates.keys()}

        # Loop through questions
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
                candidate_answer = self.get_answer(candidate, answer_index)
                # print "%d: %s - %s" % (i, self.candidates[candidate].name, str(candidate_answer))
                if candidate_answer != "":
                    deviation[candidate] += int(importance) * abs(candidate_answer - int(user_choice)) / 10.0
                else:
                    deviation[candidate] += int(importance) * abs(self.get_answer("PAP", answer_index) - int(user_choice)) / 10.0
        # End loop

        least_deviation = deviation.keys()[0]
        for candidate in deviation.keys():
            if deviation[candidate] < deviation[least_deviation]:
                least_deviation = candidate

        sorted_deviation = OrderedDict(sorted(deviation.iteritems(), key=lambda x: x[1])).items()

        to_return = []
        for result in sorted_deviation:
            candidate, deviation = result
            summary = self.candidates[candidate].get_summary()
            summary["deviation"] = deviation
            to_return.append(summary)

        print to_return

        return self.candidates[least_deviation].get_summary(), to_return
