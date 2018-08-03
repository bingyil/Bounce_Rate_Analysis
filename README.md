# Bounce_Rate_Analysis

Team Members: Yue Lan, Bingyi Li, Guoqiang Liang, Beiming Liu, Zizhen Song

## Goal

Optimize webpage design by collecting user-level data and conducting multi-level A/B tests.

## Brief Intro

No discussion of transportation in New York would be complete without talking about one of the cheapest, easiest—and, increasingly, most popular—ways of getting around the city: biking. About 450,000 bike trips are taken every day in the five boroughs, with one in five of those trips being taken by someone who’s commuting. So what are bikers' favorite route to ride in the city? And when is the most common time for biking? In order to clearly answer these questions, we created a dynamic visualization tool. 

However, we come up with three different webpage designs and wonder which one is the most attractive. To get answers, we break down the question into three part:<br/>
1. Determine optimization metric
2. Calculate required sample size for the experiment
3. Track users' behavior

The optimization metric of our test is the bounce rate on the webpage, since we expect that users will be willing to interact with the webpage for a little bit amount of time if the diagram is attractive enough.

To calculate sample size, we build a web application using Dash in Python. The calculator is to suggest a common sample size n for each condition based on the following inputs:
- the significance level 𝛼
- thepowerofthetest 1−𝛽
- the effect size 𝛿 

To track the users' behavior, we insert Google Analytics tracking code to each of our webpages and perform the analysis until we collect enough samples. 

## Deliverable

The [report](https://github.com/bingyil/Bounce_Rate_Analysis/blob/master/Bounce_Rate_Analysis_Report.pdf) is a complete demonstration of the discussion.
