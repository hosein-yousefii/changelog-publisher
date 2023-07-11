# Changelog generator and publisher

[![GitHub license](https://img.shields.io/github/license/hosein-yousefii/changelog-publisher)](https://github.com/hosein-yousefii/changelog-publisher/blob/master/LICENSE)
![LinkedIn](https://shields.io/badge/style-hoseinyousefi-black?logo=linkedin&label=LinkedIn&link=https://www.linkedin.com/in/hoseinyousefi)

This helps you to automate generating and publishing changelog and upload it to confluence (git soon) html page format.

## Description
We usually store changelog somewhere to be able to reach it easily when needed. It should be clear enough to gives an inisght to the application.

writing this changelog manually is bothering and honestly, we don't so, it's time to automate it. you just need onething, have a clean and conventional git commits.

After your deployment is finished you can put this code in your pipeline to generate fascinating changelog in confluence html page.

If you are using jira as a issue tracker and you want to link each issue to your commits, it's also supported.

## Usage
There is python tool to generate changelog first and it supports custome template which is really good feature. with this tool and our custome template which is "changeLog_Template.md" we are able to have something like this picture.

<img width="900" src="https://github.com/hosein-yousefii/changelog-publisher/blob/main/example/changelog.png">
