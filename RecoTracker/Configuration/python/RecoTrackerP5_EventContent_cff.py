# The following comments couldn't be translated into the new config version:

#Tracks

#Tracks

#Tracks without extra and hits

import FWCore.ParameterSet.Config as cms

#Full Event content 
RecoTrackerFEVT = cms.PSet(
    outputCommands = cms.untracked.vstring('keep recoTracks_ctfWithMaterialTracksP5_*_*', 
        'keep recoTrackExtras_ctfWithMaterialTracksP5_*_*', 
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksP5_*_*', 
        'keep recoTracks_rsWithMaterialTracksP5_*_*', 
        'keep recoTrackExtras_rsWithMaterialTracksP5_*_*', 
        'keep TrackingRecHitsOwned_rsWithMaterialTracksP5_*_*', 
        'keep recoTracks_cosmictrackfinderP5_*_*', 
        'keep recoTrackExtras_cosmictrackfinderP5_*_*', 
        'keep TrackingRecHitsOwned_cosmictrackfinderP5_*_*',
        'keep recoTracks_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep recoTrackExtras_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep recoTracks_splittedTracksP5_*_*',
        'keep recoTrackExtras_splittedTracksP5_*_*',
        'keep TrackingRecHitsOwned_splittedTracksP5_*_*',                                           
        'keep *_dedxTruncated40_*_*',
        'keep *_dedxMedian_*_*',
        'keep *_dedxHarmonic2_*_*',
        'keep *_dedxTruncated40CTF_*_*',
        'keep *_dedxMedianCTF_*_*',
        'keep *_dedxHarmonic2CTF_*_*',
        'keep *_dedxTruncated40RS_*_*',
        'keep *_dedxMedianRS_*_*',
        'keep *_dedxHarmonic2RS_*_*',
        'keep *_dedxTruncated40CosmicTF_*_*',
        'keep *_dedxMedianCosmicTF_*_*',
        'keep *_dedxHarmonic2CosmicTF_*_*',
    )
)
#RECO content
RecoTrackerRECO = cms.PSet(
    outputCommands = cms.untracked.vstring('keep recoTracks_ctfWithMaterialTracksP5_*_*', 
        'keep recoTrackExtras_ctfWithMaterialTracksP5_*_*', 
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksP5_*_*', 
        'keep recoTracks_rsWithMaterialTracksP5_*_*', 
        'keep recoTrackExtras_rsWithMaterialTracksP5_*_*', 
        'keep TrackingRecHitsOwned_rsWithMaterialTracksP5_*_*', 
        'keep recoTracks_cosmictrackfinderP5_*_*', 
        'keep recoTrackExtras_cosmictrackfinderP5_*_*', 
        'keep TrackingRecHitsOwned_cosmictrackfinderP5_*_*',
        'keep recoTracks_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep recoTrackExtras_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep TrackingRecHitsOwned_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep recoTracks_splittedTracksP5_*_*',
        'keep recoTrackExtras_splittedTracksP5_*_*',
        'keep TrackingRecHitsOwned_splittedTracksP5_*_*',                                           
        'keep *_dedxTruncated40_*_*',
        'keep *_dedxMedian_*_*',
        'keep *_dedxHarmonic2_*_*',
        'keep *_dedxTruncated40CTF_*_*',
        'keep *_dedxMedianCTF_*_*',
        'keep *_dedxHarmonic2CTF_*_*',
        'keep *_dedxTruncated40RS_*_*',
        'keep *_dedxMedianRS_*_*',
        'keep *_dedxHarmonic2RS_*_*',
        'keep *_dedxTruncated40CosmicTF_*_*',
        'keep *_dedxMedianCosmicTF_*_*',
        'keep *_dedxHarmonic2CosmicTF_*_*',
    )
)
#AOD content
RecoTrackerAOD = cms.PSet(
    outputCommands = cms.untracked.vstring('keep recoTracks_ctfWithMaterialTracksP5_*_*', 
        'keep recoTracks_rsWithMaterialTracksP5_*_*', 
        'keep recoTracks_cosmictrackfinderP5_*_*',
        'keep recoTracks_ctfWithMaterialTracksBeamHaloMuon_*_*',
        'keep recoTracks_splittedTracksP5_*_*',
        'keep *_dedxTruncated40_*_*',
        'keep *_dedxMedian_*_*',
        'keep *_dedxHarmonic2_*_*',
        'keep *_dedxTruncated40CTF_*_*',
        'keep *_dedxMedianCTF_*_*',
        'keep *_dedxHarmonic2CTF_*_*',
        'keep *_dedxTruncated40RS_*_*',
        'keep *_dedxMedianRS_*_*',
        'keep *_dedxHarmonic2RS_*_*',
        'keep *_dedxTruncated40CosmicTF_*_*',
        'keep *_dedxMedianCosmicTF_*_*',
        'keep *_dedxHarmonic2CosmicTF_*_*',
    )
)

