from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub

from tools.tools import get_profile_url_tavily


def search(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
    # llm = ChatOllama(model="llama3.1")

    template = """
    Given the details of a person as "{name_of_person}", do a web-search and return everything you find about the person, organized as bullets.
    Also return the person's LinkedIn profile URL and the Github profile URL.   
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Do a Google search",
            func=get_profile_url_tavily,
            description="Useful for searching something or someone on internet",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    load_dotenv()
    print(search(name="Prabhakar working at nvidia, studied from IIIT hyderabad"))
