import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------
# 1. Define arrival and departure rates
# ---------------------------------------------

def arrival_rate(t):
    """
    Example: baseline 5 tasks/min + a Gaussian burst around t=5.
    You can replace this with any simple function (step, sine, etc.).
    Units: tasks per minute.
    """
    baseline = 5.0
    burst   = 20.0 * np.exp(-0.5 * ((t - 5.0)/1.0)**2)  # peaked at t=5, width=1
    return baseline + burst

def departure_rate(U, mu):
    """
    If U servers are busy, total departure rate = mu * U (jobs finish at rate μ each).
    """
    return mu * U

# ---------------------------------------------
# 2. Euler‐step update for U and R
# ---------------------------------------------

def simulate_euler(total_servers, mu, T, dt):
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
    
    U = np.zeros(num_steps)  # busy servers over time
    R = np.zeros(num_steps)  # free servers over time
    
    # initial condition: no busy servers, all free
    U[0] = 0.0
    R[0] = float(total_servers)
    
    for i in range(1, num_steps):
        t_prev = time[i-1]
        U_prev = U[i-1]
        R_prev = R[i-1]
        
        lam = arrival_rate(t_prev)           # λ(t)
        dep = departure_rate(U_prev, mu)     # μ * U
        
        # If there is at least one free server, arrivals go into service:
        if R_prev > 0:
            dU_dt = lam - dep
        else:
            # No free servers => arrivals cannot start service; U only decreases
            dU_dt = -dep
        
        # Euler update for U
        U_new = U_prev + dt * dU_dt
        
        # Enforce floor/ceiling so U stays between 0 and total_servers
        U_new = max(0.0, min(U_new, float(total_servers)))
        
        # Because U + R = total_servers, we can set R directly:
        R_new = float(total_servers) - U_new
        
        U[i] = U_new
        R[i] = R_new
    
    return time, U, R

# ---------------------------------------------
# 3. Run the simulation
# ---------------------------------------------

total_servers = 200   # e.g. a pool of 200 identical servers
mu            = 1.0   # each busy server finishes its job at rate = 1 job/min
T             = 15.0  # simulate for 15 minutes
dt            = 0.01  # time step = 0.01 minute

time, U, R = simulate_euler(total_servers, mu, T, dt)

# ---------------------------------------------
# 4. Plot results
# ---------------------------------------------

plt.figure(figsize=(10,5))
plt.plot(time, U, label='Busy Servers U(t)')
plt.plot(time, R, label='Free Servers R(t)')
plt.xlabel('Time (minutes)')
plt.ylabel('Number of Servers')
plt.title('Cloud Resource Utilisation (Euler Method)')
plt.legend()
plt.grid(True)
plt.show()
