import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

omp_csvfile = "../data/csv/OMPtime.csv"
ompWEAK_csvfile = "../data/csv/OMPtime_weakscaling.csv"
seq_csvfile = "../data/csv/SEQtime.csv"
mpi_csvfile = "../data/csv/MPItime.csv"
mpiWEAK_csvfile = "../data/csv/MPItime_weakscaling.csv"

def process_csv(filename):
    data = pd.read_csv(filename, delimiter=';')

    if  filename == "../data/csv/OMPtime.csv":
        data_avg = data.groupby(['n_threads', 'mPow_size'], as_index=False)['time(s)'].mean()
        n_threads = data_avg['n_threads']

    elif filename == "../data/csv/MPItime.csv":
        data_avg = data.groupby(['n_procs', 'mPow_size'], as_index=False)['time(s)'].mean()
        n_threads = data_avg['n_procs']

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
    plt.figure(figsize=(10, 6))

    # Loop through each matrix size and plot the time vs. n_threads
    matrix_sizes = df_avg['mPow_size'].unique()
    for matrix_size in matrix_sizes:
        subset = df_avg[df_avg['mPow_size'] == matrix_size]
        plt.plot(subset['n_threads'], subset['time(s)'], marker='o', linestyle='-',label=f"Matrix Size {matrix_size}")
        plt.xticks(subset['n_threads'])

    plt.xlabel('Number of Threads (n_threads)')

    plt.ylabel('Time (s)')
    plt.yscale('log')
    plt.legend()
    plt.title('[M1]Time vs. Number of Threads for Different Matrix Sizes')
    plt.legend(title='Matrix Sizes')

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'../data/graphs/omp_comparison1.png')
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
    plt.title('[M1]Time vs. Matrix Sizes for Different Threads (avg of 5 runs)')
    plt.legend(title='Thread configuration')

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'../data/graphs/omp_comparison2.png')
    plt.show()

def plot_mpi_comparison1(filename):
    df = pd.read_csv(filename, delimiter=";")
    df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Create a figure and axis for the plot
    plt.figure(figsize=(10, 6))

    # Loop through each matrix size and plot the time vs. n_threads
    matrix_sizes = df_avg['mPow_size'].unique()
    for matrix_size in matrix_sizes:
        subset = df_avg[df_avg['mPow_size'] == matrix_size]
        plt.plot(subset['n_procs'], subset['time(s)'], marker='o', linestyle='-',label=f"Matrix Size {matrix_size}")
        plt.xticks(subset['n_procs'])

    plt.xlabel('Number of Processors (n_procs)')

    plt.ylabel('Time (s)')
    plt.yscale('log')
    plt.legend()
    plt.title('[M1]Time vs. Number of Processors for Different Matrix Sizes')
    plt.legend(title='Matrix Sizes')

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'../data/graphs/mpi_comparison1.png')
    plt.show()

def plot_mpi_comparison2(filename):
        df = pd.read_csv(filename, delimiter=";")
        df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

        # Create a figure and axis for the plot
        plt.figure(figsize=(8, 6))

        # Loop through each matrix size and plot the time vs. n_threads
        n_threads = df_avg['n_procs'].unique()
        for thread in n_threads:
            subset = df_avg[df_avg['n_procs'] == thread]
            plt.plot(subset['mPow_size'], subset['time(s)'], marker='o', linestyle='-', label=f"n_procs {thread}")

        plt.xlabel('Matrix size pow (2^n)')

        plt.ylabel('log Time (s)')
        plt.yscale('log')
        plt.title('[M1]Time vs. Matrix Sizes for Different N_Processors (avg of 5 runs)')
        plt.legend(title='N_Procs configuration')

        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.savefig(f'../data/graphs/mpi_comparison2.png')
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
    plt.title('[M1]Speedup Comparison for Different Thread configurations (avg of 5 runs)')
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
    plt.title('[M1]Efficiency Comparison for Different Thread configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/omp_efficiency_comparison.png')
    plt.show()

