import os
import sys
import shutil
import numpy as np
import matplotlib.pyplot as plt
import time

def read_spline_file(fname):
    with open(fname) as input_data:
        listi = []
        images = []
        spline = []
        for i,line in enumerate(input_data):
            if line == '\n':
                listi.append('E')
            else:
                line=line.split()
                listi.append(line)
                if line[0] == 'Interp.:':
                    spline.append(i)
                if line[0] == 'Images:':
                    images.append(i)
    return listi, images, spline

def read_images(start_point, listi):
    arclength = []
    energy    = []
    index = start_point
    while True:
        if listi[index][0].strip().upper() == 'INTERP.:' or listi[index][0].strip().upper() == 'E':
            break
        arclength.append( float(listi[index][0]) )
        energy.append( float(listi[index][1]) )
        index += 1
    return arclength, energy

def read_spline(start_point, listi):
    arclength = []
    energy    = []
    index = start_point
    while True:
        if listi[index][0].strip().upper() == 'ITERATION:' or listi[index][0].strip().upper() == 'E':
            break
        arclength.append( float(listi[index][0]) )
        energy.append( float(listi[index][1]) )
        index += 1
        if  index == len(listi):
            break
    return arclength, energy

def convert_bool(val):
    if val.upper() == 'FALSE':
        val = False
    elif val.upper() == 'TRUE':
        val = True
    return val
    
if __name__ == "__main__":

    """
    Script to generate quick 'energy-profile' trajectory from an ORCA NEB run
    using python 2.7, numpy and matplotlib.

    Usage: python neb_snapshots.py basename.interp start_at_iter<int> end_at_iter<int> full<bool>
    (in the given order)

    Authors: Vilhjalmur Asgeirsson, Benedikt Orri Birgirsson (UI, 2018)
    """

    # ============================================
    # Print header
    # ============================================
    print('==========================================')
    print('     Generation of snapshots from        ')
    print('              ORCA NEB       ')
    print('==========================================')
    print(' ')

    # ============================================
    # set default values for input arguments
    # ============================================
    fname            = 'orca.interp'
    only_one_frame   = True  
    start_from       = 0  
    end_at           = -1 
    # ============================================
    # get input arguments
    # ============================================
    
    # Notice that the ordering of the input arguments matter!
    for i in range(1, len(sys.argv)):
        if i == 1:
            fname=sys.argv[i] 
            if not os.path.isfile(fname):
                raise RuntimeError("Can not find file: %s", fname)
        elif i == 2:
            try:
                start_from = int(sys.argv[i])
            except:
                raise TypeError("Invalid type for the second argument. Expecting int")
        elif i == 3:
            try:
                end_at = int(sys.argv[i])
            except:
                raise TypeError("Invalid type for the third argument. Expecting int")
        elif i == 4:
            only_one_frame = convert_bool(sys.argv[i])
            
        else:
            raise RuntimeError("Too many input arguments. Usage: python neb_snapshots.py basename.interp start_at<int> end_at<int> full<bool>")
            

    if only_one_frame:
        print_str = 'all in single frame'
    else:
        print_str = 'snapshots'
        
    print('=> plotting from iteration %i to %i' % (start_from, end_at))
    print('=> type of plot: %s\n' % print_str)

    # - - - - - - - - - - - - - - - - - - - - - - - 
    # Let the plotting begin...
    # - - - - - - - - - - - - - - - - - - - - - - - 
    

    # ==========================================================
    # We read .interp file only once into 'listi'
    # and the starting points of each 'images' and 'interp'
    # sections in the file.
    # =========================================================
    
    listi, start_images, start_spline = read_spline_file(fname)
    no_of_iters = len(start_spline)

    if end_at == -1:
        end_at = no_of_iters

    # ==========================================================
    # Make some checks...
    # =========================================================

    if len(start_images) != len(start_spline):
        raise RuntimeError("Corrupt spline file!")

    if start_from > no_of_iters or end_at > no_of_iters or start_from > end_at:
        raise RuntimeError("The number of iterations in the .interp file is incorrect")

    # ==========================================================
    # Create dir. neb_frames (you can comment out this section)
    # ==========================================================
    path = os.getcwd()
    working_dir = path+'/neb_frames'
    
    if os.path.isdir(working_dir):
        print('Directory %s found!' % working_dir)
        print('    => Existing files are overwritten!')
    else:
        os.mkdir(working_dir)
        print('Working dir: %s' % working_dir)

    os.chdir(working_dir)

    one_iter = False
    if no_of_iters == 1:
        if 'final' in fname.lower():
            print('*** Note that %s contains only the last iteration of a NEB/CI-NEB run  ***' % fname)
        else:
            print('%s contains only one iteration?   ***' % fname)
        one_iter = True

    # ==========================================================
    # Read and plot the spline and images of the .interp file 
    # ==========================================================
    if not one_iter:
        print('Iteration: ')

    for i in range(start_from, end_at):
        saveI = i
        if not one_iter:
            print('%3i' % i)
            

        arcS,  Eimg    = read_images(start_images[i]+1, listi)       
        arcS2, Eimg2   = read_spline(start_spline[i]+1, listi)
        
        # Convert atomic units to eV and angstr.
        newE1 = np.array(Eimg)#*27.211396132
        newE2 = np.array(Eimg2)#*27.211396132
        newS1 = np.array(arcS)#/1.889725989
        newS2 = np.array(arcS2)#/1.889725989

        if not only_one_frame:
            # Generate and save frame
            plt.plot(newS2, newE2, '-k', label='Interp.')
            plt.plot(newS1, newE1, '.r', Markersize=5.5, label='NEB img.')
            plt.xlabel("Reaction path")
            plt.ylabel("Energy")
            plt.savefig('frame_'+str(saveI)+'.png')
            plt.clf()
        else:
            # Plot frames together
            if i == end_at-1:
                plt.plot(newS2, newE2, '-r', label='Last iter.')
                plt.plot(newS1, newE1, '.r', Markersize=5.5)                
            else:
                plt.plot(newS2, newE2, '-k', label='Interp.')
                plt.plot(newS1, newE1, '.y', Markersize=5.5, label='NEB img.')

    
    # save whole trajectory
    if only_one_frame:
        plt.xlabel("Reaction path")
        plt.ylabel("Energy")
        if not one_iter:
            plt.title( "Iter.:"+str(start_from)+" to "+str(saveI) )
        plt.savefig('neb_optimization.png')

        plt.clf()
        plt.plot(newS2, newE2, '-k', label='Interp.')
        plt.plot(newS1, newE1, '.r', label='NEB img.')
        plt.xlabel("Reaction path")
        plt.ylabel("Energy")
        plt.savefig('neb_lastiter.png')


    print('')
    print('==========================================')
    print('Execution terminated (see /neb_frames).')
    print('==========================================')

