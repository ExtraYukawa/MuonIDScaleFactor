# Muon ID Scale Factor

## Installation instructions (Under afs)

These installation instructions correspond to the muon ID scale factor production.
To install, execute the following in your work area (need to be under afs, due to some condor issue).

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_16
cd CMSSW_10_6_16/src
cmsenv
git cms-init
git clone https://github.com/AlbertHsuNTUphys/MuonIDScaleFactor.git
cd MuonIDScaleFactor/
```

## Download Tag and Probe ntuples
Download the tag and probe ntuples. 
```
sh Download_ntuple.sh [Store directory]
```
## Flatten ntuples
In this part, we put on the tag muon & probe muon selectoins to produce our own flatten root files. You need to change the source directory (The one where you download ntuples to in previous part.) in makehist.py.
```
# Test locally
python makehist.py --era 2017 --outDir ./ --shift puWeightUp --NLO 0 --ptbin 0 --etabin 0
# Submit to condor
python runCondor.py
# Check condor process
condor_q
```
## Tag and Probe Analysis
After producing the flatten root files. We can do tag and probe analysis to get muon ID scale factor (ID+ISO SF actually).
```
python muSF.py
```

