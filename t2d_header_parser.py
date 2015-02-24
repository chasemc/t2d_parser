import struct 

from t2d_headers import *

# Struct format specifiers
# See header templates (preferably in 010 editor) for what these specify
# Strings are used for internal structs so these can be parsed later 
file_header_fmt = '<hhL4s4shh128s16s'
version_fmt = '<hh'
spectrum_header_fmt = '<h2xL16sl4h2l6d2L84s84sd16sL'
calibration_data_fmt = '2h80s'
calibration_data_constants_fmt = '10d'
laser_intensity_fmt = '2d'

file_header_length = struct.calcsize(file_header_fmt)
spectrum_header_length = struct.calcsize(spectrum_header_fmt)

def parse_version(version_data):
    return Version._make(struct.unpack(version_fmt, version_data))

def parse_cstring(cstring_data):
    return cstring_data.split('\x00')[0]

def parse_file_header(file_header_data):
    file_header = FileHeader._make(struct.unpack(file_header_fmt, file_header_data))

    # file_header contains other structs, so unpack these to coresponding namedtuples 
    file_header = file_header._replace(softwareVersion=parse_version(file_header.softwareVersion))
    file_header = file_header._replace(fileVersion=parse_version(file_header.fileVersion))

    # cut null terminated string down to correct length
    file_header = file_header._replace(instrumentDBProvider=parse_cstring(file_header.instrumentDBProvider))

    return file_header

def parse_calibration_constants(calibration_constants_data):
    return struct.unpack(calibration_data_constants_fmt, calibration_constants_data)

def parse_calibration(calibration_data):
    calibration = Calibration._make(struct.unpack(calibration_data_fmt, calibration_data))

    # parse internal structs
    calibration = calibration._replace(constants=parse_calibration_constants(calibration.constants))

    return calibration

def parse_laser_intensity(laser_intensity_data):
    return LaserIntensity._make(struct.unpack(laser_intensity_fmt, laser_intensity_data))

def parse_spectrum_header(spectrum_header_data):
    spectrum_header = SpectrumHeader._make(struct.unpack(spectrum_header_fmt, spectrum_header_data))

    # parse internal structs
    spectrum_header = spectrum_header._replace(defaultCalibration=parse_calibration(spectrum_header.defaultCalibration))
    spectrum_header = spectrum_header._replace(acquisitionCalibration=parse_calibration(spectrum_header.acquisitionCalibration))
    spectrum_header = spectrum_header._replace(laserIntensity=parse_laser_intensity(spectrum_header.laserIntensity))

    return spectrum_header