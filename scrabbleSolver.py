minWordLength = 3

def canSpell(letters, word):
    word = list(word)

    for letter in letters:
        if len(word) == 0:
            return True
        elif letter in word:
            word.remove(letter)

    return len(word) == 0

def solve(letters):
    result = []
    with open('engmix.txt', 'r') as dictionary:
        for line in dictionary:
            word = line.strip()
            if len(word) < minWordLength:
                continue
            if canSpell(letters, word):
                result.append(word)

    result = sorted(result, key=lambda w: len(w))

    #for word in result:
    #    print(word)

    return result