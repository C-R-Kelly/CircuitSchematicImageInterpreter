"""
Configuration Parameters
========================

Configuration Options

author: C. R. Kelly
email: CK598@cam.ac.uk

"""


# Configuration Options for module / function
class Config:
    def __init__(self):
        # actions / wireDetect config
        self.threshold = 0.05  # default: 0.05 /// % of empty space required in region either side of a wire for it to count. Value range between 0 and 1
        # actions / wireScanHough config
        self.minWireLength = 10  # default 10 /// minimum length a line can be for it to be classed as a wire
        self.borderSize = 15  # default 15  /// how many pixels the inspection region extends either side of the wire
        # actions / objectDetection config
        self.maximumDistance = 85  # default 85 /// maximum distance allowed between end of first wire and start of second for it to be classed as an ROI
        self.minimumDistance = 3  # default 3 /// minimum distance allowed between end of first wire and start of second for it to be classed as an ROI
        self.bboxOffset = 4  # default is 10 /// how many pixels the bounding box extends in the direction of each connecting wire. 0 means the start of wire 1 and end of wire 2 is the bbox.
        # actions / groundSymbolCheck config
        self.groundInspectionAreaHeight = 7   # default is 7 /// half the length of the square inspection area at the end of the wire
        self.groundInspectionAreaWidth = 10  # default is 10 /// half the length of the square inspection area at the end of the wire
        self.groundInspectionThreshold = 0.17    # default is 0.17 /// % of pixels in area to be 'on' pixels to return a found ground symbol


        # Classes / Component config
        self.componentWidth = 25  # default 35 /// how many pixels the bounding box extends at the normal to the direction of each connecting wire

        # io / config
        self.extension = '.tif'
        self.exportPath = 'C:\\PycharmProjects\\MPhil_Project_Final_V0.0.1\\test_results\\'
        self.exportDPI = (300, 300)

        # OCR / config
        self.langModelSymbols = 'model_project_final'
        self.langModelLabels = 'eng+grc'
        self.configLineSymbols = '--psm 13 --dpi 300 -c tessedit_char_whitelist=0123456789@[]+-*{}<>/Aa()\\\ -c load_system_dawg=false -c load_freq_dawg=false'
        self.configLineLabels = ' -c load_system_dawg=false -c load_freq_dawg=false'
        self.labelsPSM = '--psm 12'
        self.display = True


class SPICE_Config:

    def __init__(self):
        # config for optional component values
        self.Resistor = '1kOhm'
        self.Capacitor = '1uF'
        self.Inductor = '1H'
        self.Cell = '10V'

        # Assign default component values
        self.AssignDefaultComponentValues = True

        # Netlist file extension
        self.NetlistExtension = '.txt'