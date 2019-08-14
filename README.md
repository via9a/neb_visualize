# neb_visualize
script to visualize results from an ORCA-NEB run for ORCA 4.2

Usage: python neb_snapshots.py basename.interp start_at_iter<int> end_at_iter<int> 

Input Variables:
basename.interp - name of the .interp file outputted from an ORCA NEB run (default: orca.interp)
start_at_iter   - integer value for the number of iteration where the script should start plotting (default: 0)
end_at_iter     - integer value for the number of iteration where the script should stop plotting  (default: -1 (last iter.))
