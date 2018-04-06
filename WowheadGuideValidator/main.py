import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError
from SEOValidator import SEOValidator
         
validator = SEOValidator()

results = 'Spec\tOverview\tTalents\tRotation\tArtifact\tGear\tStat\tEnhancements\tMacros\tLeveling\n'
issues = []

#title, content = validator.dataFetch('Hunter', 'Beast Mastery', 'guide')

for combo in validator.classSpecCombos():
    res, iss = validator.seoAnalysis(combo[1],combo[0])
    results += '{1} {0}\t{2}\n'.format(combo[0], combo[1], res)
    issues += iss
    if iss:
        issues.append('\n')
        

with open('seo_results.csv', 'w') as f:
    f.write('\n'.join((results, '\n'.join(issues))))
    #f.write(title + '\n' + content)


