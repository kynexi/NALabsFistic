import numpy as np
import matplotlib.pyplot as plt
# Arrival rate functions
def arrival_rate_steady(t):
    return 5.0

def arrival_rate_gaussian(t):
    baseline = 5.0
    burst = 20.0 * np.exp(-0.5 * ((t - 5.0)/1.0)**2)
    return baseline + burst

def arrival_rate_sine(t):
    return 5.0 + 5.0 * np.sin(2 * np.pi * t / 10)

def departure_rate(U, mu):
    return mu * U

def simulate_euler(total_servers, mu, T, dt, arrival_fn):
    """
    Simulate using forward Euler:
      dU/dt = λ(t) - μ·U,  if there is at least one free server
             = -μ·U,      if U has already hit capacity
      dR/dt = -dU/dt  (because U+R = total_servers is constant)
      
    Arguments:
      total_servers: integer, total pool size (U + R always = this).
      mu:            service‐completion rate per busy server (1/minute).
      T:             total simulation time (minutes).
      dt:            time step (minutes).
    Returns:
      time_array, U_array, R_array
    """
    num_steps = int(T / dt) + 1
    time = np.linspace(0, T, num_steps)
    U = np.zeros(num_steps)
    R = np.zeros(num_steps)

    U[0] = 0.0
    R[0] = float(total_servers)

    for i in range(1, num_steps):
        t_prev = time[i - 1]
        U_prev = U[i - 1]
        R_prev = R[i - 1]

        lam = arrival_fn(t_prev)
        dep = departure_rate(U_prev, mu)

        if R_prev > 0:
            dU_dt = lam - dep
        else:
            dU_dt = -dep

        U_new = max(0.0, min(U_prev + dt * dU_dt, total_servers))
        R_new = total_servers - U_new

        U[i] = U_new
        R[i] = R_new

    return time, U, R


def choose_scenario():
    print("Select a simulation scenario:")
    print("1 - Steady Load (constant arrival rate)")
    print("2 - Gaussian Spike (traffic surge around t=5)")
    print("3 - Oscillating Load (sine wave arrival pattern)")
    choice = input("Enter 1, 2, or 3: ")
    return int(choice)

def main():
    scenario = choose_scenario()
    if scenario == 1:
      arrival_fn = arrival_rate_steady
      title = "Scenario 1: Steady Load"
    elif scenario == 2:
      arrival_fn = arrival_rate_gaussian
      title = "Scenario 2: Spike"
    elif scenario == 3:
      arrival_fn = arrival_rate_sine
      title = "Scenario 3: Oscillating Load"
    else:
      print("Invalid choice. Defaulting to Scenario 1.")
      arrival_fn = arrival_rate_steady
      title = "Scenario 1: Steady Load"

    total_servers = int(input("Enter total number of servers (10, 20, 50): "))
    mu            = 1.0   # each busy server finishes its job at rate = 1 job/min
    T             = 15.0  # simulate for 15 minutes
    dt            = 0.01  # time step = 0.01 minute

    
    time, U, R = simulate_euler(total_servers, mu, T, dt, arrival_fn)

    plt.figure(figsize=(10,5))
    plt.plot(time, U, label='Busy Servers U(t)')
    plt.plot(time, R, label='Free Servers R(t)')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Number of Servers')
    plt.title('Cloud Resource Utilisation (Euler Method)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
   main()