from RecoTracker.IterativeTracking.DetachedTripletStep_cff import *
from HIPixelTripletSeeds_cff import *
from HIPixel3PrimTracks_cfi import *
from hiSecondPixelTripletStep_cff import *

#hidetachedTripletStepClusters = detachedTripletStepClusters.clone()
#hidetachedTripletStepSeedLayers = detachedTripletStepSeedLayers.clone()
#hidetachedTripletStepSeeds = detachedTripletStepSeeds.clone()
#hidetachedTripletStepTrackCandidates = detachedTripletStepTrackCandidates.clone()
#hidetachedTripletStepTracks = detachedTripletStepTracks.clone()
#hidetachedTripletStepSelector = detachedTripletStepSelector.clone()
#hidetachedTripletQual = detachedTripletStep.clone()


#?hidetachedTripletStepClusters.oldClusterRemovalInfo = cms.InputTag('hiPixelPairClusters')

hiDetachedClusters = cms.EDProducer("HITrackClusterRemover",
     clusterLessSolution = cms.bool(True),
     trajectories = cms.InputTag("hiPixelPairGlobalPrimTracks"),
     overrideTrkQuals = cms.InputTag('hiPixelPairStepSelector','hiPixelPairStep'),
     TrackQuality = cms.string('highPurity'),
     minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
     pixelClusters = cms.InputTag("siPixelClusters"),
     stripClusters = cms.InputTag("siStripClusters"),
     Common = cms.PSet(
         maxChi2 = cms.double(9.0),
     ),
     Strip = cms.PSet(
        #Yen-Jie's mod to preserve merged clusters
        maxSize = cms.uint32(2),
        maxChi2 = cms.double(9.0)
     )

)




# SEEDING LAYERS
import RecoTracker.TkSeedingLayers.PixelLayerTriplets_cfi
hiDetachedSeedLayers = RecoTracker.TkSeedingLayers.PixelLayerTriplets_cfi.PixelLayerTriplets.clone()
hiDetachedSeedLayers.BPix.skipClusters = cms.InputTag('hiDetachedClusters')
hiDetachedSeedLayers.FPix.skipClusters = cms.InputTag('hiDetachedClusters')

# SEEDS
from RecoPixelVertexing.PixelTriplets.PixelTripletHLTGenerator_cfi import *
from RecoPixelVertexing.PixelLowPtUtilities.ClusterShapeHitFilterESProducer_cfi import *
from RecoHI.HiTracking.HIPixelTrackFilter_cfi import *
from RecoHI.HiTracking.HITrackingRegionProducer_cfi import *
hiDetachedPixelTracks = cms.EDProducer("PixelTrackProducer",

    passLabel  = cms.string('Pixel detached tracks with vertex constraint'),

    # Region
    RegionFactoryPSet = cms.PSet(
	  ComponentName = cms.string("GlobalTrackingRegionWithVerticesProducer"),
	  RegionPSet = cms.PSet(
                HiTrackingRegionWithVertexBlock
	  )
    ),
     
    # Ordered Hits
    OrderedHitsFactoryPSet = cms.PSet( 
          ComponentName = cms.string( "StandardHitTripletGenerator" ),
	  SeedingLayers = cms.InputTag( "PixelLayerTriplets" ),
          GeneratorPSet = cms.PSet( 
		PixelTripletHLTGenerator
          )
    ),
	
    # Fitter
    FitterPSet = cms.PSet( 
	  ComponentName = cms.string('PixelFitterByHelixProjections'),
	  TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelTriplets')
    ),
	
    # Filter
    useFilterWithES = cms.bool( True ),
    FilterPSet = cms.PSet( 
          HiFilterBlock
    ),
	
    # Cleaner
    CleanerPSet = cms.PSet(  
          ComponentName = cms.string( "TrackCleaner" )
    )
)



hiDetachedPixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.extraHitRPhitolerance = cms.double(0.0)
hiDetachedPixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.extraHitRZtolerance = cms.double(0.0)
#hiDetachedPixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.SeedingLayers = cms.InputTag('hiDetachedSeedLayers')
hiDetachedPixelTracks.OrderedHitsFactoryPSet.SeedingLayers = cms.InputTag('hiDetachedSeedLayers')



minPt = 0.95
sv = 0.5
hiDetachedPixelTracks.RegionFactoryPSet = cms.PSet(
        ComponentName = cms.string('GlobalTrackingRegionWithVerticesProducer'),
        RegionPSet = cms.PSet(
            precise = cms.bool(True),
            beamSpot = cms.InputTag("offlineBeamSpot"),
            useFixedError = cms.bool(True),
            nSigmaZ = cms.double(4.0),
            sigmaZVertex = cms.double(4.0),
            fixedError = cms.double(sv),
            VertexCollection = cms.InputTag("hiSelectedVertex"),
            ptMin = cms.double(minPt),
            useFoundVertices = cms.bool(True),
            originRadius = cms.double(sv)
        )
)
hiDetachedPixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.maxElement = cms.uint32(1000000)

