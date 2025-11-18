
# 1. IMPORT LIBRARIES

# Import numpy for math calculations
import numpy as np
# Import matplotlib.pyplot for creating plots and visualizations
import matplotlib.pyplot as plt


# 2. DEFINE BIOLOGICAL PARAMETERS AND SIMULATION SETUP

# This function defines the key variables that control our simulation,
# including timing for LTP and LTD induction and the learning rates.

def setup_parameters():
    """
    Sets up all the parameters for the LTP and LTD simulation.
    Returns:
        dict: A dictionary containing all simulation parameters.
    """
    params = {
        # Simulation Time 
        'total_time': 150,         # Total simulation duration in seconds
        'dt': 0.1,                 # Time step in seconds (The smaller it is the more precise it si)

        # Synaptic Properties 
        'w_initial': 1.0,          # Initial synaptic weight (baseline strength)
        'w_max': 2.5,              # Maximum possible synaptic weight (a ceiling for potentiation)
        'w_min': 0.5,              # Minimum possible synaptic weight (a floor for depression)
        'ltp_learning_rate': 0.5,  # Controls how quickly the weight increases during LTP
        'ltd_learning_rate': 0.3,  # Controls how quickly the weight decreases during LTD

        # Stimulation Protocol 
        'hfs_start': 40,           # HFS (High-Frequency Stimulation) for LTP starts
        'hfs_end': 45,             # HFS for LTP ends
        'lfs_start': 100,          # LFS (Low-Frequency Stimulation) for LTD starts
        'lfs_end': 105,            # LFS for LTD ends
    }
    return params


# 3. RUN THE LTP/LTD SIMULATION

# This is the main function where the simulation happens. It will loop through
# time, check the stimulation protocol, and update the synaptic weight.

def run_simulation(params):
    """
    So this will simulate the change in synaptic weight over time based on the stimulation protocol.
    Args:
        params (dict): A dictionary containing simulation parameters.
    Returns:
        tuple: A tuple containing the time array and the synaptic_weight array.
    """
    # Unpack parameters from the dictionary for easier access
    total_time = params['total_time']
    dt = params['dt']
    w_initial = params['w_initial']
    w_max = params['w_max']
    w_min = params['w_min']
    ltp_rate = params['ltp_learning_rate']
    ltd_rate = params['ltd_learning_rate']
    
    hfs_start = params['hfs_start']
    hfs_end = params['hfs_end']
    lfs_start = params['lfs_start']
    lfs_end = params['lfs_end']

    #  Initialization 
    # Create a time vector from 0 to total_time with steps of dt
    time_steps = np.arange(0, total_time, dt)
    # Create an array to store the synaptic weight at each time step
    synaptic_weight = np.zeros(len(time_steps))
    synaptic_weight[0] = w_initial

    #  Simulation Loop 
    # Iterate through each time step to calculate the new synaptic weight
    for i in range(len(time_steps) - 1):
        current_time = time_steps[i]
        current_weight = synaptic_weight[i]

        # Check for High-Frequency Stimulation (HFS) to induce LTP
        if hfs_start <= current_time < hfs_end:
            # The weight increases towards its maximum value (w_max)
            dw = ltp_rate * (w_max - current_weight) * dt
            synaptic_weight[i+1] = current_weight + dw
        
        # Check for Low-Frequency Stimulation (LFS) to induce LTD
        elif lfs_start <= current_time < lfs_end:
            # The weight decreases towards its minimum value (w_min)
            dw = ltd_rate * (w_min - current_weight) * dt  # Note: (w_min - current_weight) is negative
            synaptic_weight[i+1] = current_weight + dw
            
        else:
            # Baseline or Post-Stimulation: The weight remains stable
            synaptic_weight[i+1] = current_weight

    return time_steps, synaptic_weight

# 
# 4. PLOT THE RESULTS
# 
# This function takes the results of the simulation and creates a professional,
# well-labeled plot to visualize the bidirectional plasticity.

def plot_results(time_steps, synaptic_weight, params):
    """
    So this will generate and display a plot of synaptic weight vs. time.
    Args:
        time_steps (np.array): The array of time points.
        synaptic_weight (np.array): The array of synaptic weights over time.
        params (dict): The dictionary of simulation parameters for labeling.
    """
    plt.figure(figsize=(12, 7)) # Create a figure
    
    # Plot the synaptic weight against time
    plt.plot(time_steps, synaptic_weight, label='Synaptic Weight', color='royalblue', linewidth=2.5)

    # --- Add labels and title ---
    plt.title('Model of Bidirectional Plasticity in Schaffer Collateral Pathway', fontsize=16)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Synaptic Weight (Arbitrary Units)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6) # Add a grid

    # --- Add shaded regions to indicate stimulation periods ---
    plt.axvspan(params['hfs_start'], params['hfs_end'], color='salmon', alpha=0.4, 
                label='High-Frequency Stimulation (LTP Induction)')
    
    plt.axvspan(params['lfs_start'], params['lfs_end'], color='skyblue', alpha=0.5, 
                label='Low-Frequency Stimulation (LTD Induction)')

    # Set the y-axis limits
    plt.ylim(params['w_min'] - 0.2, params['w_max'] + 0.2)
    plt.legend(fontsize=10) # Display the legend
    
    # Display the final plot
    plt.show()


# 5. MAIN EXECUTION BLOCK

# This block runs all the functions in the correct order when the script is executed.

if __name__ == '__main__':
    # Step 1: Set up the parameters
    simulation_params = setup_parameters()
    # Step 2: Run the simulation with those parameters
    time, weight = run_simulation(simulation_params)
    # Step 3: Plot the generated data
    plot_results(time, weight, simulation_params)