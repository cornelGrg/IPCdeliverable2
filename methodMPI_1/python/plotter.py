import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

omp_csvfile = "../data/csv/OMPtime.csv"
seq_csvfile = "../data/csv/SEQtime.csv"
mpi_csvfile = "../data/csv/MPItime.csv"
seqWEAK_csvfile = "../data/csv/csv_weakscaling/SEQtime.csv"
mpiWEAK_csvfile = "../data/csv/csv_weakscaling/MPItime.csv"
ompWEAK_csvfile = "../data/csv/csv_weakscaling/OMPtime.csv"
mpiSTRONG_csvfile = "../data/csv/csv_strongscaling/MPItime.csv"
ompSTRONG_csvfile = "../data/csv/csv_strongscaling/OMPtime.csv"
seqSTRONG_csvfile = "../data/csv/csv_strongscaling/SEQtime.csv"
comparemethods = "../data/csv/comparemethods.csv"

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

    labels = {
        12: "MPI [M1] Per row divided and gather approach",
        13: "MPI [M2] Scatter local transpose with gather on shared memory",
        14: "MPI [M3] Scatter local transpose with final reduction",
        15: "OMP"
    }


    # Loop through each matrix size and plot the time vs. n_threads
    matrix_sizes = df_avg['mPow_size'].unique()
    for matrix_size in matrix_sizes:
        subset = df_avg[df_avg['mPow_size'] == matrix_size]
        label = labels.get(matrix_size, matrix_size)

        plt.plot(subset['n_threads'], subset['time(s)'], marker='o', linestyle='-',label=label)
        plt.xticks(subset['n_threads'])

    plt.xlabel('Number of Processes/Threads')

    plt.ylabel('Time (s)')
    plt.yscale('log')
    plt.title('Time vs. N_Threads/Processes Comparison with Matrix size 2^12', fontsize=16)
    plt.legend(title='Implementations', loc='lower left', prop={'size': 7})

    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(f'../data/graphs/MPImethods_compare.png')
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

def plot_mpi_omp_comparison2(mpifile, ompfile):
    # Read the MPI data
    df_mpi = pd.read_csv(mpifile, delimiter=";")
    df_mpi_avg = df_mpi.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Read the OpenMP data
    df_omp = pd.read_csv(ompfile, delimiter=";")
    df_omp_avg = df_omp.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Create a figure with two subplots stacked vertically
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1, 1]})

    # Plot MPI data
    ax1 = axes[0]
    n_procs = df_mpi_avg['n_procs'].unique()
    for n_proc in n_procs:
        subset = df_mpi_avg[df_mpi_avg['n_procs'] == n_proc]
        ax1.plot(subset['mPow_size'], subset['time(s)'], marker='o', linestyle='-', label=f"n_procs {n_proc}")

    ax1.set_title('[M1] Time vs. Matrix Sizes for Different N_Processors (MPI)', fontsize=14)
    ax1.set_ylabel('log Time (s)')
    ax1.set_yscale('log')
    ax1.set_xlabel('Matrix size pow (2^n)')
    plt.xticks(subset['mPow_size'])
    ax1.legend(title='N_Procs configuration', loc='best', prop={'size': 8})
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Plot OpenMP data
    ax2 = axes[1]
    n_threads = df_omp_avg['n_threads'].unique()
    for n_thread in n_threads:
        subset = df_omp_avg[df_omp_avg['n_threads'] == n_thread]
        ax2.plot(subset['mPow_size'], subset['time(s)'], marker='o', linestyle='-', label=f"n_threads {n_thread}")

    ax2.set_title('[M1] Time vs. Matrix Sizes for Different N_Threads (OMP)', fontsize=14)
    ax2.set_xlabel('Matrix size pow (2^n)')
    ax2.set_ylabel('log Time (s)')
    ax2.set_yscale('log')
    ax2.legend(title='N_Threads configuration', loc='best', prop={'size': 8})
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, top=0.95, bottom=0.1)

    # Save and show the figure
    plt.savefig('../data/graphs/mpi_omp_comparison2.png')
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
    plt.title('[M1]Efficiency Comparison for Different Matrix Sizes (strong scaling) (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_efficiency_comparisonSTRONG.png')
    plt.show()

