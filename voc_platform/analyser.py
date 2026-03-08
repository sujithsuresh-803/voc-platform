from google import genai
import json
import pandas as pd
from config import GEMINI_API_KEY, MODEL_NAME, MAX_FEEDBACK_ITEMS

# Connect to Gemini - reads API key from environment automatically
client = genai.Client(api_key=GEMINI_API_KEY)


def analyse_feedback(feedback_list):
    """
    Takes a list of feedback strings
    Sends them to Gemini
    Returns a structured dataframe with tags
    """

    # Safety limit
    feedback_list = feedback_list[:MAX_FEEDBACK_ITEMS]

    # Number each piece of feedback
    numbered_feedback = "\n".join(
        [f"{i+1}. {item}" for i, item in enumerate(feedback_list)]
    )

    prompt = f"""
    You are a senior product analyst at a tech company.
    Analyse each piece of customer feedback below and return a JSON array.
    
    For each feedback item return:
    - id: the number
    - feedback: the original text (shortened to 100 chars)
    - theme: one of [Performance, UI/UX, Features, Pricing, Support, Content, Onboarding, Bug]
    - sentiment: one of [Positive, Negative, Neutral]
    - severity: one of [Critical, High, Medium, Low]
    - feature_area: the specific feature or area being mentioned
    - summary: one sentence summary of the issue or praise
    
    Return ONLY a valid JSON array. No explanation. No markdown. Just the JSON.
    
    Feedback to analyse:
    {numbered_feedback}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    raw = response.text.strip()

    # Clean response in case Gemini adds markdown
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    # Parse JSON into a pandas dataframe
    data = json.loads(raw)
    df = pd.DataFrame(data)

    return df


def generate_executive_summary(df):
    """
    Takes the analysed dataframe
    Asks Gemini to write an executive summary
    Returns a string report
    """

    total = len(df)
    critical = len(df[df["severity"] == "Critical"])
    negative = len(df[df["sentiment"] == "Negative"])
    top_themes = df["theme"].value_counts().head(3).to_dict()
    top_features = df["feature_area"].value_counts().head(3).to_dict()

    prompt = f"""
    You are a senior product operations manager writing a weekly insights report.
    
    Here is this week's customer feedback summary:
    - Total feedback items analysed: {total}
    - Critical issues: {critical}
    - Negative sentiment: {negative} ({round(negative/total*100)}%)
    - Top themes: {top_themes}
    - Most mentioned feature areas: {top_features}
    
    Write a concise executive summary with these exact sections:
    
    ## Overview
    2-3 sentences on overall customer sentiment this week.
    
    ## Critical Issues
    List the most urgent problems that need immediate attention.
    
    ## Key Patterns
    What recurring themes or trends are emerging?
    
    ## Recommended Actions
    3-5 specific, actionable recommendations for the product team.
    
    ## Positive Signals
    What are customers happy about? What is working well?
    
    Keep it sharp, specific and actionable. Write like a PM presenting to leadership.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text