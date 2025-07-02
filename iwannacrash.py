import time
import argparse
import multiprocessing
import psutil
import os

def cpu_burn(throttle):
    # CPU-burn loop with sleep to throttle
    interval = 0.1  # seconds
    busy = interval * throttle
    idle = interval - busy
    while True:
        t0 = time.time()
        while (time.time() - t0) < busy:
            pass  # busy-wait
        if idle > 0:
            time.sleep(idle)

def ram_eat(ram_throttle):
    # Fill RAM up to the throttle limit (percentage)
    available = psutil.virtual_memory().available
    target = int(psutil.virtual_memory().total * ram_throttle)
    chunk = 100_000_000  # 100 MB
    gobble = []
    used = 0
    try:
        while used < target:
            gobble.append(bytearray(min(chunk, target - used)))
            used += chunk
            time.sleep(0.1)  # slow ramp-up
        while True:
            time.sleep(1)  # keep memory alive
    except MemoryError:
        print("Memory limit reached or process killed.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu', type=float, default=0.0, help='CPU throttle (0 to 1)')
    parser.add_argument('--ram', type=float, default=0.0, help='RAM throttle (0 to 1)')
    parser.add_argument('--workers', type=int, default=1, help='Number of CPU workers')
    args = parser.parse_args()

    procs = []
    # Start CPU burn processes
    for _ in range(args.workers):
        if args.cpu > 0:
            p = multiprocessing.Process(target=cpu_burn, args=(args.cpu,))
            p.start()
            procs.append(p)
    # Start RAM eat process (just one)
    if args.ram > 0:
        p = multiprocessing.Process(target=ram_eat, args=(args.ram,))
        p.start()
        procs.append(p)
    print(f"Started with CPU throttle {args.cpu}, RAM throttle {args.ram}, workers {args.workers}")
    for p in procs:
        p.join()

if __name__ == '__main__':
    main()
