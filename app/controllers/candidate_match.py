import json, os
from collections import OrderedDict

class Candidate(object):

    def __init__(self, answers, name, short):
        self.answers = answers
        self.name = name
        self.short = short
        self.max_deviation = 0
        self.min_deviation = 0

    def get_summary(self):
        summary =  {"answers": self.answers,
                    "name": self.name,
                    "short": self.short,
                    "max_deviation": self.max_deviation,
                    "min_deviation": self.min_deviation}
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
            "PAP": Candidate([(1,0.5),(2,0.5),(3,1),(4,0.5),(5,0.25),(6,0),(7,1.75),(8,0),(9,0),(10,1.25),(11,2.25),(12,3),(13,0.5),(14,0), (15,0.25)], "PAP (People's Action Party)", "PAP"),
            "SingFirst": Candidate([(1,3.5),(2,2.75),(3,2.25),(4,3.75),(5,4),(6,3),(7,2),(8,4),(9,2.25),(10,3.25),(11,3.75),(12,2.75),(13,3.75),(14,""),(15,3.75)], "SingFirst (Singaporeans First)", "SingFirst"),
            "SDA": Candidate([(1,2.5),(2,2.75),(3,3.75),(4,3.5),(5,""),(6,0),(7,3),(8,3),(9,4),(10,4),(11,3.333333333),(12,""),(13,3.75),(14,""),(15,"")], "SDA (Singapore Democratic Alliance)", "SDA"),
            "WP": Candidate([(1,3.75),(2,3),(3,2.5),(4,3.5),(5,1.333333333),(6,3.5),(7,3),(8,3),(9,3),(10,3),(11,3.75),(12,3.5),(13,3),(14,3.75),(15,4)], "WP (Worker's Party)", "WP"),
            "SDP": Candidate([(1,3.25),(2,2),(3,3.5),(4,4),(5,4),(6,4),(7,3.25),(8,4),(9,3.5),(10,3.75),(11,4),(12,3.75),(13,4),(14,4), (15,4)], "SDP (Singapore Democratic Party)", "SDP"),
            "DPP": Candidate([(1,2.5),(2,2.5),(3,3.75),(4,3.5),(5,1.25),(6,3),(7,3),(8,1.5),(9,2.25),(10,3),(11,3.5),(12,3),(13,2.75),(14,""), (15,4)], "DPP (Democratic Progressive Party)", "DPP"),
            "NSP": Candidate([(1,3.5),(2,3.5),(3,3.25),(4,3),(5,2.25),(6,4),(7,1.5),(8,2.25),(9,2.25),(10,3.333333333),(11,3.75),(12,3.5),(13,2.75),(14,""),(15,3.5)], "NSP (National Solidarity Party)", "NSP"),
            "RP": Candidate([(1,3),(2,3.75),(3,3),(4,3.5),(5,4),(6,3.75),(7,3.75),(8,4),(9,4),(10,3),(11,3),(12,2),(13,4),(14,""), (15,3.25)], "RP (Reform Party)", "RP"),
            "SPP": Candidate([(1,3.5),(2,2.5),(3,2.5),(4,2.75),(5,""),(6,3.75),(7,3),(8,2.25),(9,2.5),(10,2.75),(11,2.75),(12,3.75),(13,3.5),(14,""),(15,2.75)], "SPP (Singapore People's Party)", "SPP"),
            "PPP": Candidate([(1,2.25),(2,3.25),(3,3.25),(4,3.25),(5,""),(6,3.75),(7,""),(8,3.333333333),(9,4),(10,3),(11,2.5),(12,""),(13,3.25),(14,""),(15,2.75)], "PPP (People's Power Party)", "PPP")
        }
        self.num_questions = num_questions
        for candidate in self.candidates:
            self.candidates[candidate].max_deviation, self.candidates[candidate].min_deviation = self.calculate_maxmindeviation(self.candidates[candidate])

    def calculate_maxmindeviation(self, candidate):
        max_deviation = 0
        min_deviation = 0
        for answer in candidate.answers:
            if answer[1] != "":
                max_deviation += 5 * max(4 - answer[1], answer[1] - 0)
                min_deviation += 1 * min(4 - answer[1], answer[1] - 0)
            else:
                max_deviation += 5 * 2
                min_deviation += 1 * 2
        return max_deviation, min_deviation

    def get_answer(self, candidate, index):
        return self.candidates[candidate].answers[index][1]

    def get_match(self, request_form):
        deviation = {key: {"act_difference": 0, "max_deviation": 0} for key in self.candidates.keys()}

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
                    deviation[candidate]["act_difference"] += abs(candidate_answer - int(user_choice))
                    deviation[candidate]["max_deviation"] += 4 * int(importance)
                    # deviation[candidate] += int(importance) * abs(candidate_answer - int(user_choice)) / (self.candidates[candidate].max_deviation - self.candidates[candidate].min_deviation) * 100
                else:
                    deviation[candidate]["act_difference"] += abs(2 - int(user_choice))
                    deviation[candidate]["max_deviation"] += 4 * int(importance)
                    # deviation[candidate] += int(importance) * abs(2 - int(user_choice)) / (self.candidates[candidate].max_deviation - self.candidates[candidate].min_deviation) * 100
        # End loop

        least_deviation = deviation.keys()[0]
        for candidate in deviation.keys():
            try:
                deviation[candidate]["percentage"] = deviation[candidate]["act_difference"] / deviation[candidate]["max_deviation"] * 100
            except ZeroDivisionError:
                deviation[candidate]["percentage"] = 100.0

        sorted_deviation = OrderedDict(sorted(deviation.iteritems(), key=lambda x: x[1]["percentage"])).items()

        to_return = []
        for result in sorted_deviation:
            candidate, deviation = result
            summary = self.candidates[candidate].get_summary()
            summary["deviation"] = 100 - deviation["percentage"]
            to_return.append(summary)

        return self.candidates[least_deviation].get_summary(), to_return
