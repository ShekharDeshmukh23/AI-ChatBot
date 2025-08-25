from dataclasses import dataclass
from typing import List
from sklearn.linear_model import LogisticRegression
import numpy as np
from .utils import polite_score

@dataclass
class EligibilityModel:
    clf: LogisticRegression

    def featurize(self, messages: List[str]) -> np.ndarray:
        # Simple handcrafted features
        n_turns = len(messages)
        avg_len = np.mean([len(m) for m in messages]) if messages else 0
        politeness = sum(polite_score(m) for m in messages)
        contains_accept = sum(1 for m in messages if "accept the code of conduct" in m.lower())
        return np.array([n_turns, avg_len, politeness, contains_accept]).reshape(1, -1)

    def score(self, messages: List[str]) -> float:
        X = self.featurize(messages)
        proba = self.clf.predict_proba(X)[0,1]
        return float(proba)

def train_toy_model() -> EligibilityModel:
    # Toy training data
    # Features: [n_turns, avg_len, politeness, contains_accept]
    X = np.array([
        [2, 25, 0, 0],   # short, not polite, no accept -> ineligible
        [6, 60, 2, 1],   # longer, polite, accept -> eligible
        [5, 40, 1, 1],   # decent, accept -> eligible
        [3, 15, 0, 0],   # short, nope -> ineligible
        [7, 80, 3, 1],   # very likely eligible
        [4, 30, 0, 1],   # borderline
        [8, 90, 2, 1],   # eligible
        [5, 20, 0, 0]    # ineligible
    ], dtype=float)
    y = np.array([0,1,1,0,1,1,1,0], dtype=int)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)
    return EligibilityModel(clf)
