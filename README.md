# neb_visualize
Process Nudged Elastic Band (NEB) data from an ORCA-NEB run

Usage: 

```ruby
chmod +x nebsnap.sh 	#make into executable (only do once)
nebsnap.sh [orca.interp] [start iter] [end iter] 	#run nebsnap.sh executable
```

**orca.interp**	name of the .interp file outputted from an ORCA NEB run (default: orca.interp)

**start iter**	integer value for the iteration index where the script starts plotting (default: 0)

**end iter** 	integer value for the iteration index where the script stops plotting  (default: -1 (last iter))

Example: `CH3Cl  + F- --> Cl- + CH3F` reaction IRC path [calculated using orca](https://www.orcasoftware.de/tutorials_orca/react/nebts.html) 

Makes

<img src="README__neb_optimization.png" alt="drawing" width="300"/></a> <img src="README__neb_lastiter.png" alt="drawing" width="300"/></a>

---LOCAL MAXIMA (E barriers) ---
E = 0.00645889 Hartrees @ 0.76422265 Bohrs

