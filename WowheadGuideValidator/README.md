# Guide Validator

This script has been built in order to verify SEO aspects on different WoW Class Guides, following SEO recommendations about the classes and specializations and guides themselves.

## Workflow

The script follows a simple workflow:

* Check the options to see which class and specialization it should verify and which guides from those combinations
* Builds the URL based on a known pattern and fetches the live version of the page using a generic parser that extracts the title and the content from the HTML page.
* Verifies if the Title of the guide follows the SEO instructions
* Verifies if the guide uses the proper amount of aliases as it should for each class and specialization. 
  - For instance, when searching for Death Knights, people predominantly use `DK` instead of `Death Knight`, so it was stipulated that the expression `DK` should appear three times more often than `Death Knight` on guides about that class.
* Verifies if the guide is using the correct amount of expressions as it should.
  - Each guide type (`Talents`, `Macros`, `Stats`) was recommended to have different expressions shown in their bodies. For instance, Talent guides should have `<Specialization> <Class> Talents` and `<Specialization> <Class> Builds` show up at least twice each in their bodies. 
* Builds a table showing the amount of issues on each guide for each specialization/class and list the issues below

## Functions
    
In order to execute the workflow, there are _ main working functions:
* `dataFetch` that takes Class, Specialization and Guide type, builds the URL for that guide, extracts and returns the title and content from the HTML page.
* `termFrequencyEvaluation` that receives a generic term and the content of a guide and evaluates the usage of that given term's aliases on that given guide.
* `expressionEvaluation` that receives the Class, Specialization, Content of a guide, expression format and the amount of times that given format should show up and  verifies if that expression shows up as many times in the body of the guide, considering all possible aliases for Specializations and Classes.

The main flow of the script is done by `seoAnalysis`, that starts all the flows, calling the delegate functions for each type of guide, prefixed by `seoGuideAnalysis_`. Each guide type holds the rules for that guide and is responsible for calling the generic and specific guide analysis for that given guide.

For base data storage, the file `options.json` is used. In it, you will find the definitions for the current expansion, patch, artifact weapons names, aliases used by classes and specializations and which type of guides will be verified. The class+specialization combos are found in the main code due to ease of access, but could easily moved to the options file.
    