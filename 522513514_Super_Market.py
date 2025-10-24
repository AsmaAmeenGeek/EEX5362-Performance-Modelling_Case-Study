import random
import simpy
import statistics
import matplotlib.pyplot as plt

def supermarket_simulation(num_cashiers=4, sim_time=480, arrival_rate=0.4, service_mean=7.5, seed=42, verbose=False):
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
        event_logs.append(f"Customer {cust_id} arrived at {arrival_time:.2f} min")
        queue_history.append((env.now, len(cashiers.queue)))
        
        with cashiers.request() as req:
            yield req
            start_service_time = env.now
            wait = start_service_time - arrival_time
            wait_times.append(wait)
            if wait > 0:
                customers_who_waited += 1
            
            event_logs.append(f"Customer {cust_id} assigned to cashier at {start_service_time:.2f} min (waited {wait:.2f} min)")
            queue_history.append((env.now, len(cashiers.queue)))

            service_time = random.expovariate(1.0 / service_mean)
            total_busy_time += service_time
            yield env.timeout(service_time)
            
            depart_time = env.now
            event_logs.append(f"Customer {cust_id} departed at {depart_time:.2f} min (service {service_time:.2f} min)")
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
    percent_waited = (customers_who_waited / total_served * 100.0) if total_served > 0 else 0.0
    percent_immediate = 100.0 - percent_waited
    utilization = min((total_busy_time / (num_cashiers * sim_time) * 100.0), 100.0)

    print("\n=== Simulation Results ===")
    print(f"Total customers served: {total_served}")
    print(f"Average wait time: {avg_wait:.2f} min")
    print(f"Throughput: {throughput:.3f} cust/min")
    print(f"Percent waited: {percent_waited:.2f}%")
    print(f"Percent immediate: {percent_immediate:.2f}%")
    print(f"Cashier utilization: {utilization:.2f}%")

    if verbose:
        print("\n--- Event Logs ---")
        for log in event_logs:
            print(log)

    plt.figure(figsize=(8, 5))
    plt.hist(wait_times, bins=10, edgecolor='black', alpha=0.7)
    plt.xlabel('Wait Time (minutes)')
    plt.ylabel('Frequency')
    plt.title('Wait Time Distribution')
    plt.show()

    if queue_history:
        times, queue_lens = zip(*queue_history)
        plt.figure(figsize=(10, 6))
        plt.step(times, queue_lens, where='post')
        plt.scatter(times, queue_lens, s=10)
        plt.xlabel('Time (minutes)')
        plt.ylabel('Queue Length')
        plt.title('Queue Length Over Time')
        plt.grid(True)
        plt.show()

    metrics = ['Avg Wait', 'Throughput', '% Waited', 'Utilization']
    values = [avg_wait, throughput, percent_waited, utilization]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(metrics, values, color=['blue', 'green', 'red', 'purple'])
    for bar in bars:
        h = bar.get_height()
        plt.annotate(f'{h:.2f}', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0,3), textcoords="offset points", ha='center', va='bottom')
    plt.title('Key Metrics')
    plt.show()

if __name__ == "__main__":
    results = supermarket_simulation(verbose=True)
