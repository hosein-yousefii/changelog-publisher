# Changelog generator and publisher

[![GitHub license](https://img.shields.io/github/license/hosein-yousefii/changelog-publisher)](https://github.com/hosein-yousefii/changelog-publisher/blob/master/LICENSE)
![LinkedIn](https://shields.io/badge/style-hoseinyousefi-black?logo=linkedin&label=LinkedIn&link=https://www.linkedin.com/in/hoseinyousefi)

This helps you to automate generating and publishing changelog and upload it to confluence (git soon) html page format.

## Description
We usually store changelog somewhere to be able to reach it easily when needed. It should be clear enough to gives an inisght to the application.

writing this changelog manually is bothering and honestly we don't. So, it's time to automate it. you just need onething, have a clean and conventional git commits.

After your deployment is finished you can put this code in your pipeline to generate fascinating changelog in confluence html page.

If you are using jira as a issue tracker and you want to link each issue to your commits, it's also supported.

Finally the result would be something like this picture:

<img width="900" src="https://github.com/hosein-yousefii/changelog-publisher/blob/main/example/changelog.png">

## Usage
We need to do it step by step and make sure everything is right inorder to get the better result.

**Steps:**

**1-** make sure your commits messages are in conventional way or something similar like this: "fix(OPTIONAL SCOPE): [JiraTicketKey-1122] DESCRIPTION"
  or if it's a feature: "feat(OPTIONAL SCOPE): [DEVOPS-1122] DESCRIPTION". [more information about conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
**2-** Install changelog generator tool [Read more about it in this link](https://github.com/pawamoy/git-changelog) by executing:
  ```
  pip install git-changelog
  ```
**3-** Clone your application and inside the repository execute:
  ```
  git-changelog -c angular -rt path:./template.jinja --output CHANGELOG.md -s fix,feat
  ```
  it will create a file named CHANGELOG.md with our template which name is "template.jinja" and located in "changelog-generator-template".

  **REMEMBER you need to choose the right path to the template** 

**4-** Now you need to install dependencies for changelog-publisher by using:
  ```
  pip3 install -r requirements.txt
  ```
**5-** Then you have to provide some variables regarding confluence:
  ```
  # Your confluence url
  export ChangeLogPub_confluenceURL="http://your-confluence-server.com"

  # which confluence do you want to create the page.
  export ChangeLogPub_confluenceSpace=DEVOPS

  # what is the name of the page
  export ChangeLogPub_confluencePageTitle=application-changelog

  # apikey to be able to connect to confluence server
  export ChangeLogPub_confluenceApiKey="TEST"
  ```
**6-** After this you just need to execute this tool:
  ```
  python3 changelog-publisher.py
  ```
  It will convert the CHANGELOG.md to html format and add header/footer from "changeLog_Template.md" then make it compatible with confluence html page, then if the mentioned page doesn't exist it will create it otherwise it will update it to a newer version.

## OPTIONS

You are able to change these options by exporting them into your environments:

| VARIABLES                       | REQUIRED  | DESCRIPTION                                                                     |
| ------------------------------- | --------- | ------------------------------------------------------------------------------- |
| ChangeLogPub_htmlOutputToFile   | OPTIONAL  | You are able to save the converted html file. (default: true)                   |
| ChangeLogPub_changeLogTemplate  | OPTIONAL  | You can have your own changelog template (default: ./ChangeLog_Template.md)     |
| ChangeLogPub_ChangeLogFile      | REQUIRED  | Path to the Changelog.md (default: ./CHANGELOG.md)                              |
| ChangeLogPub_htmlFile           | REQUIRED  | Converted changelog to html. (default: CHANGELOG.html)                          |
| ChangeLogPub_headerTag          | REQUIRED  | Header tag which is used in changelog template file. (default: [header])        |
| ChangeLogPub_footerTag          | REQUIRED  | Footer tag which is used in changelog template file. (default: [footer])        |
| ChangeLogPub_confluenceURL      | REQUIRED  | Confluence url.(default: http://confluence-server.com)                          |
| ChangeLogPub_confluenceSpace    | REQUIRED  | Cofluence space which you want to create/update the page.                       |
| ChangeLogPub_confluencePageTitle| REQUIRED  | Confluence page which you want to put your changelog.                           |
| ChangeLogPub_confluenceApiKey   | REQUIRED  | Confluence api key.                                                             |


## contribute
Do you want to contribute so, don't waste your time and send me an email: Yousefi.hosein.o@gmail.com

Copyright 2023 Hosein Yousefi <yousefi.hosein.o@gmail.com>







