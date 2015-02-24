from __future__ import print_function

import zlib, array, sys

from t2d_headers import *
from t2d_header_parser import parse_file_header, parse_spectrum_header, file_header_length, spectrum_header_length
from t2d_mass_solver import solve_mass

expected_file_header_signature = 2774143540
expected_spectrum_header_signature = 1515852355

intensity_formats = {
    1 : 'H',            # unsigned short
    2 : 'i',            # signed integer
    3 : 'f',            # float
    4 : 'd'             # double
}

def parse_data(file_data):
    file_header         = parse_file_header(        file_data[ 0                 : file_header_length                            ])
    spectrum_header     = parse_spectrum_header(    file_data[file_header_length : file_header_length + spectrum_header_length   ])

    if file_header.signature != expected_file_header_signature:
        sys.exit("Expected header signature %ld, got %ld" % (expected_file_header_signature, file_header.signature))

    if spectrum_header.signature != expected_spectrum_header_signature:
        sys.exit("Expected spectrum signature %ld, got %ld" % (expected_spectrum_header_signature, spectrum_header.signature))

    # decompress point data and extract points to an array
    compressed_data_start   = file_header.fileHeaderSize + file_header.spectrumHeaderSize
    compressed_data_end     = compressed_data_start + spectrum_header.sizeBytes
    uncompressed_data = zlib.decompress(file_data[compressed_data_start : compressed_data_end])

    if spectrum_header.dataFormat not in intensity_formats:
        sys.exit("Unable to parse data format %d for intensities" % (spectrum_header.dataFormat))

    fmt = intensity_formats[spectrum_header.dataFormat]
    intensities = array.array(fmt, uncompressed_data)

    if (len(intensities) != spectrum_header.sizePoints):
        sys.exit("Expected %d points, got %d" % (spectrum_header.sizePoints, len(intensities)))

    readings = [ (solve_mass(
                    spectrum_header.startTime, 
                    spectrum_header.incrementTime, 
                    index, 
                    spectrum_header.acquisitionCalibration
                  ), intensity) for index, intensity in enumerate(intensities) ]

    return file_header, spectrum_header, readings

def parse_file(filename):
    with open(filename, 'rb') as f:
        file_data = f.read();

        return parse_data(file_data)


if __name__ == '__main__':
    import argparse, time

    parser = argparse.ArgumentParser(description='Read and convert t2d spectrum files to raw readings.')
    parser.add_argument('input_file', help='t2d file to read data from.')
    parser.add_argument('-o', '--ouput' , help='Output file to write readings to. Each row consists of a mass then an intensity.')
    args = parser.parse_args()

    infile = args.input_file
    outfile = args.ouput

    print ("t2d to raw converter")
    print ("")
    print ("Parsing %s..." % (infile,), end='')

    start = time.time()
    file_header, spectrum_header, readings = parse_file(infile)
    end = time.time()

    print(" done")
    print("Parsing took %fms" % ((end-start)*1000,))

    print("""
Spectrum info:
    Instrument DB provider:    "%s"

    Operating mode:            %d
    Number of points:          %d
    Total ION count:           %f
    Base peak time:            %f
    Base peak intensity:       %f
    Total shots:               %ld
    Total accumulations:       %ld

    Minimum laser intensity:   %f
    Maximum laser intensity:   %f
    """ % ( file_header.instrumentDBProvider, spectrum_header.operatingMode, spectrum_header.sizePoints,
            spectrum_header.totalIONCount, spectrum_header.basePeakTimeS, spectrum_header.basePeakIntensity, 
            spectrum_header.totalShots, spectrum_header.totalAccumulations,
            spectrum_header.laserIntensity.min, spectrum_header.laserIntensity.max ))

    if outfile:
        print ("Writing readings to %s..." % (outfile, ), end='')
        with open(outfile, 'w') as f:
            for reading in readings:
                f.write("%f\t%f\n" % reading)

    print(" done")
