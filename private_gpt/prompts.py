PROMPTS = [
    {
        "section": "context",
        "prompt": """
            Using a concise, brief tone with no fluff words, describe the team’s product or service to serve as an introduction to a document describing their technical work. If you can find the information, briefly overview the team’s technical accomplishments in the previous fiscal year. Keep it to less than 300 characters.
        """
    },
    {
        "section": "technicalObjectives",
        "prompt": """
            Using a concise, brief tone with no fluff words, describe the team’s technical goal or goals in this year. Keep it to less than 150 characters.
        """
    },
    {
        "section": "technologicalUncertainties",
        "prompt": """
            Tone: academic, focusing on technology, concise
            Define a technological uncertainty as when the team who did the work in the description had technical goals, but standard technology or technologies that they have considered limits them to completely achieving those technical goals. Based on the information you have, identify the technological uncertainty the team faced. In around 1000 characters, begin with a sentence describing what the team was uncertain and why. Then, based on the information, talk about why existing solutions/off the shelf products/methodologies/solutions they tried prevented them from reaching their technical goal(s).
        """
    },
    {
        "section": "iterations",
        "prompt": """
            Tone: first person format, concise, no fluff words, academic, focus on technology
            Start with a single sentence containing a hypothesis statement. To build the hypothesis statement, scan the information to understand what work the team accomplished. Based on this work, reverse engineer a hypothesis statement in the format of what technical technique/methodology would result in what outcome, so that it makes sense according to the work done. For technologies described, try to provide a technical description of what that technology does and contextualize it within your description of work done.
            Then, in around 1000 characters, describe the work done to address the reverse-engineered hypothesis. Conclude with whether the hypothesis has been addressed.
        """
    },
    {
        "section": "advancement",
        "prompt": """
            based on the following information, what technological advancements did the team achieve that mirrors their technological uncertainties? keep it to 2 advancements, one per uncertainty, and for each advancement, write a concise, tightly worded paragraph where the gist is "we discovered that _________ result in _________ and therefore resolves the [technological uncertainty] [in this manner]"
        """
    },
]