#try tracks!!!
#hidetachedPixelTracks = hiPixel3PrimTracks.clone()
#hidetachedPixelTracks.OrderedHitsFactoryPSet = hidetachedTripletStepSeeds.OrderedHitsFactoryPSet
#hidetachedPixelTracks.RegionFactoryPSet = hidetachedTripletStepSeeds.RegionFactoryPSet
hiDetachedPixelTracks.FilterPSet.ptMin = cms.double(minPt)
hiDetachedPixelTracks.FilterPSet.lipMax = cms.double(sv)
hiDetachedPixelTracks.FilterPSet.tipMax = cms.double(sv)
hiDetachedPixelTracks.FilterPSet.nSigmaTipMaxTolerance = cms.double(0)
hiDetachedPixelTracks.FilterPSet.tiplipMin = cms.double(0)
hiDetachedPixelTracks.FilterPSet.useClusterShape = cms.bool(True)


hiDetachedPixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.SeedComparitorPSet = RecoPixelVertexing.PixelLowPtUtilities.LowPtClusterShapeSeedComparitor_cfi.LowPtClusterShapeSeedComparitor


#hidetachedPixelTrackSeeds = hiPixelTrackSeeds.clone()
#hidetachedPixelTrackSeeds.InputCollection = cms.InputTag("hidetachedPixelTracks")
#hiSecondPixelTripletTrackCandidates.src=cms.InputTag("hidetachedPixelTrackSeeds") #below

import RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi
hiDetachedSeeds = RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi.pixelTrackSeeds.clone(
        InputCollection = 'hiDetachedPixelTracks'
  )

#hiDetachedSeeds.ClusterCheckPSet.MaxNumberOfCosmicClusters = cms.uint32(50000000)
#hiDetachedSeeds.ClusterCheckPSet.MaxNumberOfPixelClusters = cms.uint32(5000000)



#????????hidetachedTripletStepSeeds.SeedComparitorPSet = .... cms.string('PixelClusterShapeSeedComparitor'),
#change region and to trackseeds!

#hidetachedTripletStepTrajectoryFilter = detachedTripletStepTrajectoryFilter.clone()
#hidetachedTripletStepTrajectoryFilter.ComponentName='hidetachedTripletStepTrajectoryFilter'
#hidetachedTripletStepTrajectoryFilter.filterPset.minPt = cms.double(minPt)

#hidetachedTripletStepChi2Est = detachedTripletStepChi2Est.clone()
#hidetachedTripletStepChi2Est.ComponentName = 'hidetachedTripletStepChi2Est'

#hidetachedTripletStepTrajectoryBuilder = detachedTripletStepTrajectoryBuilder.clone()
#hidetachedTripletStepTrajectoryBuilder.ComponentName='hidetachedTripletStepTrajectoryBuilder'
#hidetachedTripletStepTrajectoryBuilder.trajectoryFilterName='hidetachedTripletStepTrajectoryFilter'
#hidetachedTripletStepTrajectoryBuilder.estimator = 'hidetachedTripletStepChi2Est'



# QUALITY CUTS DURING TRACK BUILDING
import TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff
hiDetachedTrajectoryFilter = TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff.CkfBaseTrajectoryFilter_block.clone(
    maxLostHits = 999, #1?
    minimumNumberOfHits = 6,
    minPt = cms.double(minPt),
    constantValueForLostHitsFractionFilter = cms.double(0.701) #1.0?
    )

import TrackingTools.KalmanUpdators.Chi2MeasurementEstimatorESProducer_cfi
hiDetachedChi2Est = TrackingTools.KalmanUpdators.Chi2MeasurementEstimatorESProducer_cfi.Chi2MeasurementEstimator.clone(
        ComponentName = cms.string('hiDetachedChi2Est'),
            nSigma = cms.double(3.0),
            MaxChi2 = cms.double(9.0)
        )




#hidetachedTripletStepTrackCandidates.TrajectoryBuilder = cms.string('hidetachedTripletStepTrajectoryBuilder')
#hidetachedTripletStepTrackCandidates.clustersToSkip='hidetachedTripletStepClusters'
#hidetachedTripletStepTrackCandidates.src = cms.InputTag("hidetachedTripletStepSeeds")
#hidetachedTripletStepTrackCandidates.src = cms.InputTag("hidetachedPixelTrackSeeds")

#hidetachedTripletStepTracks.src = cms.InputTag('hidetachedTripletStepTrackCandidates')


# TRACK BUILDING
import RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi
hiDetachedTrajectoryBuilder = RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi.GroupedCkfTrajectoryBuilder.clone(
    MeasurementTrackerName = '',
    trajectoryFilter = cms.PSet(refToPSet_ = cms.string('hiDetachedTrajectoryFilter')),
    maxCand = 2, #3?
    estimator = cms.string('hiDetachedChi2Est'),
    maxDPhiForLooperReconstruction = cms.double(0),
    maxPtForLooperReconstruction = cms.double(0),
    alwaysUseInvalidHits = cms.bool(False)
    )