def plot_mpi_omp_performance_comparisonSTRONG(mpifile, ompfile, seqfile):
    # Read the CSV file directly
    df = pd.read_csv(mpifile, delimiter=';')
    df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df2 = pd.read_csv(ompfile, delimiter=';')
    df2_avg = df2.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df3 =  pd.read_csv(seqfile, delimiter=';')
    df3_avg = df3.groupby(['mPow_size']).agg({'time(s)': 'mean'}).reset_index()

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

        #SEQ data to get actual best serial time as T0:
        subset3 = df3_avg[df3_avg['mPow_size'] == msize]
        subset_time3 = subset3['time(s)']

        if len(subset_time3) > 0 and subset_time3.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time3.iloc[0] #subset_time2 to utilize T0 from SEQ data
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

        subset3 = df3_avg[df3_avg['mPow_size'] == msize2]
        subset_time3 = subset3['time(s)']

        if len(subset_time3) > 0 and subset_time3.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time3.iloc[0] #subset_time2 to utilize T0 from SEQ data
            # T1_O = subset_time2.iloc[0]  #USE T1 from the openmp 1 thread as base timing
            speedup2 = [T1 / t for t in subset_time2]
            speedup_data2[msize2] = speedup2

            # Calculate efficiency
            efficiency2 = [(S / p) * 100 for S, p in zip(speedup2, subset_threads2)]
            efficiency_data2[msize2] = efficiency2
        else:
            print(f"Warning: No data found for matrix size 2^{msize2} with n_threads = 1")



    # Plot Speedup vs Threads for all matrix sizes
    plt.figure(figsize=(10, 6))

    # Plot ideal speedup line
    # plt.plot(subset_threads, subset_threads, linestyle='--', color = 'black', label=f"Ideal speedup")

    #Plot Speedup vs NThreads for all matrix sizes
    for msize, color in zip(speedup_data, ['#FF6347', '#FBC02D', '#A52A2A']):
        plt.plot(subset_threads, speedup_data[msize], marker='o', linestyle='-', color=color, label=f"Matrix Size 2^{msize} [MPI]")
        plt.xticks(subset_threads)

    for msize2, color in zip(speedup_data2, ['#4682B4', '#1E90FF', '#000080']):
        plt.plot(subset_threads2, speedup_data2[msize2], marker='o', linestyle='-', color=color, label=f"Matrix Size 2^{msize2} [OMP]")

    plt.xlabel('Number of Processes/Threads')
    plt.ylabel('Speedup')
    plt.title('[M1]Speedup Comparison for Different Matrix sizes configurations, Strong scaling (avg of 5 runs)', fontsize=14)
    plt.legend(title='Matrix Sizes', loc='upper left', bbox_to_anchor=(0, 1), prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_omp_speedup_comparisonSTRONG.png')
    plt.show()

    # Plot Efficiency vs NThreads for all matrix sizes
    plt.figure(figsize=(10, 6))
    for msize, color in zip(efficiency_data, ['#FF6347', '#FBC02D', '#A52A2A']):
        plt.plot(subset_threads, efficiency_data[msize], marker='o', linestyle='-', color=color, label=f"Matrix Size 2^{msize} [MPI]")
        plt.xticks(subset_threads)

    for msize2, color in zip(efficiency_data2, ['#4682B4', '#1E90FF', '#000080']):
        plt.plot(subset_threads2, efficiency_data2[msize2], marker='o', linestyle='-', color=color, label=f"Matrix Size 2^{msize2} [OMP]")


    plt.xlabel('log2 Number of Processes/Threads')
    plt.xscale('log', base=2)
    plt.ylabel('Efficiency (%)')
    plt.yscale('linear')
    plt.title('[M1]Efficiency Comparison for Different Matrix sizes configurations, Strong scaling (avg of 5 runs)', fontsize=14)
    plt.legend(title='Matrix Sizes', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_omp_efficiency_comparisonSTRONG.png')
    plt.show()

def plot_mpi_omp_performance_comparisonWEAK(mpifile, ompfile, seqfile):
    # Read the CSV file directly
    df = pd.read_csv(mpifile, delimiter=';')
    df_avg = df.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df2 = pd.read_csv(ompfile, delimiter=';')
    df2_avg = df2.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df3 =  pd.read_csv(seqfile, delimiter=';')
    df3_avg = df3.groupby(['mPow_size']).agg({'time(s)': 'mean'}).reset_index()

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

        #SEQ data to get actual best serial time as T0:
        subset3 = df3_avg[df3_avg['mPow_size'] == msize]
        subset_time3 = subset3['time(s)']

        if len(subset_time3) > 0 and subset_time3.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time3.iloc[0] #subset_time2 to utilize T0 from SEQ data
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

        #SEQ data to get actual best serial time as T0:
        subset3 = df3_avg[df3_avg['mPow_size'] == msize]
        subset_time3 = subset3['time(s)']

        if len(subset_time3) > 0 and subset_time3.iloc[0] is not np.nan:
            # Time with a single thread (n_threads = 1)
            T1 = subset_time3.iloc[0] #subset_time2 to utilize T0 from SEQ data
            # T1_O = subset_time2.iloc[0]  #USE T1 from the openmp 1 thread as base timing
            speedup2 = [T1 / t for t in subset_time2]
            speedup_data2[msize2] = speedup2

            # Calculate efficiency
            efficiency2 = [(S / p) * 100 for S, p in zip(speedup2, subset_threads2)]
            efficiency_data2[msize2] = efficiency2
        else:
            print(f"Warning: No data found for matrix size 2^{msize2} with n_threads = 1")



    # Plot Speedup vs Threads for all matrix sizes
    plt.figure(figsize=(10, 6))

    # Plot ideal speedup line
    # plt.plot(subset_threads, subset_threads, linestyle='--', color = 'black', label=f"Ideal speedup")

    #Plot Speedup vs NThreads for all matrix sizes
    for msize, color in zip(speedup_data, ['#FF6347', '#E34234', '#A52A2A']):
        plt.plot(subset_threads, speedup_data[msize], marker='o', linestyle='-', color=color, label=f"[MPI]")
        plt.xticks(subset_threads)

    for msize2, color in zip(speedup_data2, ['#4682B4', '#1E90FF', '#000080']):
        plt.plot(subset_threads2, speedup_data2[msize2], marker='o', linestyle='-', color=color, label=f"[OMP]")


    plt.xlabel('Number of Processes/Threads')
    plt.ylabel('Speedup')
    plt.title('[M1]Weak scaling Speedup ([N_procs/threads]:matrix_size = [1]:2^7, [4]:2^8, [16]:2^9, [64]:2^10) (avg of 5 runs)')
    plt.legend(title='Matrix Sizes', loc='upper left', bbox_to_anchor=(0, 1), prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_omp_speedup_comparisonWEAK.png')
    plt.show()

    # Plot Efficiency vs NThreads for all matrix sizes
    plt.figure(figsize=(10, 5))
    for msize, color in zip(efficiency_data, ['#FF6347', '#E34234', '#A52A2A']):
        plt.plot(subset_threads, efficiency_data[msize], marker='o', linestyle='-', color=color, label=f"[MPI]")
        plt.xticks(subset_threads)

    for msize2, color in zip(efficiency_data2, ['#4682B4', '#1E90FF', '#000080']):
        plt.plot(subset_threads2, efficiency_data2[msize2], marker='o', linestyle='-', color=color, label=f"[OMP]")

    # Plot ideal weak scaling efficiency line
    plt.axhline(y=100, color='red', linestyle='--', label="Ideal Weak Scale Efficiency")

    plt.xlabel('log2 Number of Processes/Threads')
    plt.xscale('log', base=2)
    plt.ylabel('Efficiency (%)')
    plt.yscale('linear')
    plt.title('[M1]Weak scaling Efficiency ([N_procs/threads]:matrix_size = [1]:2^7, [4]:2^8, [16]:2^9, [64]:2^10) (avg of 5 runs)')
    plt.legend(title='Implementation', loc='upper right', prop={'size': 9})
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig('../data/graphs/mpi_omp_efficiency_comparisonWEAK.png')
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

def plot_mpi_omp_bandwidth(seqfile, mpifile, ompfile):
    # Read and preprocess the data
    df_seq = pd.read_csv(seqfile, delimiter=';')
    df_seq_avg = df_seq.groupby(['mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df_mpi = pd.read_csv(mpifile, delimiter=';')
    df_mpi_avg = df_mpi.groupby(['n_procs', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    df_omp = pd.read_csv(ompfile, delimiter=';')
    df_omp_avg = df_omp.groupby(['n_threads', 'mPow_size']).agg({'time(s)': 'mean'}).reset_index()

    # Define a helper function to calculate bandwidth
    def calculate_bandwidth(matrix_size_pow2, time_s):
        matrix_size = 2 ** matrix_size_pow2  # Compute size of one side
        total_elements = matrix_size ** 2   # Total number of elements
        data_moved = 2 * total_elements * 4  # Bytes (2 for read/write, 4 bytes for float)
        data_moved_gb = data_moved / (1024 ** 3)  # Convert to GB
        return data_moved_gb / time_s  # Bandwidth in GB/s

    # Calculate bandwidth for sequential
    df_seq_avg['bandwidth(GB/s)'] = df_seq_avg.apply(
        lambda row: calculate_bandwidth(row['mPow_size'], row['time(s)']),
        axis=1
    )

    # Calculate bandwidth for MPI
    df_mpi_avg['bandwidth(GB/s)'] = df_mpi_avg.apply(
        lambda row: calculate_bandwidth(row['mPow_size'], row['time(s)']),
        axis=1
    )

    # Calculate bandwidth for OpenMP
    df_omp_avg['bandwidth(GB/s)'] = df_omp_avg.apply(
        lambda row: calculate_bandwidth(row['mPow_size'], row['time(s)']),
        axis=1
    )

    # Create the plots
    plt.figure(figsize=(12, 10))

    # Plot Sequential Bandwidth
    plt.subplot(3, 1, 1)
    plt.plot(
        df_seq_avg['mPow_size'], df_seq_avg['bandwidth(GB/s)'],
        marker='o', label="Sequential", color='blue'
    )
    plt.title('Sequential Bandwidth', fontsize=14)
    plt.xlabel('Matrix size (2^n)')
    plt.ylabel('Bandwidth (GB/s)')
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.legend()

    # Plot MPI Bandwidth
    plt.subplot(3, 1, 2)
    for n_procs in df_mpi_avg['n_procs'].unique():
        subset = df_mpi_avg[df_mpi_avg['n_procs'] == n_procs]
        plt.plot(
            subset['mPow_size'], subset['bandwidth(GB/s)'],
            marker='o', label=f"MPI {n_procs} procs"
        )
    plt.title('MPI Bandwidth', fontsize=14)
    plt.xlabel('Matrix size (2^n)')
    plt.ylabel('Bandwidth (GB/s)')
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.legend()

    # Plot OpenMP Bandwidth
    plt.subplot(3, 1, 3)
    for n_threads in df_omp_avg['n_threads'].unique():
        subset = df_omp_avg[df_omp_avg['n_threads'] == n_threads]
        plt.plot(
            subset['mPow_size'], subset['bandwidth(GB/s)'],
            marker='o', label=f"OpenMP {n_threads} threads"
        )
    plt.title('OpenMP Bandwidth', fontsize=14)
    plt.xlabel('Matrix size (2^n)')
    plt.ylabel('Bandwidth (GB/s)')
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.legend()

    # Save the figure to a PNG file
    plt.tight_layout()
    plt.savefig('../data/graphs/mpi_omp_bandwidth.png')
    plt.show()


def main():
    plot_omp_comparison1(comparemethods)
    # plot_omp_comparison2(omp_csvfile)
    # plot_omp_performance_comparison(omp_csvfile)
    # plot_seq_imp_performance(*process_csv(seq_csvfile))
    # plot_seq_imp_performance(*process_csv(imp_csvfile))
    # plot_seq_imp_comparison() DEPRECATED
    # plot_imp_optimizations()
    # plot_mpi_comparison1(mpi_csvfile)
    # plot_mpi_comparison1BAR(mpi_csvfile)
    # plot_mpi_omp_comparison2(mpi_csvfile, omp_csvfile)
    # plot_mpi_performance_comparison(mpiSTRONG_csvfile)
    plot_mpi_omp_performance_comparisonSTRONG(mpiSTRONG_csvfile, ompSTRONG_csvfile, seqSTRONG_csvfile)
    # plot_mpi_omp_performance_comparisonWEAK(mpiWEAK_csvfile, ompWEAK_csvfile, seqWEAK_csvfile)
    # plot_mpi_omp_bandwidth(seq_csvfile, mpi_csvfile, omp_csvfile)
if __name__ == "__main__":
    main()
