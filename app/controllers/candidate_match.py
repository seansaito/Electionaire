import json, os
from collections import OrderedDict

"""
Candidate object that stores information, including issue positions
"""
class Candidate(object):

    def __init__(self, answers, name, short):
        self.answers = answers
        self.name = name
        self.short = short

    def get_summary(self):
        summary =  {"answers": self.answers,
                    "name": self.name,
                    "short": self.short}
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
            "PAP": Candidate([(1,0.5),(2,0.5),(3,1),(4,0.5),(5,0.25),(6,0),(7,1.75),(8,0),(9,0),(10,1.5),(11,2.25),(12,3),(13,0.5),(14,0), (15,0.25)], "PAP (People's Action Party)", "PAP"),
            "SingFirst": Candidate([(1,3.5),(2,2.75),(3,2.25),(4,3.75),(5,4),(6,3),(7,2),(8,4),(9,2.25),(10,3.5),(11,3.75),(12,2.75),(13,3.75),(14,""),(15,3.75)], "SingFirst (Singaporeans First)", "SingFirst"),
            "SDA": Candidate([(1,2.5),(2,2.75),(3,3.75),(4,3.5),(5,""),(6,0),(7,3),(8,3),(9,4),(10,2.5),(11,3.333333333),(12,""),(13,3.75),(14,""),(15,"")], "SDA (Singapore Democratic Alliance)", "SDA"),
            "WP": Candidate([(1,3.75),(2,3),(3,2.5),(4,3.5),(5,1.333333333),(6,3.5),(7,3),(8,3),(9,3),(10,3.5),(11,3.75),(12,3.5),(13,3),(14,3.75),(15,4)], "WP (Worker's Party)", "WP"),
            "SDP": Candidate([(1,3.25),(2,2),(3,3.5),(4,4),(5,4),(6,4),(7,3.25),(8,4),(9,3.5),(10,4),(11,4),(12,3.75),(13,4),(14,4), (15,4)], "SDP (Singapore Democratic Party)", "SDP"),
            "DPP": Candidate([(1,2.5),(2,2.5),(3,3.75),(4,3.5),(5,1.25),(6,3),(7,3),(8,1.5),(9,2.25),(10,2),(11,3.5),(12,3),(13,2.75),(14,""), (15,4)], "DPP (Democratic Progressive Party)", "DPP"),
            "NSP": Candidate([(1,3.5),(2,3.5),(3,3.25),(4,3),(5,2.25),(6,4),(7,1.5),(8,2.25),(9,2.25),(10,3.5),(11,3.75),(12,3.5),(13,2.75),(14,""),(15,3.5)], "NSP (National Solidarity Party)", "NSP"),
            "RP": Candidate([(1,3),(2,3.75),(3,3),(4,3.5),(5,4),(6,3.75),(7,3.75),(8,4),(9,4),(10,4),(11,3),(12,2),(13,4),(14,""), (15,3.25)], "RP (Reform Party)", "RP"),
            "SPP": Candidate([(1,3.5),(2,2.5),(3,2.5),(4,2.75),(5,""),(6,3.75),(7,3),(8,2.25),(9,2.5),(10,2),(11,2.75),(12,3.75),(13,3.5),(14,""),(15,2.75)], "SPP (Singapore People's Party)", "SPP"),
            "PPP": Candidate([(1,2.25),(2,3.25),(3,3.25),(4,3.25),(5,""),(6,3.75),(7,""),(8,3.333333333),(9,4),(10,4),(11,2.5),(12,""),(13,3.25),(14,""),(15,2.75)], "PPP (People's Power Party)", "PPP")
        }
        self.num_questions = num_questions

    def get_answer(self, candidate, index):
        return self.candidates[candidate].answers[index][1]

    def get_match(self, request_form):
        deviation = {key: {"act_difference": 0, "max_deviation": 0} for key in self.candidates.keys()}

        # Loop through questions from request_form
        for i in range(1, self.num_questions + 1):
            answer_index = i - 1 # offset for array of answers
            result = request_form.getlist(str(i)) # get the user's response for the particular question index

            # If the length of the result is not 2, or in other words,
            # the user did not answer the question, skp it.
            if len(result) != 2:
                continue

            # Unpack result
            importance, user_choice = result

            for candidate in self.candidates.keys():
                candidate_answer = self.get_answer(candidate, answer_index)
                """
                If the party does not have an answer, then candidate_answer is set to 2
                """
                if candidate_answer != "":
                    deviation[candidate]["act_difference"] += int(importance) * abs(candidate_answer - int(user_choice))
                    deviation[candidate]["max_deviation"] += max((4 - candidate_answer), (candidate_answer - 0)) * int(importance)
                else:
                    deviation[candidate]["act_difference"] += abs(2 - int(user_choice)) * int(importance)
                    deviation[candidate]["max_deviation"] += 2 * int(importance)
        # End loop

        for candidate in deviation.keys():
            try:
                deviation[candidate]["percentage"] = deviation[candidate]["act_difference"] * 100.0 / deviation[candidate]["max_deviation"]
            except ZeroDivisionError: # This happens when the user answers zero questions
                deviation[candidate]["percentage"] = 100.0

        sorted_deviation = OrderedDict(sorted(deviation.iteritems(), key=lambda x: x[1]["percentage"])).items()

        to_return = []
        for result in sorted_deviation:
            candidate, deviation = result
            summary = self.candidates[candidate].get_summary()
            summary["deviation"] = 100 - deviation["percentage"]
            to_return.append(summary)

        return  to_return