def plot_mpi_performance_comparison(filename):
    # Read the CSV file directly
    df = pd.read_csv(filename, delimiter=';')
    df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

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
        subset_threads = subset['n_procs']

        if len(subset_time) > 0 and subset_time.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time.iloc[0]
            speedup = [T1 / t for t in subset_time]
            speedup_data[msize] = speedup

            # Calculate efficiency
            efficiency = [(S / p) * 100 for S, p in zip(speedup, subset_threads)]
            efficiency_data[msize] = efficiency
        else:
            print(f"Warning: No data found for matrix size 2^{msize} with n_procs = 1")



    # Plot Speedup vs Threads for all matrix sizes
    plt.figure(figsize=(8, 6))

    # Plot ideal speedup line
    # plt.plot(subset_threads, subset_threads, linestyle='--', color = 'black', label=f"Ideal speedup")

    #Plot Speedup vs NThreads for all matrix sizes
    for msize in speedup_data:
        plt.plot(subset_threads, speedup_data[msize], marker='o', linestyle='-', label=f"Matrix Size 2^{msize}")
        plt.xticks(subset_threads)

    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup')
    plt.title('[M1]Speedup Comparison for Different N_Processes configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper left', bbox_to_anchor=(0, 1), prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_speedup_comparison.png')
    plt.show()

    # Plot Efficiency vs NThreads for all matrix sizes
    plt.figure(figsize=(8, 6))
    for msize in efficiency_data:
        plt.plot(subset_threads, efficiency_data[msize], marker='o', linestyle='-', label=f"Matrix Size 2^{msize}")
        plt.xticks(subset_threads)

    plt.xlabel('log2 Number of Processes')
    plt.xscale('log', base=2)
    plt.ylabel('Efficiency (%)')
    plt.yscale('linear')
    plt.title('[M1]Efficiency Comparison for Different N_Processes configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_efficiency_comparison.png')
    plt.show()

def plot_mpi_omp_performance_comparison(mpifile, ompfile):
    # Read the CSV file directly
    df = pd.read_csv(mpifile, delimiter=';')
    df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df2 = pd.read_csv(ompfile, delimiter=';')
    df2_avg = df2.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Initialize dictionaries to store speedup and efficiency for each matrix size
    speedup_data = {}
    efficiency_data = {}

    speedup_data2 = {}
    efficiency_data2 = {}

    # Loop through each unique matrix size
    matrix_sizes = df_avg['mPow_size'].unique()
    matrix_sizes2 = df2_avg['mPow_size'].unique()

    # Calculate speedup and efficiency for each matrix size
    for msize in matrix_sizes:
        # Filter data for the current matrix size
        subset = df_avg[df_avg['mPow_size'] == msize]

        # Ensure there's data for n_threads = 1 to calculate speedup
        subset_time = subset['time(s)']
        subset_threads = subset['n_procs']

        if len(subset_time) > 0 and subset_time.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time.iloc[0]
            speedup = [T1 / t for t in subset_time]
            speedup_data[msize] = speedup

            # Calculate efficiency
            efficiency = [(S / p) * 100 for S, p in zip(speedup, subset_threads)]
            efficiency_data[msize] = efficiency
        else:
            print(f"Warning: No data found for matrix size 2^{msize} with n_procs = 1")

    for msize2 in matrix_sizes2:
        # Filter data for the current matrix size
        subset2 = df2_avg[df2_avg['mPow_size'] == msize2]

        # Ensure there's data for n_threads = 1 to calculate speedup
        subset_time2 = subset2['time(s)']
        subset_threads2 = subset2['n_threads']

        if len(subset_time2) > 0 and subset_time2.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1_O = subset_time2.iloc[0]
            speedup2 = [T1_O / t for t in subset_time2]
            speedup_data2[msize2] = speedup2

            # Calculate efficiency
            efficiency2 = [(S / p) * 100 for S, p in zip(speedup2, subset_threads2)]
            efficiency_data2[msize2] = efficiency2
        else:
            print(f"Warning: No data found for matrix size 2^{msize2} with n_threads = 1")



    # Plot Speedup vs Threads for all matrix sizes
    plt.figure(figsize=(8, 6))

    # Plot ideal speedup line
    # plt.plot(subset_threads, subset_threads, linestyle='--', color = 'black', label=f"Ideal speedup")

    #Plot Speedup vs NThreads for all matrix sizes
    for msize in speedup_data:
        plt.plot(subset_threads, speedup_data[msize], marker='o', linestyle='-', label=f"Matrix Size 2^{msize} [MPI]")
        plt.xticks(subset_threads)

    for msize2 in speedup_data2:
        plt.plot(subset_threads2, speedup_data2[msize2], marker='o', linestyle='-', label=f"Matrix Size 2^{msize2} [OMP]")

    plt.xlabel('Number of Processes/Threads')
    plt.ylabel('Speedup')
    plt.title('[M1]Speedup Comparison for Different N_Processes configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper left', bbox_to_anchor=(0, 1), prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_omp_speedup_comparison.png')
    plt.show()

    # Plot Efficiency vs NThreads for all matrix sizes
    plt.figure(figsize=(8, 6))
    for msize in efficiency_data:
        plt.plot(subset_threads, efficiency_data[msize], marker='o', linestyle='-', label=f"Matrix Size 2^{msize} [MPI]")
        plt.xticks(subset_threads)

    for msize2 in efficiency_data2:
        plt.plot(subset_threads2, efficiency_data2[msize2], marker='o', linestyle='-', label=f"Matrix Size 2^{msize2} [OMP]")


    plt.xlabel('log2 Number of Processes/Threads')
    plt.xscale('log', base=2)
    plt.ylabel('Efficiency (%)')
    plt.yscale('linear')
    plt.title('[M1]Efficiency Comparison for Different N_Processes configurations (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_omp_efficiency_comparison.png')
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
    plt.title(f'[M1]Speedup vs Threads for Matrix of Size 2^{mPow_size}')
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
    plt.title(f'[M1]Efficiency vs Threads for Matrix of Size 2^{mPow_size}')
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
        plt.title('[M1]Time vs Matrix Size (2^n) Sequential execution')
        plt.savefig(f'../data/graphs/seq_performance.png')
    else: #implicit
        plt.title('[M1]Time vs Matrix Size (2^n) Implicit execution')
        plt.savefig(f'../data/graphs/imp_performance.png')
    plt.show()


def plot_mpi_comparison1BAR(filename):
    # Load and process data
    df = pd.read_csv(filename, delimiter=";")
    df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Unique values
    matrix_sizes = df_avg['mPow_size'].unique()
    n_procs = df_avg['n_procs'].unique()

    # Set up positions and bar width
    bar_width = 0.2
    x_positions = np.arange(len(n_procs))

    # Create the figure
    plt.figure(figsize=(12, 6))

    # Loop through matrix sizes and create bar plots
    for i, matrix_size in enumerate(matrix_sizes):
        subset = df_avg[df_avg['mPow_size'] == matrix_size]

        # Match positions of `n_procs` with `subset`
        subset_positions = [np.where(n_procs == proc)[0][0] for proc in subset['n_procs']]

        plt.bar(
            np.array(subset_positions) + i * bar_width,  # Adjusted bar positions
            subset['time(s)'],
            width=bar_width,
            label=f"Matrix Size {matrix_size}"
        )

    # Adjust x-axis labels
    plt.xticks(x_positions + (len(matrix_sizes) - 1) * bar_width / 2, n_procs)
    plt.xlabel('Number of Processors (n_procs)')
    plt.ylabel('Time (s)')
    plt.yscale('log')
    plt.title('[M1] Time vs. Number of Processors for Different Matrix Sizes')
    plt.legend(title='Matrix Sizes')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, axis='y')

    # Save and show the graph
    plt.savefig(f'../data/graphs/mpi_comparison1_bar.png')
    plt.show()


def main():
    # plot_omp_comparison1(ompWEAK_csvfile)
    # plot_omp_comparison2(omp_csvfile)
    # plot_omp_performance_comparison(omp_csvfile)
    # plot_seq_imp_performance(*process_csv(seq_csvfile))
    # plot_seq_imp_performance(*process_csv(imp_csvfile))
    # plot_seq_imp_comparison() DEPRECATED
    # plot_imp_optimizations()
    # plot_mpi_comparison1(mpi_csvfile)
    # plot_mpi_comparison1BAR(mpi_csvfile)
    # plot_mpi_comparison2(mpi_csvfile)
    # plot_mpi_performance_comparison(mpi_csvfile)
    # plot_mpi_omp_performance_comparison(mpiWEAK_csvfile, ompWEAK_csvfile)
if __name__ == "__main__":
    main()
