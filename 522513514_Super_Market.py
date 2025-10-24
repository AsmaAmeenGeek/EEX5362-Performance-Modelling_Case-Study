import random
import simpy
import statistics
import matplotlib.pyplot as plt
import numpy as np 

def supermarket_simulation(num_cashiers=4, sim_time=480, arrival_rate=0.4, service_mean=7.5, seed=42, verbose=False, scenario_name="Unnamed"):
    
    random.seed(seed)
    
    wait_times = []               
    total_busy_time = 0.0         
    customers_who_waited = 0      
    queue_history = []            
    event_logs = []              

    env = simpy.Environment()
    cashiers = simpy.Resource(env, capacity=num_cashiers)

    def customer(env, cust_id):
        nonlocal total_busy_time, customers_who_waited
        arrival_time = env.now
        log = f"Customer {cust_id} arrives at {arrival_time:.2f} minutes"
        event_logs.append(log)
        if verbose: print(log)
        
        queue_history.append((env.now, len(cashiers.queue)))
        
        with cashiers.request() as req:
            yield req
            start_service_time = env.now
            wait = start_service_time - arrival_time
            wait_times.append(wait)
            if wait > 0:
                customers_who_waited += 1
            
            log = f"Customer {cust_id} assigned to cashier after waiting {wait:.2f} minutes at {start_service_time:.2f}"
            event_logs.append(log)
            if verbose: print(log)
            
            queue_history.append((env.now, len(cashiers.queue)))

            service_time = random.expovariate(1.0 / service_mean)
            total_busy_time += service_time
            yield env.timeout(service_time)
            
            depart_time = env.now
            log = f"Customer {cust_id} departed at {depart_time:.2f} minutes (service {service_time:.2f} min)"
            event_logs.append(log)
            if verbose: print(log)
            
            queue_history.append((env.now, len(cashiers.queue)))

    def arrival_generator(env):
        cust_id = 1
        while True:
            inter_arrival = random.expovariate(arrival_rate)
            yield env.timeout(inter_arrival)
            if env.now >= sim_time:
                break
            env.process(customer(env, cust_id))
            cust_id += 1

    env.process(arrival_generator(env))
    env.run(until=sim_time)

    total_served = len(wait_times)
    avg_wait = statistics.mean(wait_times) if wait_times else 0.0
    throughput = total_served / sim_time if sim_time > 0 else 0.0
    final_queue = len(cashiers.queue) 
    percent_waited = (customers_who_waited / total_served * 100.0) if total_served > 0 else 0.0
    percent_immediate = 100.0 - percent_waited
    utilization = min((total_busy_time / (num_cashiers * sim_time) * 100.0), 100.0)
    
    print(f"\n=== {scenario_name} Results ===")
    
    print(f"Simulation complete (time: {sim_time} min).")
    print(f"Total customers served: {total_served}")
    print(f"Average wait time: {avg_wait:.2f} min")
    print(f"Throughput: {throughput:.3f} cust/min")
    print(f"Final queue length: {final_queue}")
    print(f"Percent customers who waited: {percent_waited:.2f}%")
    print(f"Percent customers served immediately: {percent_immediate:.2f}%")
    print(f"Cashier utilization: {utilization:.2f}%")

    return {
        'total_served': total_served,
        'avg_wait': avg_wait,
        'throughput': throughput,
        'final_queue': final_queue,
        'wait_times': wait_times,
        'queue_history': queue_history,
        'percent_waited': percent_waited,
        'percent_immediate': percent_immediate,
        'utilization': utilization,
        'event_logs': event_logs,
        'num_cashiers': num_cashiers,
        'sim_time': sim_time,
        'arrival_rate': arrival_rate,
        'service_mean': service_mean
    }

