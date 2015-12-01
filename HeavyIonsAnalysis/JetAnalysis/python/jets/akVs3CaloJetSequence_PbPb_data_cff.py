

import FWCore.ParameterSet.Config as cms
from HeavyIonsAnalysis.JetAnalysis.patHeavyIonSequences_cff import patJetGenJetMatch, patJetPartonMatch, patJetCorrFactors, patJets
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

akVs3Calomatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVs3CaloJets"),
    matched = cms.InputTag("ak3HiGenJets"),
    maxDeltaR = 0.3
    )

akVs3Caloparton = patJetPartonMatch.clone(src = cms.InputTag("akVs3CaloJets"),
                                                        matched = cms.InputTag("genParticles")
                                                        )

akVs3Calocorr = patJetCorrFactors.clone(
    useNPV = False,
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),
    src = cms.InputTag("akVs3CaloJets"),
    payload = "AK3Calo_offline"
    )

akVs3CalopatJets = patJets.clone(jetSource = cms.InputTag("akVs3CaloJets"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVs3Calocorr")),
                                               genJetMatch = cms.InputTag("akVs3Calomatch"),
                                               genPartonMatch = cms.InputTag("akVs3Caloparton"),
                                               jetIDMap = cms.InputTag("akVs3CaloJetID"),
                                               addBTagInfo         = False,
                                               addTagInfos         = False,
                                               addDiscriminators   = False,
                                               addAssociatedTracks = False,
                                               addJetCharge        = False,
                                               addJetID            = False,
                                               getJetMCFlavour     = False,
                                               addGenPartonMatch   = False,
                                               addGenJetMatch      = False,
                                               embedGenJetMatch    = False,
                                               embedGenPartonMatch = False,
                                               # embedCaloTowers     = False,
                                               # embedPFCandidates = False
				            )

akVs3CaloJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVs3CalopatJets"),
                                                             genjetTag = 'ak3HiGenJets',
                                                             rParam = 0.3,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJets',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
                                                             genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator")
                                                             )

akVs3CaloJetSequence_mc = cms.Sequence(
						  akVs3Calomatch
                                                  *
                                                  akVs3Caloparton
                                                  *
                                                  akVs3Calocorr
                                                  *
                                                  akVs3CalopatJets
                                                  *
                                                  akVs3CaloJetAnalyzer
                                                  )

akVs3CaloJetSequence_data = cms.Sequence(akVs3Calocorr
                                                    *
                                                    akVs3CalopatJets
                                                    *
                                                    akVs3CaloJetAnalyzer
                                                    )

akVs3CaloJetSequence_jec = cms.Sequence(akVs3CaloJetSequence_mc)
akVs3CaloJetSequence_mix = cms.Sequence(akVs3CaloJetSequence_mc)

akVs3CaloJetSequence = cms.Sequence(akVs3CaloJetSequence_data)
