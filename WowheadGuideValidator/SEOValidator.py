import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen, urlcleanup
from urllib.error import URLError
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import copy
import re
import string


class SEOValidator:    

    def __init__(self):
        self.file = 'options.json'
        self.options = {}
        self.loadOptions()
        self.loop = 0
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")

        #chrome driver from https://sites.google.com/a/chromium.org/chromedriver/home
        self.chrome_driver = os.getcwd() +"\\chromedriver.exe"        
      
    def loadOptions(self):
        try:
            with open(self.file, 'r') as f:
                s = f.read()
                self.options = json.loads(s)
        except Exception:
            print(self.file+' not found')
            return

    def seoAnalysis(self, charClass, charSpec):
    
        # Retrieves all guides that it should analyze
        guideTypes = self.options['guidesTypes']
        guides = guideTypes.split(',')
        
        result = ''
        issues = []
        
        # For each guide, call its own analysis method
        for guide in guides:
            analysis = getattr(self, 'seoGuideAnalysis_' + guide.replace('-','_') )
            res, iss = analysis(charClass, charSpec)
            result += res + '\t'
            issues += iss
        
        return result, issues
        
    def seoGuideAnalysis_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Overview Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Guide – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Guide - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Overview Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Overview Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} guide'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Overview Guide', 3 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
            
    def seoGuideAnalysis_talent_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Talent Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Talent Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Talents & Build Guide – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Talents & Build Guide - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Talent Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Talent Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} talent'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Talent Guide', 2 )
        guideFormat = '{0} {1} build'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Talent Guide', 2 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_simple_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Simple Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Simple Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Quick Start Guide – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Quick Start Guide - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Simple Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Simple Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_azerite(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Azerite')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Azerite Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Azerite Traits, Azerite Armor, and Heart of Azeroth – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Azerite Traits, Azerite Armor, and Heart of Azeroth - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Azerite Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Azerite Guide', content)

        # Checks if the body is using expressions as often as it should                    
        guideFormat = '{0} {1} azerite'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Azerite Guide', 3 )

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_simulations(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Simulations')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Simulations Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Simulation Compilation – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Simulation Compilation - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Simulations Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Simulations Guide', content)

        # Checks if the body is using expressions as often as it should

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_mythic_plus(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Mythic Plus')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Mythic Plus Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Mythic+ Guide – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Mythic+ Guide - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Mythic Plus Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Mythic Plus Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_raid_tips(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Raid Tips')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Raid Tips Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Raid Guide & Battle of Dazar\'alor Raid Tips – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Raid Guide & Battle of Dazar\'alor Raid Tips - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Raid Tips Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Raid Tips Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_improve(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Improve')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Improve Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Mistakes and How to Improve – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Mistakes and How to Improve - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Improve Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Improve Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_macro_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Macro Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Macro Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Macros & Addons – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Macros & Addons - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Macro Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Macro Guide', content)

        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} macro'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Macro Guide', 3 )

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_weakauras(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'WeakAuras')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} WeakAuras Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} WeakAuras – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} WeakAuras - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} WeakAuras Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'WeakAuras Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_pvp(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'PvP')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} PvP Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} PvP Guide – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} PvP Guide - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} PvP Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'PvP Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
            
    def seoGuideAnalysis_glossary(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Glossary')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Glossary Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Glossary, Abbreviations, and Common Terms – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Glossary, Abbreviations, and Common Terms - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Glossary Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))  

        # Checks the usage of aliases   
        issues += self.aliasesEvaluation(charClass, charSpec, 'Glossary Guide', content)

        # Checks if the body is using expressions as often as it should    

        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues

    def seoGuideAnalysis_rotation_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Rotation Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Rotation Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Rotation Guide – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Rotation Guide - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Rotation Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Rotation Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} rotation'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Rotation Guide', 4 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
        
    def seoGuideAnalysis_artifact_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Artifact Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Artifact Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
            
        artifact = self.options['artifacts']['-'.join(charSpec.lower().split(' ')) + '-' + '-'.join(charClass.lower().split(' '))]
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Artifact Weapon: {4} – {2} {3}'.format(charSpec, charClass, expansion, patch, artifact)
        expectedTitle2 = '{0} {1} Artifact Weapon: {4} - {2} {3}'.format(charSpec, charClass, expansion, patch, artifact)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Artifact Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Artifact Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} artifact'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Artifact Guide', 3 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
        
    def seoGuideAnalysis_gear_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Gear Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Gear Guide wasn\'t found.'.format(charClass, charSpec)]
        
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Gear, Tier Sets & BiS – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Gear, Tier Sets & BiS - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Gear Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Gear Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = 'bis'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        #guideFormat = 'tier set'
        #issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        guideFormat = 'armor'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        guideFormat = 'gear'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        
        guideFormat = '{0} {1} gear'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 1 )
        #guideFormat = '{0} {1} tier set'
        #issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 1 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
        
    def seoGuideAnalysis_stat_priority_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Stat Priority Guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Stat Guide wasn\'t found.'.format(charClass, charSpec)]
            
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Stat Priority – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Stat Priority - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Stat Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Stat Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} stat priority'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Stat Guide', 3 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
        
    def seoGuideAnalysis_enhancements_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Enhancements Guide')
        
        content = content.lower()
        
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Enhancements Guide wasn\'t found.'.format(charClass, charSpec)]
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Enchants, Gems & Enhancements – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Enchants, Gems & Enhancements - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Enhancements Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Enhancements Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} enchants'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Enhancements Guide', 2 )        
        guideFormat = '{0} {1} gems'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Enhancements Guide', 2 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues
        
    def seoGuideAnalysis_macro_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'Macro Guide')
                
        # Verifies if it was found
        if title is None:
            return 'x', ['{0} {1} Macro Guide wasn\'t found.'.format(charClass, charSpec)]
            
        content = content.lower()
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Macros & Addons – {2} {3}'.format(charSpec, charClass, expansion, patch)
        expectedTitle2 = '{0} {1} Macros & Addons - {2} {3}'.format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle and title != expectedTitle2:
            issues.append('{0} {1} Macro Title has the wrong format. "<{2}>" instead of "<{3}>" '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks the usage of aliases
        issues += self.aliasesEvaluation(charClass, charSpec, 'Macro Guide', content)
        
        # Checks if the body is using expressions as often as it should
        guideFormat = '{0} {1} macro'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Macro Guide', 3 )
            
        # Returns the amount of issues for the summary and the list of them for the detail
        return str(len(issues)), issues        
            
    def expressionEvaluation(self, charClass, charSpec, content, guideFormat, guide, expectedCount):
        classAliases = []
        specAliases = []
        issues = []
        
        # Adds all aliases to the list, if there are any
        if charSpec in self.options['validations']:
            specAliases += self.options['validations'][charSpec].keys()
            
        # Otherwise, adds only the spec to it
        else:
            specAliases.append(charSpec)
            
        # Adds all aliases to the list, if there are any    
        if charClass in self.options['validations']:
            classAliases += self.options['validations'][charClass].keys()
            
        # Otherwise, adds only the spec to it
        else:
            classAliases.append(charClass)
        
        
        # Build all terms based on aliases and count how many times they show up
        terms = []
        
        for classAlias in classAliases:
            for specAlias in specAliases:
                terms.append( guideFormat.format( specAlias, classAlias ).lower() )
                
        occurenceCount = 0
        
        for term in terms:
            occurenceCount += content.lower().count(term)
        
        # If the body doesn't contain enough occurences, add issue
        if occurenceCount < expectedCount:
            issues.append('{0} {1} {2} needs more expressions <{3}>. Found {4} instead of {5} '.format(charClass, charSpec, guide, terms[0], occurenceCount, expectedCount))
        
        return issues
            
    def aliasesEvaluation(self, charClass, charSpec, guide, content):
        
        issues = []
        
        # Checks if either spec or class has an alias
        
        if charClass in self.options['validations']:
            issues += self.termFrequencyEvaluation(charClass, content, '{0} {1} {2}'.format(charSpec, charClass, guide))

        if charSpec in self.options['validations']:
            issues += self.termFrequencyEvaluation(charSpec, content, '{0} {1} {2}'.format(charSpec, charClass, guide))
        
        return issues
        
    
    def termFrequencyEvaluation(self, term, content, context):    
        issues = []
        
        validations = self.options['validations'][term]                        
        totalWeight = sum(validations.values())
        aliases = validations.keys()
        
        exclude = set(string.punctuation)
        content = ''.join(ch for ch in content.lower() if ch not in exclude)
        
        # Count the occurence of each term
        termsCount = []
        for alias in aliases:
            lowAlias = alias.lower()
            pattern = r'{0}(\s|s\s|$)+'.format(lowAlias)            
            termsCount.append([alias, re.subn(pattern, '', content)[1]])                
        
        # Total sum of occurences
        termsSum = sum([x[1] for x in termsCount])

        if termsSum == 0:
            termsSum = 1
        
        for key, value in validations.items():
            
            # Checks if key shows up at least twice
            pattern = r'{0}(\s|s\s|$)+'.format(key.lower())            
             

            if re.subn(pattern, '', content)[1] < 2:
                issues.append('{0} doesn\'t show up 2 times on {1}'.format(key, context) )
                
            # If the ratio of a given term is 50% or higher checks its frequency
            if ( 1.0 * value ) / totalWeight >= 0.5:
                dic = dict(termsCount)
                ratio = ( 1.0 * dic[key] ) / termsSum
                
                # Gives a the ratio a lee way
                precision = self.options['precision']                
                
                # If ratio found is too far from the ratio expected
                if ratio < ( 1 - precision ) * ( ( 1.0 * value ) / totalWeight ):                   
                    issues.append('{0} doesn\'t show as often as it should on {1} - Only {2} appearances in {3} aliases'.format(key, context, dic[key],termsSum) )
                    
        return issues
        
    def dataFetch(self, charClass, charSpec, guide):
        print('>Fetching {1} {0} {2}'.format(charClass, charSpec, guide))
        
        charClass = '-'.join(charClass.lower().split(' '))
        charSpec = '-'.join(charSpec.lower().split(' '))
        guide = '-'.join(guide.lower().split(' '))
        
        url = (self.options['urlFormats'][guide]+'&brl').format(charClass, charSpec)
        
        driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chrome_driver)
        driver.get(url)

        try:
            title = copy.deepcopy(driver.title.replace(' - Guides - Wowhead',''))
            body = copy.deepcopy(driver.find_element_by_id(id_='guide-body').text)
        except:
            driver.close()
            return None, None

        driver.close()
        
        return title, body
        #return title, '\n'.join(lines)
            
    def classSpecCombos(self):
        combos = []
        combos.append(['Blood', 'Death Knight'])
        #return combos
        combos.append(['Frost', 'Death Knight'])
        combos.append(['Unholy', 'Death Knight'])        
        combos.append(['Havoc', 'Demon Hunter'])
        combos.append(['Vengeance', 'Demon Hunter'])
        combos.append(['Balance', 'Druid'])
        combos.append(['Guardian', 'Druid'])
        combos.append(['Feral', 'Druid'])
        combos.append(['Restoration', 'Druid'])
        combos.append(['Beast Mastery', 'Hunter'])
        combos.append(['Marksmanship', 'Hunter'])
        combos.append(['Survival', 'Hunter'])
        combos.append(['Arcane', 'Mage'])
        #return combos
        combos.append(['Fire', 'Mage'])
        combos.append(['Frost', 'Mage'])
        combos.append(['Brewmaster', 'Monk'])
        combos.append(['Mistweaver', 'Monk'])
        combos.append(['Windwalker', 'Monk'])
        combos.append(['Holy', 'Paladin'])
        combos.append(['Protection', 'Paladin'])
        combos.append(['Retribution', 'Paladin'])
        combos.append(['Discipline', 'Priest'])
        combos.append(['Holy', 'Priest'])
        combos.append(['Shadow', 'Priest'])
        combos.append(['Assassination', 'Rogue'])
        combos.append(['Outlaw', 'Rogue'])
        combos.append(['Subtlety', 'Rogue'])
        combos.append(['Elemental', 'Shaman'])
        combos.append(['Enhancement', 'Shaman'])
        combos.append(['Restoration', 'Shaman'])
        combos.append(['Affliction', 'Warlock'])
        combos.append(['Destruction', 'Warlock'])
        combos.append(['Demonology', 'Warlock'])
        combos.append(['Arms', 'Warrior'])
        combos.append(['Fury', 'Warrior'])
        combos.append(['Protection', 'Warrior'])
        return combos
        