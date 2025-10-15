import random

with open("research_papers.txt", "w") as f:
    for i in range(100, 11000):  # 10,000 papers
        features = [str(random.randint(1, 10)) for _ in range(8)]
        f.write(f"{i}: {' '.join(features)}\n")
