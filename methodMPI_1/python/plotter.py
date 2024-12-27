import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

omp_csvfile = "../data/csv/OMPtime.csv"
seq_csvfile = "../data/csv/SEQtime.csv"
imp_csvfile = "../data/csv/IMPtime.csv"

def process_csv(filename):
    data = pd.read_csv(filename, delimiter=';')

    if  filename == "../data/csv/OMPtime.csv":
        data_avg = data.groupby(['n_threads', 'mPow_size'], as_index=False)['time(s)'].mean()
        n_threads = data_avg['n_threads']

    else:
        if filename == "../data/csv/SEQtime.csv":
            n_threads = -1  #-1 stands for sequential execution
        else :
            n_threads = 0  #0 stands for implicit execution

    data_avg = data.groupby('mPow_size', as_index=False)['time(s)'].mean()

    return n_threads, data_avg['time(s)'], data_avg['mPow_size']


def plot_omp_comparison1(filename):
    df = pd.read_csv(filename, delimiter=";")
    df_avg = df.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Create a figure and axis for the plot
    plt.figure(figsize=(8, 6))

    labels = {
        12: "[M1] Naive out-of-place",
        13: "[M2] Triangular in-place",
        14: "[M3] Block-based out-of-place(bs=256)",
    }

    # Loop through each matrix size and plot the time vs. n_threads
    matrix_sizes = df_avg['mPow_size'].unique()
    for matrix_size in matrix_sizes:
        subset = df_avg[df_avg['mPow_size'] == matrix_size]

        label = labels.get(matrix_size, matrix_size)

        plt.plot(subset['n_threads'], subset['time(s)'], marker='o', linestyle='-',label=label)
        plt.xticks(subset['n_threads'])

    plt.xlabel('Number of Threads (n_threads)')

    plt.ylabel('log Time (s)')
    plt.yscale('log')
    plt.legend()
    plt.title('OpenMP comparison between methods n_threads = 64, matrix size = 2^12')
    plt.legend(title='Methods')

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'../data/graphs/omp_methods_comparison.png')
    plt.show()


def plot_omp_comparison2(filename):
    df = pd.read_csv(filename, delimiter=";")
    df_avg = df.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Create a figure and axis for the plot
    plt.figure(figsize=(8, 6))

    # Loop through each matrix size and plot the time vs. n_threads
    n_threads = df_avg['n_threads'].unique()
    for thread in n_threads:
        subset = df_avg[df_avg['n_threads'] == thread]
        plt.plot(subset['mPow_size'], subset['time(s)'], marker='o', linestyle='-',label=f"n_threads {thread}")

    plt.xlabel('Matrix size pow (2^n)')

    plt.ylabel('log Time (s)')
    plt.yscale('log')
    plt.title('[M2]Time vs. Matrix Sizes for Different Threads (avg of 5 runs)')
    plt.legend(title='Thread configuration')

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'../data/graphs/omp_comparison2.png')
    plt.show()


