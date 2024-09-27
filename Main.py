from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from third_party.linkedin import scrape_linkedin_profile


def main():
    summary_template = """
    Given the Linkedin information {info} about a person, create:
    1. A short summary
    2. Two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["info"],
        template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
    # llm = ChatOllama(model="llama3.1")

    chain = summary_prompt_template | llm | StrOutputParser()

    information = scrape_linkedin_profile("")
    res = chain.invoke(input={"info": information})
    print(res)


if __name__ == '__main__':
    load_dotenv()
    main()