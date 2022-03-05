# neb_visualize fork 
Process Nudged Elastic Band (NEB) data from an ORCA-NEB run

Plot generation: 

<img src="README__neb_optimization.png" alt="drawing" width="300"/></a> <img src="README__neb_lastiter.png" alt="drawing" width="300"/></a>

NEB snapshot plots for the CH3Cl  + F- --> Cl- + CH3F reaction IRC path [calculated using orca](https://www.orcasoftware.de/tutorials_orca/react/nebts.html) 

Usage: 

```ruby
chmod +x nebsnap.sh 								#make into executable (only do once)
nebsnap.sh [orca.interp] [start iter] [end iter] 	#run nebsnap.sh executable
```

**orca.interp**	name of the .interp file outputted from an ORCA NEB run (default: orca.interp)

**start iter**	integer value for the number of iteration where the script should start plotting (default: 0)

**end iter** 	integer value for the number of iteration where the script should stop plotting  (default: -1 (last iter.))





