#!/bin/python

import numpy as np
import pandas as pd
from tqdm import tqdm

from constants import MIN_DAYSAHEAD, MAX_DAYSAHEAD
from grid_definition import define_grid


def main():
    # Search for minimum score
    scores = {}

    for k, method, delta_window, daysahead, tag in tqdm(define_grid()):
        if tag not in scores:
            scores[tag] = 0

        scores[tag] +=  get_score(0, tag, daysahead)

    I = np.argsort(list(scores.values()))
    sorted_tags = np.array(list(scores.keys()))[I]
    sorted_scores = np.array(list(scores.values()))[I]
    df_rows = []

    for i, (tag, score) in enumerate(zip(sorted_tags, sorted_scores)):
        df_rows.append(
            [
                i,
                score,
                tag
            ]
        )

    df = pd.DataFrame(df_rows, columns=["Rank", "Score", "Tag"])
    print(df.to_string(index=0))


def get_score(real, tag, daysahead):
    percentiles_path = (
        f"data/processed/{tag}/percentiles_daysahead{daysahead}_R{real:03d}.csv"
    )
    df = pd.read_csv(percentiles_path)

    percentiles_true = np.array(df["TruePercentile"].tolist() + [100])
    score = 0

    percentiles_pred = np.array(df["ObservedPercentile"].tolist() + [100])
    score += np.trapezoid(np.abs(percentiles_true - percentiles_pred), percentiles_true)

    return score


if __name__ == "__main__":
    main()
