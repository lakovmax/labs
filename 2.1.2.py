def combination2(candidates, target):
    result = []
    candidates.sort()

    def backtrack(combination, remaining, start):
        if remaining == 0:
            result.append(combination.copy())
            return

        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            combination.append(candidates[i])
            backtrack(combination, remaining - candidates[i], i + 1)
            combination.pop()

    backtrack([], target, 0)
    return result

candidates = [10, 1, 2, 7, 6, 1, 5]
target = 8
combinations = combination2(candidates, target)
print(combinations)