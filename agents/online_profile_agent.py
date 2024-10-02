from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub

from tools.tools import get_profile_url_tavily


def search(person_details: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")
    # llm = ChatOllama(model="llama3.1")

    template = """
    Given the details of a person as "{person_info}", return the Github and LinkedIn Profile Urls by doing a web search.
    The returned results should contain not contain anything but the URLs for the LinkedIn profile and the Github profile of the person.   
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["person_info"]
    )
    tools_for_agent = [
        Tool(
            name="Do a Google search",
            func=get_profile_url_tavily,
            description="Useful for searching online profiles of a person or someone on internet",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(person_info=person_details)}
    )

    res = result["output"]
    return res


if __name__ == "__main__":
    load_dotenv()
    print(search(person_details="Prabhakar bikkaneti"))