def plot_omp_performance_comparison(filename):
    # Read the CSV file directly
    df = pd.read_csv(filename, delimiter=';')
    df_avg = df.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Initialize dictionaries to store speedup and efficiency for each matrix size
    speedup_data = {}
    efficiency_data = {}

    # Loop through each unique matrix size
    matrix_sizes = df_avg['mPow_size'].unique()

    # Calculate speedup and efficiency for each matrix size
    for msize in matrix_sizes:
        # Filter data for the current matrix size
        subset = df_avg[df_avg['mPow_size'] == msize]

        # Ensure there's data for n_threads = 1 to calculate speedup
        subset_time = subset['time(s)']
        subset_threads = subset['n_threads']

        if len(subset_time) > 0 and subset_time.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time.iloc[0]
            speedup = [T1 / t for t in subset_time]
            speedup_data[msize] = speedup

            # Calculate efficiency
            efficiency = [(S / p) * 100 for S, p in zip(speedup, subset_threads)]
            efficiency_data[msize] = efficiency
        else:
            print(f"Warning: No data found for matrix size 2^{msize} with n_threads = 1")



    # Plot Speedup vs Threads for all matrix sizes
    plt.figure(figsize=(8, 6))

    # Plot ideal speedup line
    # plt.plot(subset_threads, subset_threads, linestyle='--', color = 'black', label=f"Ideal speedup")

    #Plot Speedup vs NThreads for all matrix sizes
    for msize in speedup_data:
        plt.plot(subset_threads, speedup_data[msize], marker='o', linestyle='-', label=f"Matrix Size 2^{msize}")
        plt.xticks(subset_threads)

    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup')
    plt.title('[M2]Speedup Comparison for Different Thread configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper left', bbox_to_anchor=(0, 1), prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/omp_speedup_comparison.png')
    plt.show()

    # Plot Efficiency vs NThreads for all matrix sizes
    plt.figure(figsize=(8, 6))
    for msize in efficiency_data:
        plt.plot(subset_threads, efficiency_data[msize], marker='o', linestyle='-', label=f"Matrix Size 2^{msize}")
        plt.xticks(subset_threads)

    plt.xlabel('log2 Number of Threads')
    plt.xscale('log', base=2)
    plt.ylabel('Efficiency (%)')
    plt.yscale('linear')
    plt.title('[M2]Efficiency Comparison for Different Thread configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/omp_efficiency_comparison.png')
    plt.show()


def plot_omp_performance(n_threads, time, mPow_size):
    T1 = time[0]  #time with a single thread
    mPow_size = mPow_size[0]

    speedup = [T1 / t for t in time]

    #speedup plot
    plt.figure(figsize=(8, 6))
    plt.plot(n_threads, speedup, marker='o', color='b', linestyle='-', label='Speedup vs Threads')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup')
    #plt.yscale("log")
    #plt.xscale("log")
    plt.xticks(n_threads)
    plt.title(f'[M2]Speedup vs Threads for Matrix of Size 2^{mPow_size}')
    plt.legend()
    plt.savefig(f'../data/graphs/omp_speedupS{mPow_size}.png')
    plt.show()

    efficiency = [(S / p) * 100 for S, p in zip(speedup, n_threads)]

    #efficiency plot
    plt.figure(figsize=(8, 6))
    plt.plot(n_threads, efficiency, marker='o', color='r', linestyle='-', label='Efficiency vs Threads')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.xlabel('log2 Number of Threads')
    plt.ylabel('Efficiency (%)')
    plt.xticks(n_threads)
    plt.yticks(efficiency)
    plt.title(f'[M2]Efficiency vs Threads for Matrix of Size 2^{mPow_size}')
    plt.legend()
    plt.savefig(f'../data/graphs/omp_efficiencyS{mPow_size}.png')
    plt.show()


def plot_seq_imp_performance(n_threads, time, mPow_size):

    plt.plot(mPow_size, time, marker='o', color='b', linestyle='-', label='Time vs Matrix Size')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.xlabel('Size of matrix 2^n')
    #plt.xticks(mPow_size)
    plt.ylabel('Time (seconds)')
    plt.yscale("log")

    plt.legend()
    if n_threads == -1: #sequential
        plt.title('[M2]Time vs Matrix Size (2^n) Sequential execution')
        plt.savefig(f'../data/graphs/seq_performance.png')
    else: #implicit
        plt.title('[M2]Time vs Matrix Size (2^n) Implicit execution')
        plt.savefig(f'../data/graphs/imp_performance.png')
    plt.show()


def plot_seq_imp_comparison():
    n_threads, seq_time, mPow_size = process_csv(seq_csvfile)
    imp_time = process_csv(imp_csvfile)[1]

    plt.plot(mPow_size, seq_time, marker='o', color='b', linestyle='-', label='Sequential')
    plt.plot(mPow_size, imp_time, marker='o', color='r', linestyle='-', label='Implicit')

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.xlabel('Size of matrix 2^n')
    #plt.xticks(mPow_size)
    plt.ylabel('Time (seconds)')
    plt.yscale('log')

    plt.legend()
    plt.title('[M2]Time vs Matrix Size (2^n) comparison execution')
    plt.savefig(f'../data/graphs/seq_imp_comparison.png')
    plt.show()

def plot_imp_optimizations():
    path = "../data/csv/"
    n_threads, imp_time, mPow_size = process_csv(imp_csvfile)

    labels = {
        "IMPtime.csv": "No compiler options (Serial)",
        "IMPtime_o1.csv": "-O1 flag",
        "IMPtime_o1_march.csv" : "-O1, -march=native",
        "IMPtime_o2.csv": "-O2 flag",
        "IMPtime_o2_funroll_march.csv": "-O2,-march=native,-funroll-loops",
    }

    plt.figure(figsize=(8, 6))

    for filename in os.listdir(path):
        if "imp" in filename.lower():
            print(filename)
            imp_time = process_csv(f'../data/csv/{filename}')[1]
            label = labels.get(filename, filename)
            plt.plot(mPow_size, imp_time, marker='o', linestyle='-', label=label)

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.xlabel('Size of matrix 2^n')
    # plt.xticks(mPow_size)
    plt.ylabel('log Time (s)')
    plt.yscale('log')

    plt.legend(title='Compiler flags', loc='upper left', prop={'size': 9})
    plt.title('[M2]Time vs Matrix Size (2^n) implicit compare execution')
    plt.savefig(f'../data/graphs/imp_optimizations_compare.png')
    plt.show()


def main():
    # plot_omp_performance(*process_csv(omp_csvfile))
    # plot_omp_comparison1(omp_csvfile)
    # plot_omp_comparison1('../../methodComparisonData/omp1_12.csv')
    plot_omp_comparison2(omp_csvfile)
    plot_omp_performance_comparison(omp_csvfile)
    # plot_seq_imp_performance(*process_csv(seq_csvfile))
    # plot_seq_imp_performance(*process_csv(imp_csvfile))
    # plot_seq_imp_comparison()
    # plot_imp_optimizations()

if __name__ == "__main__":
    main()
