import os
import sys
import optparse
import subprocess

def prepare_shell(era,shift,NLO,ptbin,etabin,condor,FarmDir):
  NLOname = "NLO" if NLO else "LO"
  cmsswBase=os.environ['CMSSW_BASE']
  OutDir = "%s/src/MuonIDScaleFactor/flatten/%s/%s/%s/"%(cmsswBase,era,shift,NLOname)
  os.system('mkdir -p %s'%OutDir)
  os.system('rm %s/*.root'%OutDir)
  shell_name = "%s_%s_%s_%s_%s.sh"%(era,shift,NLOname,str(ptbin),str(etabin))
  with open('%s/%s'%(FarmDir,shell_name),'w') as shell:
    shell.write('#!/bin/bash\n')
    shell.write('WORKDIR=`pwd`\n')
    shell.write('cd %s\n'%cmsswBase)
    shell.write('eval `scram r -sh`\n')
    shell.write('cd ${WORKDIR}\n')
    shell.write('python %s/src/MuonIDScaleFactor/makehist.py '%cmsswBase)
    shell.write('--era %s '%era)
    shell.write('--outDir %s '%OutDir)
    shell.write('--shift %s '%shift)
    shell.write('--NLO %d '%NLO)
    shell.write('--ptbin %d '%ptbin)
    shell.write('--etabin %d '%etabin)
  condor.write('cfgFile=%s\n'%shell_name)
  condor.write('queue 1\n')


if __name__=='__main__':
  FarmDir = os.environ['CMSSW_BASE']+"/Farm/"
  os.system('mkdir -p %s'%FarmDir)
  os.system('rm %s/*'%FarmDir)
 
  condor = open('%s/condor.sub'%FarmDir,'w')
  condor.write('output = %s/job_common.out\n'%FarmDir)
  condor.write('error  = %s/job_common.err\n'%FarmDir)
  condor.write('log    = %s/job_common.log\n'%FarmDir)
  condor.write('executable = %s/$(cfgFile)\n'%FarmDir)
  condor.write('requirements = (OpSysAndVer =?= "CentOS7")\n')
  condor.write('+JobFlavour = "tomorrow"\n')
  condor.write('+MaxRuntime = 7200\n')

  Eras = ['2016','apv2016','2017','2018']
  shifts = ['puWeightUp','puWeight','puWeightDown']
  NLOs = [0,1]
  ptbins = range(6)
  etabins = range(5)

  for era in Eras:
    for shift in shifts:
      for NLO in NLOs:
        for ptbin in ptbins:
          for etabin in etabins:
            prepare_shell(era,shift,NLO,ptbin,etabin,condor,FarmDir)

  condor.close()
  os.system('condor_submit %s/condor.sub'%FarmDir)
