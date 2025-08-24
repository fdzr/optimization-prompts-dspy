import pandas as pd
import argparse
import os


def make_dev_subset(
    input_file, output_file, items_per_class=50, class_column="label", random_seed=42
):
    """
    Create a balanced dev subset from a CSV file with fixed items per class.
    If a class has fewer items than required, sample with replacement.
    """
    # Load dev set
    df = pd.read_csv(input_file)

    df = df[df[class_column].isin([1, 2, 3, 4])]
    if df.empty:
        raise ValueError(f"No rows found with {class_column} in [1,2,3,4]")

    if class_column not in df.columns:
        raise ValueError(f"Column '{class_column}' not found in {input_file}")

    # Sample fixed number of items per class (with replacement if needed)
    subset_parts = []
    for label, group in df.groupby(class_column):
        replace = len(group) < items_per_class
        sampled = group.sample(
            n=items_per_class, replace=replace, random_state=random_seed
        )
        subset_parts.append(sampled)

    # Concatenate and shuffle
    subset_df = (
        pd.concat(subset_parts)
        .sample(frac=1, random_state=random_seed)
        .reset_index(drop=True)
    )

    # Save
    # os.makedirs(os.path.dirname(output_file), exist_ok=True)
    subset_df.to_csv(output_file, index=False)

    print(f"Dev subset saved to {output_file}")
    print(subset_df[class_column].value_counts())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a balanced dev subset from an existing dev CSV"
    )
    parser.add_argument("--input", required=True, help="Path to the input dev CSV file")
    parser.add_argument(
        "--output", required=True, help="Path to save the dev subset CSV file"
    )
    parser.add_argument(
        "--items_per_class",
        type=int,
        default=50,
        help="Number of items per class (default: 50)",
    )
    parser.add_argument(
        "--class_column",
        default="label",
        help="Column with class labels (default: 'label')",
    )
    args = parser.parse_args()

    make_dev_subset(args.input, args.output, args.items_per_class, args.class_column)
