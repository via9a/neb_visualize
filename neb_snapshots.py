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
            line = line.strip()
            if line == '\n' or not line:
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
        arclength.append( float(listi[index][1]) )
        energy.append( float(listi[index][2]) )
        index += 1
    return arclength, energy

def read_spline(start_point, listi):
    arclength = []
    energy    = []
    index = start_point
    while True:
        if listi[index][0].strip().upper() == 'ITERATION:' or listi[index][0].strip().upper() == 'E':
            break
        arclength.append( float(listi[index][1]) )
        energy.append( float(listi[index][2]) )
        index += 1
        if  index == len(listi):
            break
    return arclength, energy
    
if __name__ == "__main__":

    """
    Script to generate quick 'energy-profile' trajectory from an ORCA NEB run
    using python 2.7, numpy and matplotlib.

    Usage: python neb_snapshots.py basename.interp start_at_iter<int> end_at_iter<int> full<bool>
    (in the given order)

    Authors: Vilhjalmur Asgeirsson, Benedikt Orri Birgirsson (UI, 2018)
    email for bugs and requests: via9@hi.is, bob9@hi.is
    """

    # ============================================
    # Print header
    # ============================================
    print('==========================================')
    print('     Optimization Profile: ORCA-NEB')
    print('==========================================')
    print('Modified: 14.08.2019')

    # ============================================
    # set default values for input arguments
    # ============================================
    fname            = 'orca.interp'
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
        else:
            raise RuntimeError("Too many input arguments. Usage: python neb_snapshots.py basename.interp start_at<int> end_at<int>")
    print('=> looking at iteration %i to %i' % (start_from, end_at))
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
    for i in range(start_from, end_at):
        # read spline and images from list: listi
        arcS,  Eimg    = read_images(start_images[i]+1, listi)       
        arcS2, Eimg2   = read_spline(start_spline[i]+1, listi)

        if i == start_from:
            # initial frame is black
            plt.plot(arcS2, Eimg2, '-k')
            plt.plot(arcS, Eimg, '.k', Markersize=6.0)
        elif i == end_at-1:
            # final frame is red
            plt.plot(arcS2, Eimg2, '-', Color=[0.6, 0.0, 0.0],LineWidth=1.5)
            plt.plot(arcS, Eimg, '.',Color=[0.6, 0.0, 0.0], Markersize=8.0)                
        else:
            # interm. frames are gray
            plt.plot(arcS2, Eimg2, '-',Color=[0.4, 0.4, 0.4]) 
            plt.plot(arcS, Eimg, '.',Color=[0.4, 0.4, 0.4],  Markersize=4.0)

    
    # save whole profile
    plt.xlabel("Displacement [Bohr]", FontSize=15)
    plt.ylabel("Energy [Ha]", FontSize=15)
    plt.title( "Iter.: %i to %i" % (start_from, end_at-1) )
    plt.savefig('neb_optimization.png')


    # Make last iter.
    plt.clf()
    plt.plot(arcS2, Eimg2, '-',Color=[0.6, 0.0, 0.0], LineWidth=1.5)
    plt.plot(arcS, Eimg, '.',Color=[0.6, 0.0, 0.0], MarkerSize=8.0)
    plt.xlabel("Displacement [Bohr]",FontSize=15)
    plt.ylabel("Energy [Ha]", FontSize=15)
    plt.savefig('neb_lastiter.png')

    print('==========================================')
    print('Execution terminated (see /neb_frames).')
    print('==========================================')

    
