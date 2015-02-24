from collections import namedtuple

Version = namedtuple('Version',
    [   'major',
        'minor'
    ]
)

FileHeader = namedtuple('FileHeader',
    [   'checksum',
        'fileHeaderSize',
        'signature',
        'softwareVersion',
        'fileVersion',
        'spectrumHeaderSize',
        'fileTrailerSize',
        'instrumentDBProvider',
        'fileID'
    ]
)

Calibration = namedtuple('Calibration',
    [   'equationType',
        'nConstants',
        'constants'
    ]
)

LaserIntensity = namedtuple('LaserIntensity',
    [   'min',
        'max'
    ]
)

SpectrumHeader = namedtuple('SpectrumHeader',
    [   'checksum',
        'signature',
	    'spectrumID',
        'instrumentID',
        'operatingMode',
        'dataFormat',
        'compressionType',
        'dataChecksum',
        'sizePoints',
        'sizeBytes',
        'startTime',
        'incrementTime',
        'timeStamp',
        'totalIONCount',
        'basePeakTimeS',
        'basePeakIntensity',
        'totalShots',
        'totalAccumulations',

        'defaultCalibration',
        'acquisitionCalibration',

        'locationBounds',

        'laserIntensity',

        'longFlags'
    ]
)