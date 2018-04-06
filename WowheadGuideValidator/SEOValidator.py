import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen, urlcleanup
from urllib.error import URLError
import json


class SEOValidator:    

    def __init__(self):
        self.file = 'options.json'
        self.options = {}
        self.loadOptions()
        self.loop = 0
      
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
        expectedTitle2 = '{0} {1} Talents & Build Guide -{2} {3}'.format(charSpec, charClass, expansion, patch)
        
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
        guideFormat = 'tier set'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        guideFormat = 'armor'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        guideFormat = 'gear'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 3 )
        
        guideFormat = '{0} {1} gear'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 1 )
        guideFormat = '{0} {1} tier set'
        issues += self.expressionEvaluation(charClass, charSpec, content, guideFormat, 'Gear Guide', 1 )
            
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
        
        content = content.lower()
        
        # Count the occurence of each term
        termsCount = []
        for alias in aliases:
            lowAlias = alias.lower()
            termsCount.append([alias, content.count('{0} '.format(lowAlias))])                
        
        # Total sum of occurences
        termsSum = sum([x[1] for x in termsCount])
        
        for key, value in validations.items():
            
            # Checks if key shows up at least twice
            if content.count(' {0} '.format(key.lower())) < 2:
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
        url = 'https://www.wowhead.com/{1}-{0}-{2}'.format(charClass, charSpec, guide)               
        
        req = Request(url)
        try:
            urlcleanup() 
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('   We failed to reach a server.')
                print('   Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('    The server couldn\'t fulfill the request.')
                print('    Error code: ', e.code)
            return None, None
        else:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            lines = text.split('\n')
            
            # Finds the title in the text
            title = lines[0].replace(' - Guides - Wowhead','')
            
            # Finds the Context - It is the line after "ReportLinks"
            content = ''
            nextIsContent = False
                                    
            for line in lines:
                if nextIsContent:
                    content += line
                if 'ReportLinks' in line:
                    nextIsContent = True
                if 'Share your comments about ' in line:
                    break
                    
            return title, content
            #return title, '\n'.join(lines)
            
    def classSpecCombos(self):
        combos = []
        combos.append(['Blood', 'Death Knight'])
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
        