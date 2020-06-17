# ConvertMergeVCF
##This repository contains python scripts that utilize the liftOver python package to Convert VCF.gz files aligned to hg19 and align them to hg38, then merge the resulting file with another VCF.gz aligned to hg38.  

###CovertMergeHg19toHg38.py usage:

python ConvertMergeHg19toHg38.py "input VCF.gz hg19" "input VCF.gz hg38" "output VCF hg38"

ex. python ConvertMergeHg19toHg38.py 1chr22hg19.VCF.gz 2chr22hg38.VCF.gz outchr22hg38.vcf