# MAKING OF TRACK CANDIDATES
import RecoTracker.CkfPattern.CkfTrackCandidates_cfi
hiDetachedTrackCandidates = RecoTracker.CkfPattern.CkfTrackCandidates_cfi.ckfTrackCandidates.clone(
    src = cms.InputTag('hiDetachedSeeds'),
    ### these two parameters are relevant only for the CachingSeedCleanerBySharedInput
    numHitsForSeedCleaner = cms.int32(50),
    onlyPixelHitsForSeedCleaner = cms.bool(True),
    TrajectoryBuilderPSet = cms.PSet(refToPSet_ = cms.string('hiDetachedTrajectoryBuilder')),
    TrajectoryBuilder = cms.string('hiDetachedTrajectoryBuilder'),
    clustersToSkip = cms.InputTag('hiDetachedClusters'),
    doSeedingRegionRebuilding = True,
    useHitsSplitting = True
    )


# TRACK FITTING
import RecoTracker.TrackProducer.TrackProducer_cfi
hiDetachedTracks = RecoTracker.TrackProducer.TrackProducer_cfi.TrackProducer.clone(
    src = 'hiDetachedTrackCandidates',
    AlgorithmName = cms.string('detachedStep'),
    Fitter=cms.string('FlexibleKFFittingSmoother')
    )



#hidetachedTripletStepSelector.vertices = cms.InputTag("hiSelectedVertex")
#hidetachedTripletStepSelector.src=cms.InputTag("hidetachedTripletStepTracks")

#for sel in hidetachedTripletStepSelector.trackSelectors:
#    sel.name=cms.string('hi'+sel.name.value())
#    if (sel.preFilterName.value()!=''): sel.preFilterName=cms.string('hi'+sel.preFilterName.value())

# Final selection
import RecoHI.HiTracking.hiMultiTrackSelector_cfi
hiDetachedSelector = RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiMultiTrackSelector.clone(
    src='hiDetachedTracks',
    trackSelectors= cms.VPSet(
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiLooseMTS.clone(
    name = 'hiDetachedLoose',
    ), #end of pset
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiTightMTS.clone(
    name = 'hiDetachedTight',
    preFilterName = 'hiDetachedLoose',
    ),
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiHighpurityMTS.clone(
    name = 'hiDetachedStep',
    preFilterName = 'hiDetachedTight',
    # min_nhits = 14
    ),
    ) #end of vpset
    ) #end of clone

#check if that is necessary
hiDetachedSelector.trackSelectors[0].d0_par2=cms.vdouble(99999.0,99999.0)
hiDetachedSelector.trackSelectors[1].d0_par2=cms.vdouble(99999.0,99999.0)
hiDetachedSelector.trackSelectors[2].d0_par2=cms.vdouble(99999.0,99999.0)

hiDetachedSelector.trackSelectors[0].dz_par2=cms.vdouble(99999.0,99999.0)
hiDetachedSelector.trackSelectors[1].dz_par2=cms.vdouble(99999.0,99999.0)
hiDetachedSelector.trackSelectors[2].dz_par2=cms.vdouble(99999.0,99999.0)




#hidetachedTripletQual.selectedTrackQuals=cms.VInputTag(cms.InputTag("hidetachedTripletStepSelector","hidetachedTripletStepVtx"), 
#                                                               cms.InputTag("hidetachedTripletStepSelector","hidetachedTripletStepTrk"))
#hidetachedTripletQual.TrackProducers=cms.VInputTag(cms.InputTag("hidetachedTripletStepTracks"), cms.InputTag("hidetachedTripletStepTracks"))




import RecoTracker.FinalTrackSelectors.trackListMerger_cfi
hiDetachedQual = RecoTracker.FinalTrackSelectors.trackListMerger_cfi.trackListMerger.clone(
    TrackProducers=cms.VInputTag(cms.InputTag('hiDetachedTracks')),
    hasSelector=cms.vint32(1),
    selectedTrackQuals = cms.VInputTag(cms.InputTag("hiSecondPixelTripletStepSelector","hiDetachedHighPurity")),
    copyExtras = True,
    makeReKeyedSeeds = cms.untracked.bool(False),
    #writeOnlyTrkQuals = True
    )


hiDetachedStep = cms.Sequence(hiDetachedClusters*
                                     hiDetachedSeedLayers*
                                     #hidetachedTripletStepSeeds*
                                     hiDetachedPixelTracks*
                                     hiDetachedSeeds*
                                     hiDetachedTrackCandidates*
                                     hiDetachedTracks*
                                     hiDetachedSelector*
                                     hiDetachedQual)


