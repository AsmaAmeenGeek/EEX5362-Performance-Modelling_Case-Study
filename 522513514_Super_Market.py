import random
import simpy
import statistics
import matplotlib.pyplot as plt

def supermarket_simulation(num_cashiers=4, sim_time=480, arrival_rate=0.4, service_mean=7.5, seed=42, verbose=False):
    random.seed(seed)

    wait_times = []
    total_busy_time = 0.0
    customers_who_waited = 0

    env = simpy.Environment()
    cashiers = simpy.Resource(env, capacity=num_cashiers)

    def customer(env, cust_id):
        nonlocal total_busy_time, customers_who_waited
        arrival_time = env.now
        with cashiers.request() as req:
            yield req
            start_service = env.now
            wait = start_service - arrival_time
            wait_times.append(wait)
            if wait > 0:
                customers_who_waited += 1

            service_time = random.expovariate(1.0 / service_mean)
            total_busy_time += service_time
            yield env.timeout(service_time)

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
    utilization = min((total_busy_time / (num_cashiers * sim_time) * 100.0), 100.0)

    results = {
        "cashiers": num_cashiers,
        "avg_wait": avg_wait,
        "throughput": throughput,
        "percent_waited": percent_waited,
        "utilization": utilization,
        "served": total_served,
    }

    if verbose:
        print(f"\n[Scenario] Cashiers: {num_cashiers}, Arrival rate: {arrival_rate}, Service mean: {service_mean}")
        print(f"→ Served: {total_served}, Avg Wait: {avg_wait:.2f}, Utilization: {utilization:.2f}%")

    return results

def run_scenarios():
    print("\n=== Running Multiple Scenarios ===")

    scenarios = {
        "Baseline": dict(num_cashiers=4, arrival_rate=0.4, service_mean=7.5),
        "High Traffic": dict(num_cashiers=4, arrival_rate=0.8, service_mean=7.5),
        "More Cashiers": dict(num_cashiers=6, arrival_rate=0.4, service_mean=7.5),
        "Faster Service": dict(num_cashiers=4, arrival_rate=0.4, service_mean=5.0)
    }

    results = {}
    for name, params in scenarios.items():
        results[name] = supermarket_simulation(**params)

    print("\n=== Scenario Summary ===")
    for name, data in results.items():
        print(f"{name}: Served={data['served']} | Avg Wait={data['avg_wait']:.2f} | "
              f"Throughput={data['throughput']:.3f} | Utilization={data['utilization']:.2f}%")

    metrics = ["avg_wait", "throughput", "utilization"]
    for metric in metrics:
        plt.figure(figsize=(8, 5))
        values = [results[name][metric] for name in results]
        plt.bar(results.keys(), values, color=['skyblue', 'orange', 'lightgreen', 'violet'])
        plt.title(f"Comparison of {metric.replace('_', ' ').title()} Across Scenarios")
        plt.ylabel(metric.replace('_', ' ').title())
        plt.xticks(rotation=15)
        for i, val in enumerate(values):
            plt.text(i, val, f"{val:.2f}", ha='center', va='bottom')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    run_scenarios()