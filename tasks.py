import datetime
from textwrap import dedent

def get_task_desc_researcher() -> str:
    return dedent(f"""Conduct a comprehensive analysis of the latest high performing startups active in the 
field of generative AI. It is important that those startups with their advancements in 
generative AI are active in the finance sector since a year. Identify key startups, 
breakthrough technologies, and potential fast growing startups with impact in the finance 
sector caused by generative AI. As a researcher you analyse how generative AI will change 
the finance industry. It would be good to know if that startup is still searching for money 
investments actively. Your final answer MUST be a full analysis report.
Example Report: 
    Finance Tech Startup Research Table: 
    - Startup 1: 
        - Name: "Kern AI" 
        - Investment sum: 1.00.00.000 
        - Founded in: 2022 
        - Number of Employees: 50 
        - Company homepage: https://www.kern.ai/ 
    - Startup 2: 
        - Name: "Scrub AI" 
        - Investment sum: 5.00.00.000 
        - Founded in: 2023 
        - Number of Employees: 22 
        - Company homepage: https://scrub-ai.com/
Today is the """)+str(datetime.date.today())+""" ."""

def get_task_desc_autor() -> str:
    return dedent(f"""Using the insights provided, write an article like an engaging blog post that highlights the most significant startups 
active in generative AI with important advancements in this field. Your written article should be informative yet accessible, catering to a tech-savvy startup scene and 
audience. Make it sound cool, avoid complex words so it doesn't sound like AI. Your final answer MUST be the a full structures blog post 
The article you are writing has a minimum of 1600 words and highlights 10 startups. In the summary please list the startups with web addresses like url's headlines and bullet points for easy reading. 
The text itself is enriched with nice emojis to highlight important parts.
                                                       
The structure of the article you have to write could look like the example below: 
                                                       
Example article structure:
    Executive Summary: 
    - Overview of the AI startup's performance. 
    - Key financial metrics and achievements. 
    - Future growth prospects. 
    - Introduction: 
    - Brief background of the AI startup. 
    - Mission and objectives. 
    - Market Analysis: 
    - Analysis of the AI market segment. 
    - Growth trends and opportunities. 
    - Competitive landscape. 
    - Business Model: 
        - Description of the AI startup's business model. 
        - Revenue streams. 
        - Cost structure. 
    - Financial Performance: 
        - Revenue analysis: 
        - Revenue growth over time. 
    - Revenue sources (e.g., product sales, subscriptions, services). 
        - Profitability analysis: 
        - Gross profit margin. 
        - Operating profit margin. 
        - Net profit margin. 
    - Cash flow analysis: 
        - Operating cash flow. 
        - Investing cash flow. 
        - Financing cash flow. 
    - Balance sheet analysis: 
        - Assets composition. 
        - Liabilities and equity. 
    - Key financial ratios: 
        - Return on Investment (ROI). 
        - Return on Equity (ROE). 
        - Debt-to-Equity ratio. 
        - Current ratio. 
        - Quick ratio. 
    - Investment Analysis: 
        - Valuation: 
            - Methods used (e.g., Discounted Cash Flow, Comparable Company Analysis). 
            - Assumptions and inputs. 
    - Investment risks: 
        - Market risks. 
        - Technology risks. 
        - Regulatory risks. 
    - Strategic Initiatives: 
        - Expansion plans. 
        - Research and development efforts. 
        - Strategic partnerships. 
    - Conclusion: 
        - Summary of key findings. 
        - Recommendations for investors. 
        - Future outlook. 
    - Appendix: 
        - Detailed financial tables. 
        - Glossary of financial terms. 
        - References: 
    - Sources of information used in the report. \nToday is the: """) +str(datetime.date.today())+""" ."""

def get_task_desc_business_angel() -> str:
    return dedent(f"""Involve evaluating investment opportunities, conducting due diligence 
on potential ventures, and advising startups on strategy, fundraising, and growth tactics. Search how much venture capital each startup already raised. 
Add a comment if an future investment would be an option for an investor. Only from interest are startups in finance sector which are active over the last 
year and this year. Additionally, they often facilitate connections between entrepreneurs and potential investors, leveraging their network to bridge the 
gap between promising startups and capital sources. 
Executive Summary:
- Concise overview of the investment opportunity.
- Highlights of key figures and decision points.
- Summary of investment recommendations.
Introduction:
- Introduction to the company or opportunity being presented.
- Purpose of the report.
- Scope and methodology.
Market Analysis:
    - Market overview:
        - Size, growth rate, and trends.
        - Market segmentation.
    - Competitive landscape:
        - Major players and market share.
        - Competitive advantages of the company.
Business Model:
- Description of the company's business model.
- Revenue streams and sources.
- Cost structure and scalability.
Financial Performance:
    - Revenue analysis:
        - Historical revenue trends.
        - Forecasted revenue growth.
    - Profitability analysis:
        - Gross margin, operating margin, net margin.
    - Cash flow analysis:
        - Operating cash flow, free cash flow.
    - Key financial ratios:
        - Return on Investment (ROI), Return on Equity (ROE), Debt-to-Equity ratio, etc.
Investment Thesis:

Investment opportunity:
    - Value proposition.
    - Unique selling points.
    - Potential returns:
        - Expected ROI.
        - Risk-adjusted returns.
    - Risks and Mitigation Strategies:

    - Identification of potential risks:
        - Market risks, operational risks, regulatory risks, etc.
    - Mitigation strategies:
        - Plans to address identified risks.
    - Strategic Growth Initiatives:
Expansion plans:
    - Geographic expansion, product diversification, etc.
Research and development:
    - Innovation pipeline and investments.
Strategic partnerships:
    - Alliances, joint ventures, collaborations.
Valuation:
    Valuation methodology:
        - Discounted Cash Flow (DCF), Comparable Company Analysis (CCA), etc.
        - Valuation assumptions and inputs.
Investment Recommendations:
    - Summary of key findings and analysis.
Investment decision:
    - Buy, sell, hold recommendations.
    - Justification of recommendations.
Conclusion:
    - Summary of the investment opportunity.
    - Closing remarks.
Appendix:
    - Detailed financial tables.
    - Glossary of financial terms.
    - Assumptions used in the analysis.
References:
- Sources of information used in the report.                          
Today is the """)+str(datetime.date.today())+""" ."""