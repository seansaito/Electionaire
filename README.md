# Electionaire
A questionnaire that matches users with a Singapore political party


# Contact Us
Koh Wei Jie
Email: weijie.koh [at] yale-nus.edu.sg

# About Electionaire

## Electionaire is not a poll.
The site does not ask who you plan to vote for. Electionaire compares your opinions on the issues of GE2015 with the policies of Singapore’s 10 political parties, then measures how much you agree with each of them.

## Electionaire is anonymous.
The site does not ask for identifying information, log IP addresses or store cookies. Only you know your responses.

## Electionaire tries to be objective.

The team carefully examined party manifestos and public statements. When choosing issues to highlight, we also considered how many parties care about them. Volunteers from a diverse set of backgrounds and political leanings scored each party’s policies. We do not claim to perfectly represent each party’s positions.

# Methodology
Electionaire matches are merely estimates. We compare your opinions to the perceived stances of the ten parties as gathered by the research team. The research process was conducted as follows:
* The research team formulated a list of questions that highlight election issues multiple political parties have made public statements on.
* The research team examined manifestos and public statements by the political parties to create a set of fifteen issues that were central to the 2015 General Election.
* The research team then collected quotes from each party on each issue. If a clear stance was not explicitly available, the team tried to find a quote on a related topic. If the team could not find a related quote, the team marked the stance as “No mention”. See the spreadsheet [here](https://docs.google.com/spreadsheets/d/1yOqqxOdEF4vVeGnhlMlJXPVSOU_1Iof44XiB6O_T53Q/edit?usp=sharing).
* Multiple raters of varied backgrounds and political leanings used the spreadsheet to score the parties on a scale of 0-4 for their agreement with each question. 0 stood for no, 1 for qualified no, 2 for neutral, 3 for qualified yes, and 4 for yes. See the averaged ratings [here](https://docs.google.com/spreadsheets/d/1GZdSzXNlJh9Xq7zuv0dSfLtOtVaXWtC93wLk_CjlJlI/edit?usp=sharing).

Your answers, which correspond to the same 0-4 scale, are then compared with the parties’ average ratings. The degree of difference between your answers and the parties’ average ratings is then weighted according to the degree of importance you indicated for each question. This deviation is then coerced into a percentage. The exact algorithm is as follows:

> Total Deviation = Sum of (weight of each question as set by user) * (party value - user's value) for questions 1 to 15
> Final Percentage = 100 - total deviation/(max possible total deviation - min possible deviation)

# About Us
Electionaire was created by a group of third-year students at Yale-NUS College. It is not supported, funded or aligned with any political party. Some of us are first-time voters who struggled to find an online resource that collated all parties’ policy stances.

# The Team
Koh Wei Jie - Maggie Schumann - Parag Bhatnagar - Rohan Naidu - Sean Saito