def plot_visualizations(results_dict, scenario_name):


    plt.figure(figsize=(8, 5))
    plt.hist(results_dict['wait_times'], bins=10, edgecolor='black', alpha=0.7)
    plt.xlabel('Wait Time (minutes)')
    plt.ylabel('Frequency')
    plt.title(f'Wait Time Distribution - {scenario_name}')
    plt.savefig(f'wait_histogram_{scenario_name.lower().replace(" ", "_")}.png')
    plt.show()
    
    if results_dict['queue_history']:
        times, queue_lens = zip(*results_dict['queue_history'])
    else:
        times, queue_lens = ([0], [0])
    plt.figure(figsize=(10, 6))
    plt.step(times, queue_lens, where='post') 
    plt.scatter(times, queue_lens, s=10)
    plt.xlabel('Time (minutes)')
    plt.ylabel('Queue Length')
    plt.title(f'Queue Length Over Time - {scenario_name}')
    plt.grid(True)
    plt.savefig(f'queue_line_{scenario_name.lower().replace(" ", "_")}.png')
    plt.show()
    
    metrics = ['Avg Wait (min)', 'Throughput (cust/min)', 'Final Queue', '% Waited', 'Utilization %']
    values = [results_dict['avg_wait'], results_dict['throughput'], results_dict['final_queue'],
              results_dict['percent_waited'], results_dict['utilization']]
    plt.figure(figsize=(10, 5))
    bars = plt.bar(metrics, values)
    plt.title(f'Key Metrics - {scenario_name}')
    plt.ylabel('Value')
    plt.xticks(rotation=15)
    for bar in bars:
        h = bar.get_height()
        plt.annotate(f'{h:.2f}', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    plt.savefig(f'metrics_bar_{scenario_name.lower().replace(" ", "_")}.png')
    plt.show()

def run_experiments(base_params, verbose=True):
    """
    Runs multiple scenarios:
    1. Baseline
    2. High Traffic
    3. More Cashiers
    4. Faster Service
    """
    scenarios = [
        ('Baseline', base_params),
        ('High Traffic', {**base_params, 'arrival_rate': base_params['arrival_rate'] * 2}),
        ('More Cashiers', {**base_params, 'num_cashiers': max(1, base_params['num_cashiers'] * 2)}),
        ('Faster Service', {**base_params, 'service_mean': max(0.1, base_params['service_mean'] * 0.7)})
    ]
    
    results_list = []
    scenario_names = []
    
    for name, params in scenarios:
        print(f"\n--- Running {name} Scenario ---")
        results = supermarket_simulation(num_cashiers=params['num_cashiers'],
                                        sim_time=params['sim_time'],
                                        arrival_rate=params['arrival_rate'],
                                        service_mean=params['service_mean'],
                                        seed=params.get('seed', 42),
                                        verbose=verbose,
                                        scenario_name=name)  
        results_list.append(results)
        scenario_names.append(name)
    
    print("\n--- Experiment Summary Table ---")
    print("Scenario\tAvg Wait (min)\tThroughput (cust/min)\tFinal Queue\t%Waited\tUtil(%)")
    for i, name in enumerate(scenario_names):
        r = results_list[i]
        print(f"{name}\t\t{r['avg_wait']:.2f}\t\t{r['throughput']:.3f}\t\t{r['final_queue']}\t\t{r['percent_waited']:.1f}\t{r['utilization']:.1f}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(scenario_names, [r['avg_wait'] for r in results_list], color=['blue', 'red', 'green', 'purple'])
    ax1.set_title('Average Wait Time by Scenario')
    ax1.set_ylabel('Minutes')
    ax1.tick_params(axis='x', rotation=45)
    ax2.bar(scenario_names, [r['throughput'] for r in results_list], color=['blue', 'red', 'green', 'purple'])
    ax2.set_title('Throughput by Scenario')
    ax2.set_ylabel('Customers/Min')
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig('scenario_comparison.png')
    plt.show()
    
    plot_visualizations(results_list[0], scenario_names[0])
    
    return results_list

if __name__ == "__main__":
    print("Enter parameters for baseline scenario:")
    num_cashiers = int(input("Number of cashiers (default 4): ") or 4)
    sim_time = int(input("Simulation time in minutes (default 480): ") or 480)
    arrival_rate = float(input("Arrival rate (cust/min, default 0.4): ") or 0.4)
    service_mean = float(input("Average service time per customer (min, default 7.5): ") or 7.5)
    
    base_params = {
        'num_cashiers': num_cashiers,
        'sim_time': sim_time,
        'arrival_rate': arrival_rate,
        'service_mean': service_mean,
        'seed': 42
    }
    
    results = run_experiments(base_params, verbose=True)
    
    print("\nApplication terminated!")
    print("=== Good Bye! ===")