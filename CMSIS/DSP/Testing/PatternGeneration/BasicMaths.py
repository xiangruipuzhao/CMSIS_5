import os.path
import numpy as np
import itertools
import Tools


# Those patterns are used for tests and benchmarks.
# For tests, there is the need to add tests for saturation


def writeTests(config,format):
    NBSAMPLES=256

    data1=np.random.randn(NBSAMPLES)
    data2=np.random.randn(NBSAMPLES)
    data3=np.random.randn(1)
    
    data1 = data1/max(data1)
    data2 = data1/max(data2)

    config.writeInput(1, data1)
    config.writeInput(2, data2)
    
    ref = data1 + data2
    config.writeReference(1, ref)
    
    ref = data1 - data2
    config.writeReference(2, ref)
    
    ref = data1 * data2
    config.writeReference(3, ref)
    
    ref = -data1
    config.writeReference(4, ref)
    
    ref = data1 + 0.5
    config.writeReference(5, ref)
    
    ref = data1 * 0.5
    config.writeReference(6, ref)
    
    
   
    nb = Tools.loopnb(format,Tools.TAILONLY)
    ref = np.array([np.dot(data1[0:nb] ,data2[0:nb])])

    if format == 31 or format == 15:
       if format==31:
          ref = ref / 2**15 # Because CMSIS format is 16.48
       if format==15:
          ref = ref / 2**33 # Because CMSIS format is 34.30
       config.writeReferenceQ63(7, ref)
    elif format == 7:
       ref = ref / 2**17 # Because CMSIS format is 18.14
       config.writeReferenceQ31(7, ref)
    else:
       config.writeReference(7, ref)
    
    nb = Tools.loopnb(format,Tools.BODYONLY)
    ref = np.array([np.dot(data1[0:nb] ,data2[0:nb])])

    if format == 31 or format == 15:
       if format==31:
          ref = ref / 2**15 # Because CMSIS format is 16.48
       if format==15:
          ref = ref / 2**33 # Because CMSIS format is 34.30
       config.writeReferenceQ63(8, ref)
    elif format == 7:
       ref = ref / 2**17 # Because CMSIS format is 18.14
       config.writeReferenceQ31(8, ref)
    else:
       config.writeReference(8, ref)
    
    nb = Tools.loopnb(format,Tools.BODYANDTAIL)
    ref = np.array([np.dot(data1[0:nb] ,data2[0:nb])])

    if format == 31 or format == 15:
       if format==31:
          ref = ref / 2**15 # Because CMSIS format is 16.48
       if format==15:
          ref = ref / 2**33 # Because CMSIS format is 34.30
       config.writeReferenceQ63(9, ref)
    elif format == 7:
       ref = ref / 2**17 # Because CMSIS format is 18.14
       config.writeReferenceQ31(9, ref)
    else:
       config.writeReference(9, ref)
    
    ref = abs(data1)
    config.writeReference(10, ref)

    #ref = np.array([np.dot(data1 ,data2)])
    #config.writeReference(11, ref)

    return(11)


def writeTestsWithSat(config,format):
    if format == 31:
       NBSAMPLES=9

    if format == 15:
       NBSAMPLES=17

    if format == 7:
       NBSAMPLES=33

    nb = writeTests(config,format)

    data1 = np.full(NBSAMPLES, 2**format - 1)
    data1[1::2] = 2
    data2 = np.full(NBSAMPLES, -2**format)
    data2[1::2] = -2

    datar=np.random.randn(NBSAMPLES)
    datar = datar/max(datar)
    datar = datar / 3.0 # Because used to test shift of 2 without saturation

    config.writeInput(nb+1, datar)

    if format == 31:
       config.writeInputS32(nb+1,data1-1,"MaxPosInput")
       config.writeInputS32(nb+1,data2+1,"MaxNegInput")
       config.writeInputS32(nb+1,data2,"MaxNeg2Input")

    if format == 15:
       config.writeInputS16(nb+1,data1-1,"MaxPosInput")
       config.writeInputS16(nb+1,data2+1,"MaxNegInput")
       config.writeInputS16(nb+1,data2,"MaxNeg2Input")

    if format == 7:
       config.writeInputS8(nb+1,data1-1,"MaxPosInput")
       config.writeInputS8(nb+1,data2+1,"MaxNegInput")
       config.writeInputS8(nb+1,data2,"MaxNeg2Input")
       
    d1 = 1.0*(data1-1) / 2**format
    d2 = 1.0*(data2+1) / 2**format
    d3 = 1.0*(data2) / 2**format

    ref = d1 + d1
    config.writeReference(nb+1, ref,"PosSat")
    ref = d2 + d2
    config.writeReference(nb+2, ref,"NegSat")

    d1 = 1.0*(data1-1) / 2**format
    d2 = 1.0*(data2+1) / 2**format
    ref = d1 - d2
    config.writeReference(nb+3, ref,"PosSat")

    ref = d2 - d1
    config.writeReference(nb+4, ref,"NegSat")

    ref = d3*d3
    config.writeReference(nb+5, ref,"PosSat")

    ref = -d3
    config.writeReference(nb+6, ref,"PosSat")

    ref = d1 + 0.9
    config.writeReference(nb+7, ref,"PosSat")
    ref = d2 - 0.9
    config.writeReference(nb+8, ref,"NegSat")

    ref = d3 * d3[0]
    config.writeReference(nb+9, ref,"PosSat")

    ref = datar * 2.0
    config.writeReference(nb+10, ref,"Shift")

    ref = d1 * 2.0
    config.writeReference(nb+11, ref,"Shift")

    ref = d2 * 2.0
    config.writeReference(nb+12, ref,"Shift")



PATTERNDIR = os.path.join("Patterns","DSP","BasicMaths","BasicMaths")
PARAMDIR = os.path.join("Parameters","DSP","BasicMaths","BasicMaths")

configf32=Tools.Config(PATTERNDIR,PARAMDIR,"f32")
configq31=Tools.Config(PATTERNDIR,PARAMDIR,"q31")
configq15=Tools.Config(PATTERNDIR,PARAMDIR,"q15")
configq7=Tools.Config(PATTERNDIR,PARAMDIR,"q7")



writeTests(configf32,0)
writeTestsWithSat(configq31,31)
writeTestsWithSat(configq15,15)
writeTestsWithSat(configq7,7)

# Params just as example
someLists=[[1,3,5],[1,3,5],[1,3,5]]

r=np.array([element for element in itertools.product(*someLists)])
configf32.writeParam(1, r.reshape(81))

