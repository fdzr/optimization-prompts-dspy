import pandas as pd
from sklearn.model_selection import train_test_split
import argparse


def lexical_split(
    input_csv: str,
    train_out: str,
    dev_out: str,
    dev_ratio=0.2,
    seed=42,
):
    """
    Perform lexical split by lemma: ensures lemmas in train/dev are disjoint.
    """

    data = pd.read_csv(input_csv)
    if "lemma" not in data.columns:
        raise ValueError("Input CSV must contain a 'lemma' column.")

    lemmas = data["lemma"].unique()

    train_lemmas, dev_lemmas = train_test_split(
        lemmas, test_size=dev_ratio, random_state=seed
    )

    train_data = data[data["lemma"].isin(train_lemmas)]
    dev_data = data[data["lemma"].isin(dev_lemmas)]

    train_data.to_csv(train_out, index=False)
    dev_data.to_csv(dev_out, index=False)

    print(f"Lexical split done:")
    print(f"  Train: {len(train_data)} examples, {len(train_lemmas)} lemmas")
    print(f"  Dev:   {len(dev_data)} examples, {len(dev_lemmas)} lemmas")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lexical split by lemma (train/dev only)"
    )
    parser.add_argument(
        "--input", required=True, help="Input dataset CSV with 'lemma' column"
    )
    parser.add_argument(
        "--train-out", default="train_split.csv", help="Output train CSV"
    )
    parser.add_argument("--dev-out", default="dev_split.csv", help="Output dev CSV")
    parser.add_argument(
        "--train-ratio", type=float, default=0.8, help="Train split ratio"
    )
    parser.add_argument("--dev-ratio", type=float, default=0.2, help="Dev split ratio")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    lexical_split(
        args.input,
        args.train_out,
        args.dev_out,
        args.dev_ratio,
    )
