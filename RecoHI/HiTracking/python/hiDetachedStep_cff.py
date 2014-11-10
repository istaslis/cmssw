from RecoTracker.IterativeTracking.DetachedTripletStep_cff import *
from HIPixelTripletSeeds_cff import *
from HIPixel3PrimTracks_cfi import *
from hiSecondPixelTripletStep_cff import *

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

hiDetachedPixelTracks.FilterPSet.ptMin = cms.double(minPt)
hiDetachedPixelTracks.FilterPSet.lipMax = cms.double(sv)
hiDetachedPixelTracks.FilterPSet.tipMax = cms.double(sv)
hiDetachedPixelTracks.FilterPSet.nSigmaTipMaxTolerance = cms.double(0)
hiDetachedPixelTracks.FilterPSet.tiplipMin = cms.double(0)
hiDetachedPixelTracks.FilterPSet.useClusterShape = cms.bool(True)


hiDetachedPixelTracks.OrderedHitsFactoryPSet.GeneratorPSet.SeedComparitorPSet = RecoPixelVertexing.PixelLowPtUtilities.LowPtClusterShapeSeedComparitor_cfi.LowPtClusterShapeSeedComparitor

import RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi
hiDetachedSeeds = RecoPixelVertexing.PixelLowPtUtilities.TrackSeeds_cfi.pixelTrackSeeds.clone(
        InputCollection = 'hiDetachedPixelTracks'
  )

# QUALITY CUTS DURING TRACK BUILDING
import TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff
hiDetachedTrajectoryFilter = TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff.CkfBaseTrajectoryFilter_block.clone(
    maxLostHits = 999,
    minimumNumberOfHits = 6,
    minPt = cms.double(minPt),
    constantValueForLostHitsFractionFilter = cms.double(0.701)
    )

import TrackingTools.KalmanUpdators.Chi2MeasurementEstimatorESProducer_cfi
hiDetachedChi2Est = TrackingTools.KalmanUpdators.Chi2MeasurementEstimatorESProducer_cfi.Chi2MeasurementEstimator.clone(
        ComponentName = cms.string('hiDetachedChi2Est'),
            nSigma = cms.double(3.0),
            MaxChi2 = cms.double(9.0)
        )


# TRACK BUILDING
import RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi
hiDetachedTrajectoryBuilder = RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi.GroupedCkfTrajectoryBuilder.clone(
    MeasurementTrackerName = '',
    trajectoryFilter = cms.PSet(refToPSet_ = cms.string('hiDetachedTrajectoryFilter')),
    maxCand = 2,
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

# Final selection
import RecoHI.HiTracking.hiMultiTrackSelector_cfi
hiDetachedSelector = RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiMultiTrackSelector.clone(
    src='hiDetachedTracks',
    trackSelectors= cms.VPSet(
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiLooseMTS.clone(
    name = 'hiDetachedLoose',
    applyAdaptedPVCuts = cms.bool(False)
    ), #end of pset
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiTightMTS.clone(
    name = 'hiDetachedTight',
    preFilterName = 'hiDetachedLoose',
    applyAdaptedPVCuts = cms.bool(False)
    ),
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiHighpurityMTS.clone(
    name = 'hiDetachedStep',
    preFilterName = 'hiDetachedTight',
    applyAdaptedPVCuts = cms.bool(False)
    # min_nhits = 14
    ),
    ) #end of vpset
    ) #end of clone

import RecoTracker.FinalTrackSelectors.trackListMerger_cfi
hiDetachedQual = RecoTracker.FinalTrackSelectors.trackListMerger_cfi.trackListMerger.clone(
    TrackProducers=cms.VInputTag(cms.InputTag('hiDetachedTracks')),
    hasSelector=cms.vint32(1),
    selectedTrackQuals = cms.VInputTag(cms.InputTag("hiSecondPixelTripletStepSelector","hiDetachedHighPurity")),
    copyExtras = True,
    makeReKeyedSeeds = cms.untracked.bool(False),
    )


hiDetachedStep = cms.Sequence(hiDetachedClusters*
                                     hiDetachedSeedLayers*
                                     hiDetachedPixelTracks*
                                     hiDetachedSeeds*
                                     hiDetachedTrackCandidates*
                                     hiDetachedTracks*
                                     hiDetachedSelector*
                                     hiDetachedQual)


