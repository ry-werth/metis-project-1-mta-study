# metis-project-1-mta-study

## Back Story

An email from a potential client:

> Vinny & Joan -
>
> It was great to meet with you and chat at the event where we recently met and had a nice chat. We’d love to take some next steps to see if working together is something that would make sense for both parties.
>
> As we mentioned, we are interested in harnessing the power of data and analytics to optimize the effectiveness of our street team work, which is a significant portion of our fundraising efforts.
>
> WomenTechWomenYes (WTWY) has an annual gala in New York City at the beginning of the fall each year. As we are new and inclusive organization, we try to do double duty with the gala both to fill our event space with individuals passionate about increasing the participation of women in technology, and to concurrently build awareness and reach.
>
> To this end we place street teams at entrances to subway stations. The street teams collect email addresses and those who sign up are sent free tickets to our gala.
>
> Where we’d like to solicit your engagement is to use MTA subway data, which as I’m sure you know is available freely from the city, to help us optimize the placement of our street teams, such that we can gather the most signatures, ideally from those who will attend the gala and contribute to our cause.
>
> The ball is in your court now—do you think this is something that would be feasible for your group? From there we can explore what kind of an engagement would make sense for all of us.
>
> Best,
>
> Karrine and Dahlia
>
> WTWY International

# This Repo attempts to analyze MTA turnstyle data and outher sources to address the above email

## MTA Analysis
This is Where the bulk of the project is. 

The turnstyle analysis is done in the [Station_Scoring_Analysis directory](https://github.com/ry-werth/metis-project-1-mta-study/tree/master/Station_Scoring_Analysis). The main file to look at is `MTA_Main_Analysis.ipynb` . This will walk you through all of the work done.

## Station Points

As a group we first created a dataset of MTA stations with each getting a custom score. This scores is determined by proximity to different locations of interest. This work is done in the [Station_Scoring_Analysis directory](https://github.com/ry-werth/metis-project-1-mta-study/tree/master/Station_Scoring_Analysis). The anaylsis is done in the `Exploration and focus` file.

## Data
The Turnstyle data was taken from the public [MTA Page](http://web.mta.info/developers/turnstile.html)






