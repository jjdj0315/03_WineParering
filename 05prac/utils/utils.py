import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from .retrival import wine_search

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
)


def recommend_food(x):
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """
                        You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.

                        Your task is to accurately identify the wine in question and recommend an appropriate food pairing based on the provided wine reviews in triple quotes. 대답은 한글로 해줘

                        ### Task Instructions:

                        1. **Review Analysis**:
                        - Carefully read the wine review provided within triple quotes.
                        - Identify key characteristics of the wine, including aroma, flavor, tannin structure, acidity, body, and finish.

                        2. **Wine Identification**:
                        - Based on the identified characteristics, determine the specific type of wine, its possible grape variety, region of origin, and vintage if possible.
                        - Consider elements such as fruit notes (e.g., cherry, blackberry), non-fruit notes (e.g., oak, vanilla), and structural components (e.g., tannins, acidity).

                        3. **Pairing Recommendation**:
                        - Recommend an appropriate food pairing that complements the identified wine.
                        - Take into account the wine’s characteristics (e.g., a full-bodied red wine with high tannins pairs well with rich, fatty meats).
                        - Suggest alternative pairings such as cheese, desserts, or even specific dishes that enhance the wine's profile.
                            """,
            ),
            ("human", "{query}"),
        ]
    )

    return prompt | llm | StrOutputParser()


def chain_recommend_food():
    return RunnableLambda(recommend_food)


def taste_food(x):
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "When provided with an input question, please identify the dish in question and describe what it tastes like.",
            ),
            ("human", "{query}"),
        ]
    )

    return prompt | llm | StrOutputParser()


def wine_retrieva(taste):
    return {
        "food": taste,
        "review": "\n".join(d.page_content for d in wine_search(taste)),
    }


def recommend_wine(x):
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.

        Your task is to accurately identify an appropriate wine pairing based on the provided food description in triple quotes. 대답은 한글로 해줘

        ### Task Instructions:

        1. **Food Analysis**:
        - Carefully read the food description provided within triple quotes.
        - Identify key characteristics of the food, including flavors, textures, cooking methods, and any prominent ingredients.

        2. **Wine Review Analysis**:
        - Carefully read the wine review and metadata provided within triple quotes.
        - Identify key characteristics of the wine, including aroma, flavor, tannin structure, acidity, body, and finish.

        3. **Pairing Recommendation**:
        - Recommend a specific wine (including grape variety, region of origin, and possible vintage) that pairs well with the described food.
        - Explain why this wine is a suitable match for the food, taking into account factors such as acidity, tannin structure, body, and flavor profile.

        ### Example:

        **Food**:
        ```Triple-cooked pork belly with a crispy skin, served with a tangy apple and fennel slaw, and a rich, savory jus.```

        **Wine Review**:
        ```
        winery: Barossa Valley Shiraz
        description: This full-bodied Shiraz from Barossa Valley, Australia, boasts rich flavors of dark berries, black pepper, and a hint of vanilla. It has a robust tannin structure and a long, spicy finish.
        points: 92
        price: 30
        variety: Shiraz
        ```

        **Wine Pairing Recommendation**:
        ```A full-bodied red wine such as a Shiraz from Barossa Valley, Australia, would pair excellently with the triple-cooked pork belly. The wine’s robust tannins and dark fruit flavors will complement the rich, savory notes of the pork, while its hint of spice will enhance the tangy apple and fennel slaw. The acidity in the Shiraz will cut through the fat of the pork, creating a balanced and harmonious dining experience.```

        ### Now, provide a food description in triple quotes for the system to recommend a wine pairing:
        **Food**:
        ```
        {food}
        ```

        **Wine Review**:
        ```
        {review}
        ```
        """,
            )
        ]
    )
    return prompt | llm | StrOutputParser()


def chain_recommend_wine():
    return (
        RunnableLambda(taste_food)
        | RunnableLambda(wine_retrieva)
        | RunnableLambda(recommend_wine)
    )
