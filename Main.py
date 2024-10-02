from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from agents import online_profile_agent, search_agent


def main(person_info):
    summary_template = """
    Given the information about a person as "{info}. {online_profiles}", provide the following details of the person:
    1. A short summary
    2. Two interesting facts about them
    3. List of online profiles ( this list should contain nothing, but the URLs to all Github and LinkedIn profiles of the person )
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["info"],
        template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
    # llm = ChatOllama(model="llama3.1")

    chain = summary_prompt_template | llm | StrOutputParser()

    person_search_results = search_agent.search(person_info)
    online_profiles = online_profile_agent.search(person_info)

    res = chain.invoke(
        input={
            "info": person_search_results,
            "online_profiles": online_profiles
        }
    )

    print(res)


if __name__ == '__main__':
    load_dotenv()
    main("Prabhakar Bikkaneti")