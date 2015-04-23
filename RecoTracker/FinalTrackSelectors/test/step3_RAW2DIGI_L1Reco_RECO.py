# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions auto:run2_mc_HIon -s RAW2DIGI,L1Reco,RECO -n 2 --eventcontent RECOSIM --scenario HeavyIons --datatier GEN-SIM-RECO --beamspot RealisticHI2011Collision --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1 --filein file:step2.root --fileout file:step3.root
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process('RERECO')

#options = VarParsing.VarParsing ('analysis')
#options.register ('mva',
#                    -1,
#                    VarParsing.VarParsing.multiplicity.singleton,
#                    VarParsing.VarParsing.varType.float,
#                    "mva value for the lowpt step")
#options.parseArguments()


#outputFile = 'step3_mva_'+str(options.mva)+'.root'
#print outputFile

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentHeavyIons_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(2)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:step2_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_PU_100_1_FSH.root'),#step3_RAW2DIGI_L1Reco_RECO_100_1_nLj.root'),
#fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/user/mnguyen/PyquenUnquenched_Dijet_NcollFilt_pthat80_740pre8_MCHI1_74_V4_GEN-SIM_v3/PyquenUnquenched_Dijet_pthat80_740pre8_MCHI2_74_V3_DIGI-RAW_v2/ee815b27030c232e2e0a7be48a50a463/step2_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_PU_100_1_2fl.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:2'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RECO'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:step3_RAW2DIGI_L1Reco_RECO.root'),
    outputCommands = process.RECODEBUGEventContent.outputCommands,#cms.untracked.vstring(['keep *']),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc_HIon', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstructionHeavyIons)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOSIMoutput_step)

# customisation of the process.

from CondCore.DBCommon.CondDBSetup_cfi import *
process.beamspot = cms.ESSource("PoolDBESSource",CondDBSetup,
                                toGet = cms.VPSet(cms.PSet( record = cms.string('BeamSpotObjectsRcd'),
                                                            tag= cms.string('RealisticHICollisions2011_STARTHI50_mc')
                                                            )),
                                connect =cms.string('frontier://FrontierProd/CMS_COND_31X_BEAMSPOT')
                                )
process.es_prefer_beamspot = cms.ESPrefer("PoolDBESSource","beamspot")

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions

def setupforest(selector, forestname, forestvaluetight, forestvaluepure, variables):
    selector.GBRForestFileName = cms.string("GBRForest_algo_4_5_6_7_trees_500_4_shortlist.root")
    selector.GBRForestLabel = cms.string(forestname)
    selector.GBRForestVars = cms.vstring(variables)
    selector.useAnyMVA = cms.bool(False)
    
    selector.trackSelectors[0].useMVA = cms.bool(False)
    selector.trackSelectors[1].useMVA = cms.bool(True)
    selector.trackSelectors[2].minMVA = cms.double(forestvaluetight)    
    selector.trackSelectors[2].useMVA = cms.bool(True)
    selector.trackSelectors[2].minMVA = cms.double(forestvaluepure)
    
    for s in selector.trackSelectors:
        s.minHitsToBypassChecks = cms.uint32(999)
        s.min_nhits = cms.uint32(8)

    selector.trackSelectors[0].d0_par2 = cms.vdouble(9999.0, 0.0)
    selector.trackSelectors[0].dz_par2 = cms.vdouble(9999.0, 0.0)
    selector.trackSelectors[0].max_relpterr = cms.double(9999)
    selector.trackSelectors[0].keepAllTracks = cms.bool(False)



setupforest(process.hiInitialStepSelector, 
            "BDTG_algo_4_trees_500_4",
            -0.6, -0.5,
            ['Chi2/Ndof/Nlayer', 'Dxy1/DxyError1', 'Dz1/DzError1', 'NHit', 'Nlayer', 'Eta']
            )
setupforest(process.hiLowPtTripletStepSelector, 
            "BDTG_algo_5_trees_500_4",
            0.3, 0.4,
            ['Chi2/Ndof/Nlayer', 'Dxy1/DxyError1', 'Dz1/DzError1', 'PtError/Pt', 'NHit', 'Nlayer', 'Eta']
            )
setupforest(process.hiPixelPairStepSelector, 
            "BDTG_algo_6_trees_500_4",
            0.6, 0.7,
            ['Chi2/Ndof/Nlayer', 'Dxy1/DxyError1', 'Dz1/DzError1', 'NHit', 'Nlayer', 'Eta']
            )
setupforest(process.hiDetachedTripletStepSelector, 
            "BDTG_algo_7_trees_500_4",
            -0.1, 0.0,
            ['Chi2/Ndof/Nlayer', 'NHit', 'Nlayer', 'Eta']
            )
