# Crash Your Laptop

Fun program to Overload and crash your laptop. Use with discretion

# Installation Instruction

```
git clone https://github.com/Think-Evolve-Consulting/crash-your-laptop
pip install psutil
```

# Run instructions

CPU at 50% utilization
```
python iwannacrash.py --cpu 0.5 
```

CPU at 80% utilization and use 4 workers 
```
python iwannacrash.py --cpu 0.8 --workers 4
```

CPU at 20% utilization use all cores and RAM at 60% utilization
```
python iwannacrash.py --cpu 0.2 --ram 0.6 --workers -1
```

