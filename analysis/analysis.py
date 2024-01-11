from os import mkdir, path

import matplotlib.pyplot as plt
import pandas as pd

from config import PLOT_DIR, PLOT_COLORS, PATH_TO_GENERAL_DATA


def create_tech_plot(df):
    df['tech_stack'] = df['tech_stack'].apply(eval)
    flat_tech_stacks = [tech for stack 
                        in df['tech_stack'] for tech in stack]
    tech_counts = pd.Series(flat_tech_stacks).value_counts()

    plt.figure(figsize=(15, 12))
    plt.subplots_adjust(bottom=0.2)

    top_tech = tech_counts.head(20)
    top_tech.plot(kind='bar', color=PLOT_COLORS, edgecolor='black')

    plt.title('Top 10 Technologies')
    plt.xlabel('Technology')
    plt.ylabel('Frequency')
    plt.savefig(path.join(PLOT_DIR, "general_stat"))


def main():
    df = pd.read_csv(PATH_TO_GENERAL_DATA)
    if not path.exists(PLOT_DIR):
        mkdir(PLOT_DIR)
    create_tech_plot(df)


if __name__ == "__main__":
    main()
