import ROOT
import time
import os
import sys
import optparse
import subprocess

def get_fname(era = '2017',isNLO = False):

  SingleMuon_names = ROOT.std.vector('string')()
  DY_name   = ROOT.std.vector('string')()
  path_data = "/eos/user/t/tihsu/TnP_muon_ntuple/"
  path_mc   = "/eos/user/t/tihsu/TnP_muon_ntuple/"
  if isNLO:
    path_mc += "NLO/"
  dirs_data = os.listdir(path_data)
  dirs_mc   = os.listdir(path_mc)
  for fname in dirs_data:
    if ('SingleMuon' in fname) and (era in fname):
      SingleMuon_names.push_back(path_data+fname)
  for fname in dirs_mc:
    if ('DY' in fname) and (era in fname):
      DY_name.push_back(path_mc+fname)
  
  return SingleMuon_names,DY_name

def get_mcEventnumber(filename):
  print 'opening file ', filename
  nevent_temp=0
  for i in range(0,len(filename)):
    ftemp = ROOT.TFile.Open(filename[i])
    htemp = ftemp.Get('Events')
    nevent_temp += htemp.GetEntriesFast()
  return nevent_temp

def makehist(ptbin, etabin, SingleMuon_names, DY_name, puWeight='puWeight',outputdir='./'):

  
  lumi = 41480.

  DY_xs = 6077.22
  DY_ev = get_mcEventnumber(DY_name)

  filters_tag="Tag_pt > 26 && abs(Tag_eta) < 2.4 && abs(Tag_dxy) < 0.05 && abs(Tag_dz)<0.1 && Tag_tightId && Tag_pfRelIso04_all<0.2"
  filters_other="TnP_mass>60 && TnP_mass<120 && abs(Probe_eta)<2.4 && Probe_pt>10 && TnP_trigger"
  filters_probe="Probe_sip3d<8 && abs(Probe_dxy)<0.05 && abs(Probe_dz)<0.1 && Probe_miniPFRelIso_all<0.4 && Probe_mediumId && Probe_mvaTTH>-0.2 && Probe_tightCharge==2"
  antifilters_probe="!(Probe_sip3d<8 && abs(Probe_dxy)<0.05 && abs(Probe_dz)<0.1 && Probe_miniPFRelIso_all<0.4 && Probe_mediumId && Probe_mvaTTH>-0.2 && Probe_tightCharge==2)"

  filters_pass=filters_tag+" && " + filters_other+ " && " +filters_probe
  filters_fail=filters_tag+" && " + filters_other+ " && " +antifilters_probe

  eta_bin=[0.0, 0.8, 1.4442, 1.566, 2.0, 2.5]
  etabin_names=['m0p0','p0p8','p1p4442','p1p566','p2p0','p2p5']
  pt_bin=[10,20,35,50,100,200,500]
  ptbin_names=['10','20','35','50','100','200','500']

  outputname=outputdir+'Pt'+ptbin_names[ptbin]+'To'+ptbin_names[ptbin+1]+'Eta'+etabin_names[etabin]+'To'+etabin_names[etabin+1]+'.root'
  fileout=ROOT.TFile(outputname,"RECREATE")

  filters_pass_final=filters_pass+ "&& Probe_pt>" + str(pt_bin[ptbin]) + " && Probe_pt<" +str(pt_bin[ptbin+1])+"&& abs(Probe_eta)<" +str(eta_bin[etabin+1]) + " && abs(Probe_eta)>" + str(eta_bin[etabin])
  filters_fail_final=filters_fail+ "&& Probe_pt>" + str(pt_bin[ptbin]) + " && Probe_pt<" +str(pt_bin[ptbin+1])+"&& abs(Probe_eta)<" +str(eta_bin[etabin+1]) + " && abs(Probe_eta)>" + str(eta_bin[etabin])
  title_pass_temp="Pass_eta"+etabin_names[etabin]+"To"+etabin_names[etabin+1]+"pt"+ptbin_names[ptbin]+"To"+ptbin_names[ptbin+1]
  title_fail_temp="Fail_eta"+etabin_names[etabin]+"To"+etabin_names[etabin+1]+"pt"+ptbin_names[ptbin]+"To"+ptbin_names[ptbin+1]

  df_DY_tree_pass = ROOT.RDataFrame("Events",DY_name)
  df_DY_pass = df_DY_tree_pass.Filter(filters_pass_final)
  df_DY_pass_histo = df_DY_pass.Histo1D(("TnP_mass_DYpass",title_pass_temp ,60,60,120), "TnP_mass",puWeight)

  df_DY_tree_fail = ROOT.RDataFrame("Events",DY_name)
  df_DY_fail = df_DY_tree_fail.Filter(filters_fail_final)
  df_DY_fail_histo = df_DY_fail.Histo1D(("TnP_mass_DYfail",title_fail_temp ,60,60,120), "TnP_mass",puWeight)

  df_SingleMuon_tree_pass = ROOT.RDataFrame("Events", SingleMuon_names)
  df_SingleMuon_pass = df_SingleMuon_tree_pass.Filter(filters_pass_final)
  df_SingleMuon_pass_histo = df_SingleMuon_pass.Histo1D(("TnP_mass_Muonpass",title_pass_temp,60,60,120), "TnP_mass")

  df_SingleMuon_tree_fail = ROOT.RDataFrame("Events", SingleMuon_names)
  df_SingleMuon_fail = df_SingleMuon_tree_fail.Filter(filters_fail_final)
  df_SingleMuon_fail_histo = df_SingleMuon_fail.Histo1D(("TnP_mass_Muonfail",title_fail_temp,60,60,120), "TnP_mass")

  df_DY_pass_histo.Draw()
  df_DY_fail_histo.Draw()
  df_SingleMuon_pass_histo.Draw()
  df_SingleMuon_fail_histo.Draw()

  fileout.cd()
  df_DY_pass_histo.Write()
  df_DY_fail_histo.Write()
  df_SingleMuon_pass_histo.Write()
  df_SingleMuon_fail_histo.Write()

  fileout.Close()

if __name__ == "__main__":
 
# Configuration
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e','--era', dest='era', help='era: 2017/2018', default='2017', type='string')
  parser.add_option('-o','--outDir', dest='outDir', help='output directory', default=None, type='string')
  parser.add_option('-s','--shift', dest='shift', help='puWeight shift= puWeight/puWeightUp/puWeightDown', default='puWeight', type='string')
  parser.add_option('-n','--NLO', dest='NLO', help='NLO/LO samples', default=False, type='int')
  parser.add_option('-p','--ptbin', dest='ptbin', help='index of ptbin', default=0, type='int')
  parser.add_option('-t','--etabin', dest='etabin', help='index of etabin', default=0, type='int')
  (args,opt) = parser.parse_args()
  start = time.time()
  start1 = time.clock()
  SingleMuon_names, DY_name = get_fname(era=args.era, isNLO=args.NLO)
  makehist(args.ptbin,args.etabin,SingleMuon_names,DY_name,args.shift,args.outDir)
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

