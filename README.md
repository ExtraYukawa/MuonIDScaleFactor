# Muon ID Scale Factor

## Installation instructions (Under Lxplus)

These installation instructions correspond to the muon ID scale factor production.
To install, execute the following in your work area (need under lxplus, due to some condor issue).

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
Download the tag and probe ntuples. Suggest to download to eos directory.
``
sh Download_ntuple.sh [Store directory]
```


