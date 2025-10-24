# EEX5362-Performance-Modelling_Case-Study
This simulation analyzes supermarket checkout performance using Python


# Supermarket Checkout Simulation

## Project Overview

This project simulates a supermarket cashier checkout system to study how different configurations like number of cashiers, customer arrival rates, and service times impact key performance metrics such as customer waiting time, queue length, and cashier utilization.

Supermarket checkout systems are a common real-world scenario where performance affects both customer satisfaction and operational efficiency. Long queues can frustrate customers, while idle cashiers represent wasted resources. This simulation provides insights for making better staffing and operational decisions.

The project is implemented in Python 3.10.8, using SimPy for event-driven simulation, and Matplotlib for visualizations.
## Features

- Event-driven simulation of customers arriving and being served at multiple cashiers
- Supports parameterized experiments: number of cashiers, arrival rate, service time, simulation duration
- Tracks key metrics
   - Average wait time
   - Queue length over time
   - Throughput (customers served per minute)
   - Final queue length
   - Cashier utilization
   - Percent of customers who waited vs served immediately

- Generates detailed logs for customer arrivals, service assignments, and departures.

 - Runs four scenarios
    - Baseline (Normal store operation)
       - 4 cashiers 
       - 0.4 cust/min arrival  
       - 7.5 min service
    - High Traffic (Test system under peak customer load)
       - 4 cashiers
       - 0.8 cust/min arrival
       - 7.5 min service
    - More Cashiers (Evaluate effect of increasing staff)
       - 8 cashiers
       - 0.4 cust/min arrival
       - 7.5 min service
    - Faster Service (Evaluate effect of faster service efficiency)
       - 4 cashiers
       - 0.4 cust/min arrival
       - 5.25 min service


## Installation
 - Install Python 3.10.8 if not already installed.
 - Install required Python libraries:


```bash
pip install simpy matplotlib
```

 - Clone or download this repository to your local machine
    
## How to Run

- Open a terminal and navigate to the project folder
- Run the main script
    
```bash
522513514_Super_Market.py
```

- The program will prompt for baseline scenario parameters. You can enter values or simply press Enter to use default values:

  - Number of cashiers: 4
  - Simulation time (minutes): 480 (8 hours)
  - Arrival rate (customers/min): 0.4
  - Average service time (minutes/customer): 7.5

- The program will automatically run four scenarios and display results.

- Verbose Mode Behavior:

   - If verbose = True, each scenario prints line-by-line customer event logs (arrival, assignment, departure), followed by the scenario summary.
   - If verbose = False, the detailed logs are hidden, but all scenario summaries and the final summary table are displayed.
   - This allows you to toggle between detailed tracing and clean summary outputs depending on your needs.

- Visualizations are saved as PNG files:

## Key Metrics Tracked

- Average Wait Time – Time a customer waits before being served.
- Queue Length Over Time – Number of customers in the queue throughout the simulation.
- Throughput – Customers served per minute.
- Final Queue Length – Customers remaining in the queue at the end.
- Cashier Utilization – Percentage of time cashiers were busy.
- Percent Customers Who Waited – Shows the proportion of customers who experienced waiting.

## How to Customize

 - Modify num_cashiers, arrival_rate, service_mean, and sim_time to experiment with different conditions.
 - Toggle verbose = True/False in run_experiments() to control detailed logging.
 - Add new scenarios by extending the scenarios list in the code.

## Appendix

### References / Learning Sources
- SimPy Documentation: https://simpy.readthedocs.io/en/latest/simpy_intro/index.html
- Python Random Documentation: https://docs.python.org/3/library/random.html
- Matplotlib Documentation: https://matplotlib.org/stable/users/index.html
- Real Python – Data Visualization with Matplotlib: https://realpython.com/python-matplotlib-guide/


## Author
**Asma Ameen**  
Undergraduate – Bachelor of Software Engineering (Hons)  
The Open University of Sri Lanka

