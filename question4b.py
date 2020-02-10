def getPrereqs():
    with open("data-4b/relations.txt", "r") as f:
        with open("data-4b/task_ids.txt", "r") as file:
            lines = f.read().splitlines()
            tasks = file.readline().split(",")
            prereqs = {}

            for task in tasks:
                prereqs[task] = []

            for line in lines:
                line = line.split("->")
                prereqs[line[1]] += [line[0]]
            return prereqs


def getStartAndEnd():
    with open("data-4b/question.txt") as f:
        start = f.readline().split()[-1].split(",")
        end = f.readline().split()[-1]
        return start, end


class Pipeline:
    def __init__(self):
        self.prereqs = getPrereqs()
        self.start, self.end = getStartAndEnd()
        self.lst = []

    def solve(self, val=None):
        if val is None:
            val = self.end
        elif val in self.lst:
            return

        if val not in self.start:
            for prereq in self.prereqs[val]:
                self.solve(prereq)

        self.lst.append(val)
        return self.lst


pipeline = Pipeline()
listOfTasks = pipeline.solve()
print(listOfTasks)

# writes answer to txt file
with open("answers/task_list.txt", "w+") as f:
    f.write(",".join(listOfTasks))
