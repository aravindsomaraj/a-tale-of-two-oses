with open('scrr.txt','r') as f:
    seen = set()
    for line in f:
        if line in seen:
            print(line)
        else:
            seen.add(line)